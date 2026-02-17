# Plan: Skills Installer TUI

## Context

The skills repository contains 18 skill directories for AI coding assistants. Currently, `sync-skills.sh` copies ALL skills to `~/.claude/skills/` only. This TUI tool adds:
- **Multi-CLI support**: Claude, Codex, Kilo Code, Windsurf
- **Multi-scope**: User-level AND/OR Project-level (both selectable)
- **Three-state per skill**: install, update, keep, skip, or uninstall
- **Textual TUI** with Catppuccin Mocha theme
- **`uvx` launchable** via pyproject.toml entry points
- **Cross-platform**: Windows, Linux, macOS
- **Help system**: Footer hints + `?` modal

## Project Structure

```
/media/srv-main-softdev/projects/KI/skills/
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── sync-skills.sh                 # UPDATE: point to src/.../catalog/
├── psync-skills.sh                # UPDATE: point to src/.../catalog/
└── src/
    └── bx_skills/
        ├── __init__.py            # version
        ├── app.py                 # Textual App + all screens
        ├── core.py                # Non-TUI: discovery, install, parse
        ├── theme.py               # Catppuccin Mocha Theme
        └── catalog/               # MOVED: all 18 skill directories
            ├── brainstorming/
            ├── bx-bash-clean-architecture/
            ├── ... (16 more)
            └── verification-before-completion/
```

**Migration**: `git mv` all skill dirs into `src/bx_skills/catalog/`.
**Catalog path**: `CATALOG_DIR = Path(__file__).resolve().parent / "catalog"`

## pyproject.toml

```toml
[project]
name = "bx-skills"
version = "0.1.0"
description = "TUI for installing AI coding assistant skills"
requires-python = ">=3.10"
dependencies = ["textual>=1.0.0"]

[project.scripts]
bx-skills = "bx_skills.app:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/bx_skills"]
```

`uvx --from . bx-skills` or `uvx --from git+https://... bx-skills`

## CLI Targets & Paths

All use **full directory copy**. Both Kilo Code and Windsurf recursively scan subdirs.

| CLI | User Path | Project Path | Detect Dir |
|-----|-----------|-------------|------------|
| Claude Code | `.claude/skills/{skill}/` | `.claude/skills/{skill}/` | `.claude` |
| Codex | `.codex/skills/{skill}/` | `.codex/skills/{skill}/` | `.codex` |
| Kilo Code | `.kilocode/rules/{skill}/` | `.kilocode/rules/{skill}/` | `.kilocode` |
| Windsurf | *(not supported)* | `.windsurf/rules/{skill}/` | `.codeium/windsurf` |

- Paths relative to `Path.home()` (user) or `Path.cwd()` (project)
- Windsurf user-level not supported (global rules = single file). TUI warns + skips.
- **Auto-detect**: Pre-select targets where `(Path.home() / detect_dir).is_dir()`
- **Installed detection**: `{resolved_path}/SKILL.md` exists

## Data Model (`core.py`)

```python
@dataclass(frozen=True)
class CLITarget:
    name: str
    user_path_tpl: str       # ".claude/skills/{skill}" or "" if unsupported
    project_path_tpl: str    # ".claude/skills/{skill}"
    project_only: bool       # True for Windsurf
    detect_dir: str          # ".claude" - checked under ~ for auto-selection

class Scope(Enum):
    USER = "user"
    PROJECT = "project"

class SkillAction(Enum):
    INSTALL = "install"      # Not installed → copy from catalog
    UPDATE = "update"        # Installed → overwrite (DEFAULT for installed skills)
    KEEP = "keep"            # Installed → leave untouched
    SKIP = "skip"            # Not installed → ignore (DEFAULT for new skills)
    UNINSTALL = "uninstall"  # Installed → remove

@dataclass
class SkillInfo:
    dir_name: str
    name: str
    description: str
    source_path: Path

@dataclass
class InstallPlan:
    skill: SkillInfo
    target: CLITarget
    scope: Scope
    destination: Path        # Fully resolved absolute path
    action: SkillAction      # INSTALL, UPDATE, or UNINSTALL
```

## Catppuccin Mocha Theme (`theme.py`)

```python
CATPPUCCIN_MOCHA = Theme(
    name="catppuccin-mocha",
    primary="#89b4fa",       # Blue
    secondary="#cba6f7",     # Mauve
    accent="#f9e2af",        # Yellow
    foreground="#cdd6f4",    # Text
    background="#1e1e2e",    # Base
    success="#a6e3a1",       # Green
    warning="#fab387",       # Peach
    error="#f38ba8",         # Red
    surface="#313244",       # Surface0
    panel="#181825",         # Mantle
    dark=True,
)
```

