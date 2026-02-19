"""Data model and pure functions for skill discovery, planning, and installation."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

__all__ = [
    # Exceptions
    "SkillsError",
    "SkillInstallError",
    "SkillUninstallError",
    # Data classes & enums
    "CLITarget",
    "Scope",
    "SkillAction",
    "SkillInfo",
    "InstallPlan",
    # Constants
    "CATALOG_DIR",
    "CLI_TARGETS",
    # Slug helpers
    "get_target_slug",
    "get_all_target_slugs",
    "resolve_target_by_slug",
    # Discovery & resolution
    "detect_installed_targets",
    "resolve_skills_by_names",
    "parse_frontmatter",
    "discover_skills",
    "resolve_destination",
    "check_installed",
    # Planning & execution
    "get_active_targets",
    "build_plans",
    "install_skill",
    "uninstall_skill",
]

# ── Exceptions ────────────────────────────────────────────────────────────────


class SkillsError(Exception):
    """Base exception for all bx_skills operations."""


class SkillInstallError(SkillsError):
    """Raised when a skill install or update fails."""


class SkillUninstallError(SkillsError):
    """Raised when a skill uninstall fails."""


# ── Data classes ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class CLITarget:
    """A CLI tool that supports skill installation."""

    name: str
    user_path_tpl: str  # e.g. ".claude/skills/{skill}" or "" if unsupported
    project_path_tpl: str  # e.g. ".claude/skills/{skill}"
    project_only: bool  # True if user-level not supported (Windsurf)
    detect_dir: str  # Checked under ~/ for auto-selection


class Scope(Enum):
    USER = "user"
    PROJECT = "project"


class SkillAction(Enum):
    INSTALL = "install"
    UPDATE = "update"
    KEEP = "keep"
    SKIP = "skip"
    UNINSTALL = "uninstall"


@dataclass
class SkillInfo:
    """A skill discovered from the catalog."""

    dir_name: str
    name: str
    description: str
    source_path: Path


@dataclass
class InstallPlan:
    """A single install/update/uninstall operation."""

    skill: SkillInfo
    target: CLITarget
    scope: Scope
    destination: Path
    action: SkillAction


# ── Constants ─────────────────────────────────────────────────────────────────

CATALOG_DIR = Path(__file__).resolve().parent / "catalog_skills"

CLI_TARGETS: list[CLITarget] = [
    CLITarget(
        name="Claude Code",
        user_path_tpl=".claude/skills/{skill}",
        project_path_tpl=".claude/skills/{skill}",
        project_only=False,
        detect_dir=".claude",
    ),
    CLITarget(
        name="Codex",
        user_path_tpl=".codex/skills/{skill}",
        project_path_tpl=".codex/skills/{skill}",
        project_only=False,
        detect_dir=".codex",
    ),
    CLITarget(
        name="Kilo Code",
        user_path_tpl=".kilocode/rules/{skill}",
        project_path_tpl=".kilocode/rules/{skill}",
        project_only=False,
        detect_dir=".kilocode",
    ),
    CLITarget(
        name="Windsurf",
        user_path_tpl="",
        project_path_tpl=".windsurf/rules/{skill}",
        project_only=True,
        detect_dir=".codeium/windsurf",
    ),
]


# ── Slug mapping & helpers ───────────────────────────────────────────────────

_TARGET_SLUGS: dict[str, str] = {
    "Claude Code": "claude-code",
    "Codex": "codex",
    "Kilo Code": "kilo-code",
    "Windsurf": "windsurf",
}

_SLUG_TO_TARGET: dict[str, CLITarget] = {}


def _build_slug_index() -> dict[str, CLITarget]:
    if not _SLUG_TO_TARGET:
        for target in CLI_TARGETS:
            _SLUG_TO_TARGET[_TARGET_SLUGS[target.name]] = target
    return _SLUG_TO_TARGET


def get_target_slug(target: CLITarget) -> str:
    """Return the CLI slug for a target (e.g. 'claude-code')."""
    return _TARGET_SLUGS[target.name]


def get_all_target_slugs() -> list[str]:
    """Return all target slugs in definition order."""
    return [_TARGET_SLUGS[t.name] for t in CLI_TARGETS]


def resolve_target_by_slug(slug: str) -> CLITarget | None:
    """Look up a CLITarget by its CLI slug, or None if unknown."""
    return _build_slug_index().get(slug)


def detect_installed_targets() -> list[CLITarget]:
    """Return targets whose detect_dir exists under ~/."""
    return [t for t in CLI_TARGETS if (Path.home() / t.detect_dir).is_dir()]


def resolve_skills_by_names(
    names: list[str],
    catalog_dir: Path | None = None,
) -> tuple[list[SkillInfo], list[str]]:
    """Resolve skill dir_names to SkillInfo objects.

    Returns (found, missing) where missing contains names not in catalog.
    """
    by_name = {s.dir_name: s for s in discover_skills(catalog_dir)}
    found = [by_name[n] for n in names if n in by_name]
    missing = [n for n in names if n not in by_name]
    return found, missing


# ── Frontmatter parsing ──────────────────────────────────────────────────────


def _read_block_scalar(indicator: str, lines: list[str], start: int) -> tuple[str, int]:
    """Read a YAML block scalar (``>``, ``>-``, ``|``, or ``|-``).

    Returns (joined_value, next_line_index).
    """
    block_lines: list[str] = []
    i = start
    while i < len(lines):
        bline = lines[i]
        if bline.strip() == "---" or (bline and not bline[0].isspace()):
            break
        block_lines.append(bline.strip())
        i += 1
    joiner = "\n" if indicator.startswith("|") else " "
    value = joiner.join(bl for bl in block_lines if bl)
    if indicator.endswith("-"):
        value = value.rstrip()
    return value, i


def parse_frontmatter(path: Path) -> tuple[str, str]:
    """Parse YAML frontmatter from a SKILL.md file.

    Returns (name, description).  Falls back to (parent dir name, "") on
    any parse failure.
    """
    fallback_name = path.parent.name
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return fallback_name, ""

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return fallback_name, ""

    fields: dict[str, str] = {}
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            break

        if ":" in line:
            key, _, raw_value = line.partition(":")
            key = key.strip()
            raw_value = raw_value.strip()

            if raw_value.startswith('"') and raw_value.endswith('"') and len(raw_value) > 1:
                fields[key] = raw_value[1:-1]
            elif raw_value in (">", ">-", "|", "|-"):
                fields[key], i = _read_block_scalar(raw_value, lines, i + 1)
                continue
            else:
                fields[key] = raw_value

        i += 1

    name = fields.get("name", fallback_name)
    description = " ".join(fields.get("description", "").split())
    return name, description


# ── Discovery ─────────────────────────────────────────────────────────────────


def discover_skills(catalog_dir: Path | None = None) -> list[SkillInfo]:
    """Scan the catalog directory and return sorted SkillInfo list."""
    catalog = catalog_dir or CATALOG_DIR
    if not catalog.is_dir():
        return []

    skills: list[SkillInfo] = []
    for entry in sorted(catalog.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        skill_md = entry / "SKILL.md"
        name, description = parse_frontmatter(skill_md)
        skills.append(
            SkillInfo(
                dir_name=entry.name,
                name=name,
                description=description,
                source_path=entry,
            )
        )

    return skills


# ── Path resolution & status ──────────────────────────────────────────────────


def resolve_destination(skill: SkillInfo, target: CLITarget, scope: Scope) -> Path:
    """Resolve the full destination path for a skill."""
    if scope == Scope.USER:
        tpl = target.user_path_tpl
        base = Path.home()
    else:
        tpl = target.project_path_tpl
        base = Path.cwd()

    return base / tpl.format(skill=skill.dir_name)


def check_installed(skill: SkillInfo, target: CLITarget, scope: Scope) -> bool:
    """Check whether a skill is already installed at the destination."""
    dest = resolve_destination(skill, target, scope)
    return (dest / "SKILL.md").is_file()


# ── Planning ──────────────────────────────────────────────────────────────────


def get_active_targets(
    targets: list[CLITarget],
    scopes: list[Scope],
) -> list[tuple[CLITarget, Scope]]:
    """Return valid (target, scope) pairs, filtering invalid combinations.

    Filters:
    - USER scope for project_only targets (e.g. Windsurf).
    - USER scope when user_path_tpl is empty.
    - PROJECT scope when CWD is the home directory and the project template
      matches the user template (paths would resolve identically).
    """
    cwd_is_home = Path.cwd() == Path.home()
    pairs: list[tuple[CLITarget, Scope]] = []
    for target in targets:
        for scope in scopes:
            if scope == Scope.USER and target.project_only:
                continue
            if scope == Scope.USER and not target.user_path_tpl:
                continue
            if (
                scope == Scope.PROJECT
                and cwd_is_home
                and target.user_path_tpl
                and target.user_path_tpl == target.project_path_tpl
            ):
                continue
            pairs.append((target, scope))
    return pairs


def build_plans(
    skills: list[SkillInfo],
    actions: dict[str, SkillAction],
    targets: list[CLITarget],
    scopes: list[Scope],
) -> list[InstallPlan]:
    """Generate InstallPlan list for all (skill x target x scope) combinations."""
    active = get_active_targets(targets, scopes)
    plans: list[InstallPlan] = []

    for skill in skills:
        action = actions.get(skill.dir_name, SkillAction.SKIP)

        if action in (SkillAction.KEEP, SkillAction.SKIP):
            continue

        for target, scope in active:
            dest = resolve_destination(skill, target, scope)

            if action == SkillAction.UNINSTALL:
                # Only plan uninstall where actually installed
                if check_installed(skill, target, scope):
                    plans.append(InstallPlan(skill, target, scope, dest, action))
            else:
                # INSTALL or UPDATE
                plans.append(InstallPlan(skill, target, scope, dest, action))

    return plans


# ── Execution ─────────────────────────────────────────────────────────────────


def _ignore_pycache(directory: str, contents: list[str]) -> set[str]:
    """Ignore pattern for shutil.copytree."""
    ignored: set[str] = set()
    for item in contents:
        if item == "__pycache__" or item.endswith(".pyc"):
            ignored.add(item)
    return ignored


def install_skill(plan: InstallPlan) -> None:
    """Install or update a skill by copying from the catalog.

    Raises:
        SkillInstallError: If the filesystem operation fails.
    """
    try:
        plan.destination.parent.mkdir(parents=True, exist_ok=True)
        if plan.destination.exists():
            shutil.rmtree(plan.destination)
        shutil.copytree(plan.skill.source_path, plan.destination, ignore=_ignore_pycache)
    except OSError as exc:
        raise SkillInstallError(f"{plan.skill.dir_name}: {exc}") from exc


def uninstall_skill(plan: InstallPlan) -> None:
    """Remove a skill directory.

    Raises:
        SkillUninstallError: If the filesystem operation fails.
    """
    try:
        if plan.destination.exists():
            shutil.rmtree(plan.destination)
    except OSError as exc:
        raise SkillUninstallError(f"{plan.skill.dir_name}: {exc}") from exc
