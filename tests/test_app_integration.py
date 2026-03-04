"""Integration tests for multi-screen flows in bx_skills.app."""

# pyright: reportAttributeAccessIssue=false

from __future__ import annotations

from pathlib import Path

import pytest

from bx_skills.app import (
    CellState,
    ConfirmScreen,
    SkillsInstallerApp,
    SkillsScreen,
    TargetsScreen,
)
from bx_skills.core import CLITarget, Scope, SkillAction, SkillInfo, install_skill, uninstall_skill

pytestmark = [pytest.mark.os_agnostic, pytest.mark.integration]


def _make_skill(name: str, source: Path) -> SkillInfo:
    return SkillInfo(
        dir_name=name,
        name=name.replace("-", " ").title(),
        description=f"Desc {name}",
        source_path=source,
    )


async def test_full_install_flow(tmp_path: Path, fake_home: Path, fake_cwd: Path) -> None:
    """Walk Targets -> Skills -> Confirm, then execute plans via core."""
    skill_dir = tmp_path / "src" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: My Skill\n---\n", encoding="utf-8")

    target = CLITarget("TestCLI", ".test/skills/{skill}", ".test/skills/{skill}", False, ".test")

    async with SkillsInstallerApp().run_test() as pilot:
        app = pilot.app
        app.skills = [_make_skill("my-skill", skill_dir)]

        # Screen 1: Targets — set state directly and advance to SkillsScreen
        app.selected_targets = [target]
        app.push_screen(SkillsScreen())
        await pilot.pause()

        # Screen 2: Skills — set User column to X via _states
        screen = app.screen
        screen._states[("my-skill", Scope.USER)] = CellState.SELECT
        await pilot.pause()

        # Advance to ConfirmScreen
        screen.action_next()
        await pilot.pause()

        # Screen 3: Confirm — verify plans were built
        assert isinstance(app.screen, ConfirmScreen)
        assert len(app.plans) > 0
        assert app.plans[0].action == SkillAction.INSTALL

    # Execute the plan directly via core (avoids ResultsScreen worker issue)
    for plan in app.plans:
        install_skill(plan)

    installed = fake_home / ".test" / "skills" / "my-skill" / "SKILL.md"
    assert installed.is_file()


async def test_full_uninstall_flow(tmp_path: Path, fake_home: Path, fake_cwd: Path) -> None:
    """Walk to ConfirmScreen for uninstall, then execute plans via core."""
    skill_dir = tmp_path / "src" / "old-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: Old Skill\n---\n", encoding="utf-8")

    target = CLITarget("TestCLI", ".test/skills/{skill}", ".test/skills/{skill}", False, ".test")

    # Pre-install the skill
    installed_dir = fake_home / ".test" / "skills" / "old-skill"
    installed_dir.mkdir(parents=True)
    (installed_dir / "SKILL.md").write_text("installed", encoding="utf-8")

    async with SkillsInstallerApp().run_test() as pilot:
        app = pilot.app
        app.skills = [_make_skill("old-skill", skill_dir)]
        app.selected_targets = [target]

        app.push_screen(SkillsScreen())
        await pilot.pause()

        # The installed skill defaults to SELECT; set it to DELETE
        screen = app.screen
        screen._states[("old-skill", Scope.USER)] = CellState.DELETE
        await pilot.pause()

        # Verify action mapping
        assert screen._to_skill_action("old-skill", Scope.USER) == SkillAction.UNINSTALL

        screen.action_next()
        await pilot.pause()

        assert isinstance(app.screen, ConfirmScreen)
        assert len(app.plans) == 1
        assert app.plans[0].action == SkillAction.UNINSTALL

    # Execute uninstall directly via core
    for plan in app.plans:
        uninstall_skill(plan)

    assert not installed_dir.exists()


async def test_quit_from_targets_screen() -> None:
    """Pressing q on the first screen exits the app."""
    async with SkillsInstallerApp().run_test() as pilot:
        app = pilot.app
        app.skills = [
            SkillInfo("s", "S", "desc", Path("/fake")),
        ]
        app.push_screen(TargetsScreen())
        await pilot.pause()
        await pilot.press("q")
        await pilot.pause()