Extra constants: Subtext0 `#a6adc8`, Surface1 `#45475a`, Surface2 `#585b70`, Teal `#94e2d5`

## TUI Architecture

### App State

```python
class SkillsInstallerApp(App):
    skills: list[SkillInfo]                  # From catalog
    selected_targets: list[CLITarget]        # From Screen 1
    selected_scopes: list[Scope]             # From Screen 2 (can be both!)
    skill_actions: dict[str, SkillAction]    # Per skill_dir_name, from Screen 3
```

### Screen Flow

```
TargetsScreen → ScopeScreen → SkillsScreen → ConfirmScreen → ResultsScreen
```
All screens: `Escape` back, `q` quit, `?` help modal.

---

### Screen 1: TargetsScreen (SelectionList, multi-select)

```
  Select Target CLIs:

  [X] Claude Code   (.claude/skills/)       (detected)
  [X] Codex         (.codex/skills/)        (detected)
  [ ] Kilo Code     (.kilocode/rules/)
  [ ] Windsurf      (.windsurf/rules/)      [project-level only]
```

- Auto-detect and pre-select based on `Path.home() / detect_dir`
- Validation: ≥1 target

### Screen 2: ScopeScreen (SelectionList, multi-select)

```
  Select Installation Scope:

  [X] User-level    (global, in ~/)
  [ ] Project-level  (current directory: /path/to/cwd)

  ⚠ Windsurf will be skipped for user-level scope
```

- **Both can be selected** → skills install to both locations
- User-level pre-selected by default
- Windsurf warning shown conditionally
- Validation: ≥1 scope; error if only Windsurf + only user-level

### Screen 3: SkillsScreen (ListView with custom SkillItems)

```
  Select Skills:

  [ ] brainstorming                                       (new)
      You MUST use this before any creative work...
  [+] bx-bash-clean-architecture                          (update)
      Use when structuring Bash 4.3+ scripts...
  [+] bx-bash-reference                                   (update)
      Complete GNU Bash 5.3 reference...
  [-] bx-enhance-code-quality                             (UNINSTALL)
      Use when asked to rate, score, audit...

  [ Select All ]  [ Deselect All ]
```

**Defaults**: Installed → UPDATE (selected). Not installed → SKIP (deselected).

**State transitions:**

| State | Space | `d` key |
|-------|-------|---------|
| SKIP (not installed) | → INSTALL | no-op |
| INSTALL | → SKIP | no-op |
| UPDATE (installed, default) | → KEEP | → UNINSTALL |
| KEEP (installed) | → UPDATE | → UNINSTALL |
| UNINSTALL (installed) | → UPDATE | → KEEP |

**Visual:**

| State | Prefix | Tag | Color |
|-------|--------|-----|-------|
| INSTALL | `[+]` | (new) | primary/blue |
| UPDATE | `[+]` | (update) | primary/blue |
| KEEP | `[ ]` | (installed) | success/green dimmed |
| SKIP | `[ ]` | | dimmed |
| UNINSTALL | `[-]` | (UNINSTALL) | error/red |

**Installed status**: Computed per skill across ALL (selected_targets x selected_scopes). A skill is "installed" if it exists in ANY target+scope combination.

**Buttons**: `Select All` (→ INSTALL/UPDATE all), `Deselect All` (→ SKIP/KEEP all).
**Keys**: `Space` toggle, `d` uninstall, `a` select all, `n` deselect all, `Enter` next.

### Screen 4: ConfirmScreen (Static/RichLog, scrollable)

**Install plans are generated per (skill × target × scope)**. Uninstall only for combinations where actually installed. This makes scope explicit for every operation.

```
  Will Install/Update:
  ────────────────────
  Claude Code · User (~/.claude/skills/):
    [+] brainstorming/                    (new)
    [+] bx-bash-reference/               (update)
  Claude Code · Project (.claude/skills/):
    [+] brainstorming/                    (new)
  Kilo Code · User (~/.kilocode/rules/):
    [+] brainstorming/                    (new)
    [+] bx-bash-reference/               (update)

  Will Uninstall:
  ───────────────
  Claude Code · User (~/.claude/skills/):
    [-] bx-enhance-code-quality/
  Claude Code · Project (.claude/skills/):
    [-] bx-enhance-code-quality/

  Unchanged: 2 skills kept

  Summary: 5 installs, 2 uninstalls, 2 unchanged
```

Each line shows the **exact path** so the user knows precisely where changes happen. Uninstalls only appear for target+scope combinations where the skill IS actually installed (checked via `check_installed()`).

**Keys**: `Enter` execute, `Escape` back.

