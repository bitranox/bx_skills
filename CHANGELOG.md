# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Versioning note:** In the context of a skills collection (not a traditional software library),
> Semantic Versioning is applied as follows:
>
> - **MAJOR** — Backward-incompatible changes: skills renamed, removed, or restructured in ways
>   that break existing workflows or references.
> - **MINOR** — New skills, new reference documents, or new sync scripts added in a
>   backward-compatible manner.
> - **PATCH** — Fixes, corrections, and small improvements to existing skills or documentation.

## [Unreleased]

## [1.2.7] - 2026-02-19

### Changed

- **bx-enhance-code-quality**: All references to `CLAUDE.md` updated to be multi-platform.
  Added mapping note (Claude Code → `CLAUDE.md`, Codex → `AGENTS.md`, Kilo Code / Windsurf →
  equivalent) and replaced bare `CLAUDE.md` mentions with "project instructions file" or
  `CLAUDE.md / AGENTS.md` throughout.
- **bx-skill-writer**: Updated `CLAUDE.md` reference in "Don't create for" section to
  include `AGENTS.md` as alternative.

## [1.2.6] - 2026-02-19

### Changed

- **bx-humanize-en / bx-humanise-de**: Added scope guard instruction — humanizing
  is now restricted to prose content (blog posts, emails, articles, etc.) and explicitly
  excluded from code, docstrings, API docs, changelogs, and other technical artifacts.
  The skill now asks the user for confirmation before applying changes.

## [1.2.5] - 2026-02-19

### Fixed

- **core/TUI/CLI**: When the current working directory is the user's home directory,
  project-scope skills resolved to the same path as user-scope skills. Uninstalling
  "project" skills in this situation would accidentally delete user skills.
  `get_active_targets()` now filters out redundant project-scope pairs when CWD equals
  HOME and path templates match. The TUI hides the project column in this case.

## [1.2.4] - 2026-02-19

### Fixed

- **TUI**: Skill descriptions now word-wrap in the DataTable when the terminal window
  is narrow. Previously long descriptions were truncated instead of wrapping to the
  next line (`height=None` on `add_row` enables auto-height).

## [1.2.3] - 2026-02-19

### Fixed

- **core**: Descriptions from literal block scalars (`|`) now collapse newlines to spaces,
  matching the display behavior of folded scalars (`>`). Prevents multi-line descriptions
  from rendering with hard line breaks in the `bx-skills list` table.

## [1.2.2] - 2026-02-19

### Fixed

- **core**: Frontmatter parser now handles YAML literal block scalars (`|` and `|-`).
  Previously only folded scalars (`>` / `>-`) were supported, causing `description: |`
  multi-line values to display as the literal character `|`.
- **md-table-formatting**: Tables inside blockquotes (`> | ... |`) are now detected and
  reformatted. Previously only bare table rows starting with `|` were recognized.

## [1.2.1] - 2026-02-19

### Changed

- **bx-skill-writer**: Added CRITICAL callouts in SKILL.md and testing-skills-with-subagents.md
  ensuring GREEN/REFACTOR tests use the current working-directory version of a skill, not a stale
  installed copy at `~/.claude/skills/`. Added checklist items in both files. Clarified the
  `[skill-being-tested]` placeholder to read from the working directory.
- **bx-skill-writer**: Updated CLAUDE_MD_TESTING.md documentation variants A–D to show both
  `.claude/skills/` (project) and `~/.claude/skills/` (personal) paths.

### Fixed

- **bx-humanise-de**: Corrections and refinements to AI writing detection patterns.
- **bx-humanize-en**: Corrections and refinements to AI writing detection patterns.

## [1.2.0] - 2026-02-19

### Added

- **bx-humanize-en**: Extended from 24 to 35 AI writing detection patterns based on the February 2026
  revision of Wikipedia's "Signs of AI writing". New sections include: unusual tables, subject lines,
  skipping heading levels, section summaries, phrasal templates, prompt refusal artifacts, markdown
  artifacts, ChatGPT search reference artifacts, UTM source parameters, sudden style shifts, and
  verbose edit summaries. Expanded word lists and added key research citations.
- **bx-humanise-de**: Complete rewrite based on the German Wikipedia page "Anzeichen für
  KI-generierte Inhalte". Now 30 pattern sections with proper German umlauts, German-specific
  word lists, real examples from deleted German Wikipedia articles, and new German-specific patterns
  including ChatGPT-typischer Sound, anglizistische Konstruktionen, and Markdown-Artefakte.

### Changed

- **bx-skill-writer**: Added clarification to work on skills in the current directory first.

## [1.1.1] - 2026-02-19

### Fixed

- Dependency pin: bumped `virtualenv>=20.37.0` to `>=20.38.0` (v20.37.0 was yanked from PyPI).

### Changed

