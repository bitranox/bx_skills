# bx_skills

<!-- Badges -->
[![CI](https://github.com/bitranox/bx_skills/actions/workflows/default_cicd_public.yml/badge.svg)](https://github.com/bitranox/bx_skills/actions/workflows/default_cicd_public.yml)
[![CodeQL](https://github.com/bitranox/bx_skills/actions/workflows/codeql.yml/badge.svg)](https://github.com/bitranox/bx_skills/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?logo=github&logoColor=white&style=flat-square)](https://codespaces.new/bitranox/bx_skills?quickstart=1)
[![PyPI](https://img.shields.io/pypi/v/bx_skills.svg)](https://pypi.org/project/bx_skills/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/bx_skills.svg)](https://pypi.org/project/bx_skills/)
[![Code Style: Ruff](https://img.shields.io/badge/Code%20Style-Ruff-46A3FF?logo=ruff&labelColor=000)](https://docs.astral.sh/ruff/)
[![codecov](https://codecov.io/gh/bitranox/bx_skills/graph/badge.svg?token=UFBaUDIgRk)](https://codecov.io/gh/bitranox/bx_skills)
[![Maintainability](https://qlty.sh/badges/041ba2c1-37d6-40bb-85a0-ec5a8a0aca0c/maintainability.svg)](https://qlty.sh/gh/bitranox/projects/bx_skills)
[![Known Vulnerabilities](https://snyk.io/test/github/bitranox/bx_skills/badge.svg)](https://snyk.io/test/github/bitranox/bx_skills)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)



# Claude Skills

A collection of Claude Code skills for software engineering workflows.

Skills prefixed with `bx-` are custom-built or modified skills from one of the following sources :

- [Vercel Agent Skills Directory](https://skills.sh)
- [Obra Superpowers Skill Library](https://skills.sh/obra/superpowers)
- [React/Next.js Performance Optimization](https://skills.sh/vercel-labs/agent-skills)
- [Writing Clearly and Concisely](https://skills.sh/softaworks/agent-tools)
- [Agentation](https://skills.sh/benjitaylor/agentation)
- [Tailwind Design System](https://skills.sh/wshobson/agents/tailwind)
- [UI/UX Pro Max](https://skills.sh/nextlevelbuilder/ui)

## Installation

```bash
# install uv/uvx
python -m pip install --upgrade uv
# install bx-skills
uvx bx-skills@latest --help
```

## CLI Usage

```bash
uvx bx-skills@latest --help                                        # Show help
uvx bx-skills@latest list                                          # Browse catalog
uvx bx-skills@latest list -q                                       # Machine-readable list
uvx bx-skills@latest status --target all --scope both              # Audit installed skills
uvx bx-skills@latest install --all --target claude-code            # Install all skills
uvx bx-skills@latest install bx-textual --target claude-code --scope project  # Install specific skill
uvx bx-skills@latest uninstall bx-textual --target claude-code -y  # Remove a skill
uvx bx-skills@latest info                                          # Version & metadata
uvx bx-skills@latest tui                                           # Launch interactive TUI
```

## Auto-Update via Shell Alias

### Bash

Add the following to `~/.bashrc` to automatically sync skills before every `claude` session:

```bash
alias claude='uvx bx-skills@latest install --all -q && command claude'
```

Reload your shell or run `source ~/.bashrc` to activate.

## Skills

| Skill                              | Description                                                                                                                 |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| **brainstorming**                  | Collaborative design exploration before implementation. Explores user intent, requirements, and design.                     |
| **bx-bash-clean-architecture**     | Layered ports-and-adapters architecture for Bash 4.3+ scripts and multi-file projects.                                      |
| **bx-bash-reference**              | Complete reference for GNU Bash 5.3 covering syntax, builtins, expansions, redirections, and features.                      |
| **bx-enhance-code-quality**        | Scores a project 0-10, identifies issues by severity, and walks through fixes.                                              |
| **bx-humanize-de**                 | Removes signs of AI-generated writing from German text. Detects and fixes 32 patterns.                                      |
| **bx-humanize-en**                 | Removes signs of AI-generated writing from English text. Based on Wikipedia's "Signs of AI writing" guide (35 patterns).    |
| **bx-performance**                 | Python performance review — caching opportunities, uncompiled regex, hot spot profiling, optimization validation.           |
| **bx-plan-executor**               | Executes a written implementation plan in batches with review checkpoints between batches.                                  |
| **bx-plan-writer**                 | Creates comprehensive implementation plans from specs or requirements, before touching code.                                |
| **bx-proxmox**                     | Proxmox VE 9.1.2 reference — installation, clusters, VMs, containers, storage, Ceph, SDN, firewall, HA, backups, and CLI.   |
| **bx-python-clean-architecture**   | Typed Python ports-and-adapters architecture with domain-driven design, UoW, outbox, and idempotency patterns.              |
| **bx-python-libraries-to-use**     | Standardized library choices for Python projects ensuring consistency and enforcing preferred tools.                        |
| **bx-rpyc**                        | RPyC reference — transparent remote procedure calls, distributed computing, netref proxies, and async patterns.             |
| **bx-skill-writer**                | TDD-based skill documentation authoring — creating, editing, structuring, testing, and deploying SKILL.md files.            |
| **bx-textual**                     | Textual TUI framework documentation reference — API docs, guides, CSS reference, FAQ, and widget catalog.                   |
| **bx-uv**                          | Complete reference for uv (v0.10.2) — project setup, dependency management, lockfiles, tools, Docker, CI/CD, and migration. |
| **bx_review_anal_sub_perf**        | Performance analysis sub-agent — profiling, benchmarking, hot spot identification, before/after comparison.                 |
| **force-using-skills**             | Establishes that skills must be invoked whenever applicable before any response.                                            |
| **md-table-formatting**            | Markdown table creation, editing, and reformatting with proper column alignment.                                            |
| **systematic-debugging**           | Root-cause-first debugging methodology. Requires finding root cause before attempting fixes.                                |
| **test-driven-development**        | Write tests first, watch them fail, then write minimal code to pass.                                                        |
| **verification-before-completion** | Requires running verification commands and confirming output before making any success claims.                              |