### Screen 5: ResultsScreen (RichLog, progressive)

```
  [OK] brainstorming → Claude Code · User (installed)
  [OK] brainstorming → Claude Code · Project (installed)
  [OK] brainstorming → Kilo Code · User (installed)
  [OK] bx-bash-reference → Claude Code · User (updated)
  [OK] bx-enhance-code-quality → Claude Code · User (uninstalled)
  [OK] bx-enhance-code-quality → Claude Code · Project (uninstalled)
  [!!] bx-bash-reference → Kilo Code · User - Permission denied

  6 succeeded, 1 failed
```

Results appended per operation via `RichLog.write`.

### HelpScreen (Modal, pushed by `?`)

```
  Skills Installer — Help

  Navigation
    Enter       Next step
    Escape      Previous step / close help
    q           Quit

  Targets & Scope
    Multiple CLIs and scopes can be selected simultaneously.
    Detected CLIs are pre-selected based on ~/.<cli-dir>/ existence.

  Skills Screen
    Space       Toggle: install ↔ skip (new) or update ↔ keep (installed)
    d           Toggle uninstall for installed skills
    a           Select all for install/update
    n           Deselect all (reset to skip/keep)

  Defaults
    Installed skills default to UPDATE (will overwrite with latest).
    Deselected installed skills are KEPT (no changes).
    Not-installed skills default to SKIP.
    Uninstall removes from ALL selected scopes where present.
```

## Core Functions (`core.py`)

| Function | Purpose |
|----------|---------|
| `parse_frontmatter(path)` | YAML frontmatter → (name, desc). Handles unquoted, quoted, `>`, `>-` |
| `discover_skills(catalog_dir)` | Scan catalog dir, parse SKILL.md, return sorted list |
| `check_installed(skill, target, scope)` | `(resolved_path / "SKILL.md").exists()` |
| `resolve_destination(skill, target, scope)` | `Path.home() / tpl` or `Path.cwd() / tpl` |
| `install_skill(plan)` | `rmtree` + `copytree(ignore=('__pycache__', '*.pyc'))` |
| `uninstall_skill(plan)` | `rmtree(destination)`. Only if actually exists. |
| `get_active_targets(targets, scopes)` | Filter project_only targets from USER scope |
| `build_plans(skills, actions, targets, scopes)` | Generate `InstallPlan` list for all combos |

`CATALOG_DIR = Path(__file__).resolve().parent / "catalog"`

## Cross-Platform

- `pathlib.Path` everywhere (auto `/` vs `\`)
- `Path.home()` for home dir (Linux/macOS/Windows)
- `shutil.copytree`/`rmtree` cross-platform
- No `chown` or Unix-specific calls

## YAML Frontmatter Parser

No PyYAML. Line-by-line state machine handling 4 variants:
- Unquoted: `description: Use when...`
- Double-quoted: `description: "You MUST..."`
- Multi-line `>`: folded block
- Multi-line `>-`: folded block, strip trailing

## Edge Cases

- Terminal too small: Textual handles gracefully
- No skills found: Error notification
- Permission errors: Caught per-operation, shown in results
- Overwrite on update: `rmtree` + `copytree`
- Uninstall: `rmtree`, only for paths where skill actually exists
- Missing parent dirs: `makedirs(exist_ok=True)`
- Windsurf + User scope: Warning + skip
- All skills KEEP/SKIP: "Nothing to do" message

## Implementation Order

0. Save this plan as `/media/srv-main-softdev/projects/KI/skills/concept.md`
1. Create `src/bx_skills/` directory structure + `__init__.py`
2. `git mv` all 18 skill dirs into `src/bx_skills/catalog/`
3. Create `pyproject.toml`
4. Create `theme.py` (Catppuccin Mocha)
5. Create `core.py` (data model + pure functions)
6. Create `app.py` (Textual App + all screens)
7. Update `sync-skills.sh` and `psync-skills.sh`
8. Test with `uvx --from . bx-skills`

## Verification

1. `cd /media/srv-main-softdev/projects/KI/skills && uvx --from . bx-skills`
2. Screen 1: verify auto-detected targets pre-selected
3. Screen 2: select both User + Project → Enter
4. Screen 3: verify installed = blue `[+] (update)` by default
5. Toggle Space/d, test Select All/Deselect All buttons
6. Screen 4: verify operations grouped by target + scope with full paths
7. Screen 4: verify uninstall shows each scope separately
8. Screen 5: verify results per operation
9. `ls ~/.claude/skills/` and `ls ~/.kilocode/rules/` to confirm
10. Test `?` help modal
11. Test Escape back-navigation
12. Test on project-level from temp directory