- CI/CD workflow updated for public repository defaults.
- Bandit configured to read `pyproject.toml` for scan settings.

### Added

- Empty Quickstart notebook placeholder.

## [1.1.0] - 2026-02-17

### Added

- Domain exceptions: `SkillsError`, `SkillInstallError`, `SkillUninstallError` in `core.py`.
- `__all__` export list in `core.py` documenting the public API.
- `InstallerScreen` typed base class for TUI screens, replacing scattered `type: ignore[attr-defined]`.
- `[project.urls]` section in `pyproject.toml` (Homepage, Repository, Issues).
- `homepage` URL set in package metadata.

### Changed

- `install_skill` and `uninstall_skill` now raise `SkillInstallError`/`SkillUninstallError` instead of raw `OSError`.
- CLI and TUI catch `SkillsError` instead of `OSError` for consistent domain error handling.
- CLI install/uninstall loops extracted into shared `_execute_plans` helper.
- README skills table updated to match current catalog (18 skills).

### Removed

- Dead `ScopeScreen` class from TUI (scope selection merged into SkillsScreen).
- Dead `_err_console()` function from CLI.
- Dead `skill_actions` attribute from `SkillsInstallerApp`.
- File-level `# pyright: reportAttributeAccessIssue=false` suppression from `app.py`.

## [1.0.0] - 2026-02-17

### Added

- **Rich-click CLI** with 6 subcommands: `install`, `uninstall`, `list`, `status`, `info`, `tui`.
- Non-interactive install/uninstall for CI/CD pipelines, shell aliases, and scripting.
- `--target` option supporting `auto`, `all`, `claude-code`, `codex`, `kilo-code`, `windsurf` (repeatable).
- `--scope` option: `user`, `project`, `both`.
- `--quiet` flag for machine-readable output in `list` and `status`.
- `--yes` flag to skip uninstall confirmation.
- `info` command showing version, metadata, catalog size, and detected CLIs.
- Slug mapping helpers in `core.py`: `get_target_slug`, `resolve_target_by_slug`, `detect_installed_targets`, `resolve_skills_by_names`.
- `cli_runner` test fixture in `conftest.py`.
- `tests/test_cli.py` — 25 CLI tests covering all commands.
- `tests/test_core_helpers.py` — 9 tests for slug mapping and helper functions.
- `rich-click>=1.9.7` dependency.

### Fixed

- TUI `ResultsScreen` crash (`AttributeError: 'ResultsScreen' object has no attribute 'call_from_thread'`):
  changed `self.call_from_thread()` to `self.app.call_from_thread()` in the threaded worker.
- CI: Bandit scan now reads `pyproject.toml` config to exclude `catalog_skills/` from scanning.
- CI: Removed notebook execution job (no notebooks in this project).

### Changed

- **Breaking:** Entry point changed from `bx_skills.app:main` (TUI) to `bx_skills.cli:main` (CLI).
  The TUI is now available via `bx-skills tui`.
- `bx-skills` with no subcommand now shows help instead of launching the TUI.
- Package title updated to "CLI & TUI for installing AI coding assistant skills".
- `CLAUDE.md` rewritten for the bx_skills project (replaced template boilerplate).
- `README.md` updated with CLI usage examples and smoke test commands.

## [0.2.0] - 2026-02-12

### Added

- **bx-textual** skill — Complete Textual TUI framework documentation reference including API
  docs, guides, CSS reference, FAQ, and widget catalog.

### Fixed

- Minor correction in **bx-bash-reference** SKILL.md.

## [0.1.0] - 2026-02-12

### Added

- Initial repository setup with README, `.gitignore`, and project structure.
- Sync scripts for installing skills: `sync-skills.sh`, `sync-skills.ps1` (user-level),
  `psync-skills.sh`, `psync-skills.ps1` (project-level).
- **brainstorming** — Collaborative design exploration before implementation.
- **bx-bash-clean-architecture** — Layered ports-and-adapters architecture for Bash 4.3+.
- **bx-bash-reference** — Complete GNU Bash 5.3 syntax and builtins reference.
- **bx-enhance-code-quality** — Code quality scoring and improvement workflow.
- **bx-python-clean-architecture** — Typed Python ports-and-adapters architecture.
- **bx-python-libraries-to-use** — Standardized Python library choices.
- **bx-uv** — Complete uv (v0.10.2) package manager reference.
- **executing-plans** — Execute implementation plans with review checkpoints.
- **force-using-skills** — Enforce skill invocation when applicable.
- **systematic-debugging** — Root-cause-first debugging methodology.
- **test-driven-development** — TDD workflow enforcement.
- **verification-before-completion** — Evidence-based completion verification.
- **writing-plans** — Comprehensive implementation plan creation.
- **writing-skills** — TDD-based skill documentation authoring.
