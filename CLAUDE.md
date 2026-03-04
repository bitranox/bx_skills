# Claude Code Guidelines for bx_skills

## Session Initialization

When starting a new session, read and apply the following system prompt files from `/media/srv-main-softdev/projects/softwarestack/systemprompts`:

### Core Guidelines (Always Apply)
- `core_programming_solid.md`

### Python-Specific Guidelines
When working with Python code:
- `core_programming_solid.md`
- `python_solid_architecture_enforcer.md`
- use skill `bx-python-clean-architecture`
- `python_clean_code.md`
- `python_small_functions_style.md`
- use skill `bx-python-libraries-to-use`

## Project Overview

**bx_skills** is a CLI & TUI for installing AI coding assistant skills to Claude Code, Codex, Kilo Code, and Windsurf.

- **CLI** (`cli.py`): Rich-click commands for non-interactive use (CI/CD, scripts, shell aliases)
- **TUI** (`app.py`): Textual interactive installer with multi-step wizard
- **Core** (`core.py`): Pure business logic — discovery, planning, installation, slug mapping

## Project Structure

```
bx_skills/
├── .github/
│   └── workflows/              # GitHub Actions CI/CD workflows
├── src/
│   └── bx_skills/
│       ├── __init__.py         # Package init, re-exports __version__
│       ├── __init__conf__.py   # Static metadata (name, version, title, author)
│       ├── core.py             # Pure business logic (data classes, discovery, planning, execution)
│       ├── cli.py              # Rich-click CLI (install, uninstall, list, status, info, tui)
│       ├── app.py              # Textual TUI application (SkillsInstallerApp, screens)
│       ├── theme.py            # Catppuccin Mocha theme for TUI
│       ├── catalog_skills/     # Bundled skill catalog (shipped with package)
│       └── catalog_commands/   # Bundled command catalog
├── tests/
│   ├── conftest.py             # Shared fixtures (fake_home, fake_cwd, catalog_dir, cli_runner)
│   ├── test_cli.py             # CLI command tests (CliRunner)
│   ├── test_core_helpers.py    # Slug mapping & helper tests
│   ├── test_core_discovery.py  # Skill discovery tests
│   ├── test_core_resolution.py # Path resolution & installed checks
│   ├── test_core_planning.py   # Build plans & active targets
│   ├── test_core_execution.py  # Install/uninstall execution
│   ├── test_core_frontmatter.py # YAML frontmatter parsing
│   ├── test_app_screens.py     # TUI screen tests
│   ├── test_app_integration.py # TUI integration tests
│   ├── test_init.py            # Package metadata tests
│   └── test_theme.py           # Theme tests
├── CLAUDE.md                   # Claude Code guidelines (this file)
├── README.md                   # Project overview
├── Makefile                    # Make targets (delegates to uvx bmk@latest)
├── pyproject.toml              # Project metadata, dependencies, tool config
└── codecov.yml                 # Codecov configuration
```

## Architecture

This is a **flat module** project (not layered Clean Architecture). All source lives in `src/bx_skills/`:

| Module              | Role                                                                                                                                                                        |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `core.py`           | Pure business logic: data classes (`CLITarget`, `Scope`, `SkillInfo`, `InstallPlan`), discovery, path resolution, planning, installation/uninstall execution, slug mapping. |
| `cli.py`            | CLI adapter: Rich-click commands wrapping core functions. Thin layer — validation, argument parsing, output formatting.                                                     |
| `app.py`            | TUI adapter: Textual app with 4 screens (Targets, Skills, Confirm, Results).                                                                                                 |
| `theme.py`          | Catppuccin Mocha theme constants.                                                                                                                                           |
| `__init__conf__.py` | Static metadata constants kept in sync with `pyproject.toml`.                                                                                                               |

**Dependency direction**: `cli.py` and `app.py` import from `core.py`. `core.py` has no project imports.

## CLI Commands

```
bx-skills                     # Shows help
bx-skills tui                 # Launch interactive TUI
bx-skills list [-q]           # Browse catalog
bx-skills status [-t] [-s] [-q]  # Audit installed skills
bx-skills install SKILL [...] [--all] [-t] [-s] [-q]
bx-skills uninstall SKILL [...] [--all] [-t] [-s] [-y] [-q]
bx-skills info                # Version, metadata, detected CLIs
```

