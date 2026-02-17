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
