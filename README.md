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