**Shared options**:
- `--target / -t`: `auto` (default), `all`, `claude-code`, `codex`, `kilo-code`, `windsurf` (repeatable)
- `--scope / -s`: `user` (default), `project`, `both`
- `--quiet / -q`: Suppress non-error output; machine-readable for list/status
- `--yes / -y`: Skip confirmation (uninstall only)

## Key Data Types (core.py)

- `CLITarget`: Frozen dataclass — name, path templates, project_only flag, detect_dir
- `Scope`: Enum — USER, PROJECT
- `SkillInfo`: Dataclass — dir_name, name, description, source_path
- `InstallPlan`: Dataclass — skill, target, scope, destination, action
- `SkillAction`: Enum — INSTALL, UPDATE, KEEP, SKIP, UNINSTALL
- `CLI_TARGETS`: List of 4 targets (Claude Code, Codex, Kilo Code, Windsurf)
- `CATALOG_DIR`: Path to bundled catalog_skills directory

## Versioning & Releases

- **Single Source of Truth**: Package version is in `pyproject.toml` (`[project].version`)
- **Version Bumps**: Update `pyproject.toml` and `__init__conf__.py`
- **Release Tags**: Format is `vX.Y.Z`

## Common Make Targets

All targets delegate to `uvx bmk@latest`. Trailing arguments are forwarded.

| Target    | Aliases     | Description                                       |
|-----------|-------------|---------------------------------------------------|
| `test`    | `t`         | Lint, format, type-check, run tests with coverage |
| `build`   | `bld`       | Build wheel/sdist artifacts                       |
| `clean`   | `cln`, `cl` | Remove caches, coverage, and build artifacts      |
| `bump`    |             | Bump patch version                                |
| `push`    | `psh`, `p`  | Run tests, commit, and push to remote             |
| `release` | `rel`, `r`  | Tag vX.Y.Z, push, create GitHub release           |

## Testing

- **Framework**: pytest with pytest-cov, pytest-asyncio
- **Coverage threshold**: 80% (configured in pyproject.toml)
- **CLI tests**: Use Click's `CliRunner` via `cli_runner` fixture
- **TUI tests**: Use Textual's `App.run_test()` pilot pattern
- **Isolation**: `fake_home` and `fake_cwd` fixtures monkeypatch `Path.home()` and `Path.cwd()`; `catalog_dir` provides a temp catalog. CLI tests use `_patch_catalog` autouse fixture to monkeypatch `CATALOG_DIR`.

### Test Fixtures (conftest.py)

| Fixture               | Purpose                                              |
|-----------------------|------------------------------------------------------|
| `cli_runner`          | Fresh `CliRunner` per test                           |
| `fake_home`           | Redirects `Path.home()` to temp dir                  |
| `fake_cwd`            | Redirects `Path.cwd()` to temp dir                   |
| `catalog_dir`         | Temp catalog with 2 skills, hidden dir, regular file |
| `sample_skill`        | SkillInfo backed by real temp directory              |
| `second_skill`        | Second SkillInfo for multi-skill tests               |
| `sample_target`       | Typical CLITarget with both scopes                   |
| `project_only_target` | Project-only CLITarget (like Windsurf)               |

## Coding Style

- **Linting**: Ruff (line-length 120, target py310)
- **Type checking**: Pyright standard mode
- **Imports**: isort via Ruff
- **Per-file ignores**: Tests get relaxed rules (S101, PLR2004, etc.); `cli.py` gets FBT/PLR relaxations

## Security & Configuration

- `.env` files are for local tooling only (CodeCov tokens, etc.)
- **NEVER** commit secrets to version control
- `catalog_skills/` is bundled data, not executable code — excluded from Ruff and Pyright

## Commit & Push Policy

- **Always run `make test` before pushing** to avoid lint/test breakage
- Ensure all tests pass and code is properly formatted
- Monitor GitHub Actions after pushing
- **NEVER add Claude as co-author in commits** — no `Co-Authored-By` lines
