# Claude Skills

A collection of Claude Code skills for software engineering workflows.

Skills prefixed with `bx-` are custom-built. The remaining skills are collected and adapted from community sources:

- [Vercel Agent Skills Directory](https://skills.sh)
- [Obra Superpowers Skill Library](https://skills.sh/obra/superpowers)
- [React/Next.js Performance Optimization](https://skills.sh/vercel-labs/agent-skills)
- [Writing Clearly and Concisely](https://skills.sh/softaworks/agent-tools)
- [Agentation](https://skills.sh/benjitaylor/agentation)
- [Tailwind Design System](https://skills.sh/wshobson/agents/tailwind)
- [UI/UX Pro Max](https://skills.sh/nextlevelbuilder/ui)

## Installation

### Linux / macOS

Clone the repo and run the sync script to install all skills at once:

```bash
# Clone to a permanent location
git clone https://github.com/bitranox/skills.git ~/repos/skills

# Install skills to ~/.claude/skills/
~/repos/skills/sync-skills.sh
```

To update later, just run the sync script again — it pulls the latest changes automatically:

```bash
~/repos/skills/sync-skills.sh
```

To add skills to a specific project instead:

```bash
cd ~/my-project
~/repos/skills/psync-skills.sh
```

### Windows (PowerShell 5.x+)

```powershell
# Clone to a permanent location
git clone https://github.com/bitranox/skills.git $env:USERPROFILE\repos\skills

# Install skills to ~/.claude/skills/
& $env:USERPROFILE\repos\skills\sync-skills.ps1
```

To update later:

```powershell
& $env:USERPROFILE\repos\skills\sync-skills.ps1
```

To add skills to a specific project instead:

```powershell
cd C:\my-project
& $env:USERPROFILE\repos\skills\psync-skills.ps1
```

## Sync Scripts

Two pairs of scripts are provided (Bash and PowerShell) to sync skill directories from this repo to their target locations.

### `sync-skills.sh` / `sync-skills.ps1` — Sync to user-level skills

Syncs all skill directories to `~/.claude/skills/`. On Linux, ownership is inherited from `$HOME`.

```bash
# Bash - from anywhere:
~/repos/skills/sync-skills.sh
```

```powershell
# PowerShell - from anywhere:
& $env:USERPROFILE\repos\skills\sync-skills.ps1
```

If you directly clone the repo into `~/.claude/skills/`, the script detects this and will only `git pull` without copying.

### `psync-skills.sh` / `psync-skills.ps1` — Sync to project-level skills

Syncs all skill directories to `<cwd>/.claude/skills/`. On Linux, ownership is inherited from the current working directory. Run this from the root of the project you want to add skills to.

```bash
# Bash - from a project directory:
cd ~/my-project
~/repos/skills/psync-skills.sh
```

```powershell
# PowerShell - from a project directory:
cd C:\my-project
& $env:USERPROFILE\repos\skills\psync-skills.ps1
```

All scripts auto-detect the repo location, run `git pull` first, and skip hidden directories (`.git`) and regular files.

## Auto-Update via Shell Alias

### Bash

Add the following to `~/.bashrc` to automatically sync skills before every `claude` session:

```bash
alias claude='~/repos/skills/sync-skills.sh && command claude'
```

Reload your shell or run `source ~/.bashrc` to activate.

For project-level skills instead:

```bash
alias claude='~/repos/skills/psync-skills.sh && command claude'
```

### PowerShell

Run this once to add the alias to your PowerShell profile:

```powershell
if (!(Test-Path $PROFILE)) { New-Item -Path $PROFILE -ItemType File -Force }
Add-Content -Path $PROFILE -Value @'

function Invoke-Claude {
    & $env:USERPROFILE\repos\skills\sync-skills.ps1
    & claude @args
}
Set-Alias -Name claude -Value Invoke-Claude
'@
```

Reload PowerShell or run `. $PROFILE` to activate.

For project-level skills instead, replace `sync-skills.ps1` with `psync-skills.ps1` in the snippet above.

All arguments are passed through, so `claude --help`, `claude -p "prompt"`, etc. work as expected.

## Skills

| Skill                              | Description                                                                                                                                                                    |
|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **brainstorming**                  | Turns ideas into fully formed designs and specs through collaborative dialogue. Explores user intent, requirements, and design before implementation.                          |
| **bx-bash-clean-architecture**     | Framework-agnostic structured Bash architecture with layered ports-and-adapters pattern. Keeps domain pure and testable with inner layers never calling outer layers directly. |
| **bx-bash-reference**              | Complete reference for GNU Bash 5.3 covering all shell syntax, builtins, variables, expansions, redirections, and features.                                                    |
| **bx-enhance-code-quality**        | Scores a project 0-10, identifies issues by severity, and walks through fixes while respecting prior decisions documented in CLAUDE.md.                                        |
| **bx-python-clean-architecture**   | Framework-agnostic typed Python architecture with layered ports-and-adapters pattern. Keeps inner layers pure and independent of infrastructure.                               |
| **bx-python-libraries-to-use**     | Standardized library choices for Python projects ensuring consistency and enforcing preferred tools over alternatives.                                                         |
| **bx-uv**                          | Complete reference for uv (v0.10.2) covering project setup, dependency management, virtual environments, Python versions, tools, Docker, CI/CD, and migration from pip.        |
| **executing-plans**                | Loads a written implementation plan and executes tasks in batches with checkpoints for architect review between batches.                                                       |
| **force-using-skills**             | Establishes that skills must be invoked whenever applicable. If there is even a 1% chance a skill applies, it must be used.                                                    |
| **systematic-debugging**           | Requires finding root cause before attempting fixes. Prevents random patches that mask underlying issues.                                                                      |
| **test-driven-development**        | Write tests first, watch them fail, then write minimal code to pass. Ensures tests validate the right behavior.                                                                |
| **using-superpowers**              | Establishes how to find and use skills, requiring Skill tool invocation before any response when skills apply to the task.                                                     |
| **verification-before-completion** | Requires running verification commands and confirming output before making any success claims. Evidence before assertions.                                                     |
| **writing-plans**                  | Creates comprehensive implementation plans with bite-sized tasks, documenting which files to touch, testing strategies, and how to verify completion.                          |
| **writing-skills**                 | Applies TDD to process documentation by writing test cases, watching them fail, creating skill documentation, and verifying agents comply.                                     |
