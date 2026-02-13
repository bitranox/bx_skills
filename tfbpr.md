Test, Fix, Bump, Push, Release — full release pipeline.

Execute the following steps sequentially. Do NOT skip steps. Stop and ask the user if any decision requires human judgement.

If any `make` command prompts to update the Makefile, approve it.

---

## Step 0 — Fix Mode

Before starting, ask the user to choose a fix mode:

1. **auto** — Fix everything automatically, no questions asked.
2. **ask-big** — Fix small/obvious issues automatically; ask for approval on large or risky changes.
3. **ask-per-scope** — Group errors by scope (lint, types, tests, CI, etc.) and ask for approval on each group before applying fixes.

Remember their choice as the **fix mode** for the rest of the pipeline.

## Step 1 — Run Tests

Run `make test` and capture the full output.

## Step 2 — Fix All Errors

If `make test` failed:
- Analyze every error in the output (lint, type-check, unit tests, shellcheck, etc.).
- If fix mode is **auto**: fix all errors directly.
- If fix mode is **ask-big**: fix small/obvious errors directly; for large or risky changes, present a summary and proposed fix to the user and wait for approval.
- If fix mode is **ask-per-scope**: group errors by scope (lint, types, tests, etc.), present each group with proposed fixes, and wait for approval before applying each group.
- Re-run `make test` to confirm all errors are resolved.
- Repeat until `make test` passes with zero failures.

If `make test` passed, proceed to the next step.

## Step 3 — Determine Semver Bump Level

Analyze all changes since the last released version:
- Run `git log $(git describe --tags --abbrev=0)..HEAD --oneline` to list commits since the last tag.
- Run `git diff $(git describe --tags --abbrev=0)..HEAD --stat` to see which files changed.
- Apply semver rules:
  - **major** — breaking API changes, removed public functions/classes, changed signatures
  - **minor** — new features, new public API, new modules, backward-compatible additions
  - **patch** — bug fixes, documentation, internal refactors, dependency updates, CI/CD changes

## Step 4 — Bump Version

Run the appropriate command based on the confirmed semver level:
- `make bump-patch` for patch
- `make bump-minor` for minor
- `make bump-major` for major

## Step 5 — Update Changelog

Update `CHANGELOG.md` with the important changes since the last version:
- Group changes under the new version heading with the current date.
- Categorize entries (Added, Changed, Fixed, Removed, etc.) following Keep a Changelog format.
- Be concise but cover all user-visible and developer-visible changes.

## Step 6 — Create Commit Message

Compose a meaningful commit message that:
- Summarizes the version bump and key changes.
- References the new version number.
- Follows conventional commit style if the project uses it.


## Step 7 — Push

Run `make push ARGS="<approved commit message>"` to run tests, commit, and push to the remote.

## Step 8 — Monitor GitHub CI

After pushing:
- Run `gh run list --limit 1` to find the latest workflow run.
- Run `gh run watch <run-id>` to monitor it until completion.
- If the run **succeeds**, proceed to Step 9.
- If the run **fails**:
  - Run `gh run view <run-id> --log-failed` to get failure details.
  - If fix mode is **auto**: fix all errors directly.
  - If fix mode is **ask-big**: fix small/obvious errors directly; for large or risky changes, present a summary and wait for approval.
  - If fix mode is **ask-per-scope**: group errors by scope, present each group with proposed fixes, and wait for approval per group.
  - Go back to **Step 5** (update changelog if the fix is meaningful, re-commit, re-push).

## Step 9 — Release

Once GitHub CI is green:
- Run `make release` to create the version tag and GitHub release.

## Step 10 — Monitor Release CI

After releasing:
- Run `gh run list --limit 1` to find the release workflow run.
- Run `gh run watch <run-id>` to monitor it until completion.
- If the run **succeeds**, report the release URL and confirm completion.
- If the run **fails**:
  - Run `gh run view <run-id> --log-failed` to get failure details.
  - If fix mode is **auto**: fix all errors directly.
  - If fix mode is **ask-big**: fix small/obvious errors directly; for large or risky changes, present a summary and wait for approval.
  - If fix mode is **ask-per-scope**: group errors by scope, present each group with proposed fixes, and wait for approval per group.
  - Go back to **Step 5** (update changelog, re-commit, re-push, re-release).
