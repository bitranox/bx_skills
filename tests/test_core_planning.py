"""Tests for bx_skills.core.get_active_targets and build_plans."""

from __future__ import annotations

from pathlib import Path

import pytest

from bx_skills.core import (
    CLITarget,
    Scope,
    SkillAction,
    SkillInfo,
    build_plans,
    get_active_targets,
)

pytestmark = pytest.mark.os_agnostic


# ── get_active_targets ───────────────────────────────────────────────────────


def test_project_only_target_excluded_from_user_scope(sample_target: CLITarget, project_only_target: CLITarget) -> None:
    pairs = get_active_targets([sample_target, project_only_target], [Scope.USER])
    targets_in_pairs = [t.name for t, _ in pairs]
    assert "TestCLI" in targets_in_pairs
    assert "ProjectOnlyCLI" not in targets_in_pairs


def test_empty_user_path_excluded_from_user_scope() -> None:
    target = CLITarget(
        name="NoUser",
        user_path_tpl="",
        project_path_tpl=".nouse/skills/{skill}",
        project_only=False,
        detect_dir=".nouse",
    )
    pairs = get_active_targets([target], [Scope.USER])
    assert pairs == []


def test_both_scopes_produce_two_pairs(sample_target: CLITarget, fake_home: Path, fake_cwd: Path) -> None:
    pairs = get_active_targets([sample_target], [Scope.USER, Scope.PROJECT])
    assert len(pairs) == 2
    scopes = [s for _, s in pairs]
    assert Scope.USER in scopes
    assert Scope.PROJECT in scopes


def test_empty_targets_returns_empty() -> None:
    assert get_active_targets([], [Scope.USER, Scope.PROJECT]) == []


def test_empty_scopes_returns_empty(sample_target: CLITarget) -> None:
    assert get_active_targets([sample_target], []) == []


def test_project_only_in_project_scope_included(project_only_target: CLITarget) -> None:
    pairs = get_active_targets([project_only_target], [Scope.PROJECT])
    assert len(pairs) == 1
    assert pairs[0] == (project_only_target, Scope.PROJECT)


# ── get_active_targets: CWD == HOME guard ────────────────────────────────────


def test_project_scope_excluded_when_cwd_is_home(
    sample_target: CLITarget, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """When CWD == HOME and templates match, PROJECT scope is redundant."""
    home = tmp_path / "same"
    home.mkdir()
    monkeypatch.setattr(Path, "home", staticmethod(lambda: home))
    monkeypatch.setattr(Path, "cwd", staticmethod(lambda: home))

    pairs = get_active_targets([sample_target], [Scope.USER, Scope.PROJECT])
    scopes = [s for _, s in pairs]
    assert Scope.USER in scopes
    assert Scope.PROJECT not in scopes


def test_project_scope_included_when_cwd_is_not_home(sample_target: CLITarget, fake_home: Path, fake_cwd: Path) -> None:
    """When CWD != HOME, both scopes are valid."""
    pairs = get_active_targets([sample_target], [Scope.USER, Scope.PROJECT])
    scopes = [s for _, s in pairs]
    assert Scope.USER in scopes
    assert Scope.PROJECT in scopes


def test_project_only_target_kept_when_cwd_is_home(
    project_only_target: CLITarget, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """project_only targets (e.g. Windsurf) keep PROJECT even when CWD == HOME."""
    home = tmp_path / "same"
    home.mkdir()
    monkeypatch.setattr(Path, "home", staticmethod(lambda: home))
    monkeypatch.setattr(Path, "cwd", staticmethod(lambda: home))

    pairs = get_active_targets([project_only_target], [Scope.PROJECT])
    assert len(pairs) == 1
    assert pairs[0] == (project_only_target, Scope.PROJECT)


def test_mixed_targets_cwd_is_home(
    sample_target: CLITarget,
    project_only_target: CLITarget,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """With mixed targets and CWD == HOME: normal target loses PROJECT, project_only keeps it."""
    home = tmp_path / "same"
    home.mkdir()
    monkeypatch.setattr(Path, "home", staticmethod(lambda: home))
    monkeypatch.setattr(Path, "cwd", staticmethod(lambda: home))

    pairs = get_active_targets([sample_target, project_only_target], [Scope.USER, Scope.PROJECT])
    # sample_target: only USER (PROJECT filtered)
    # project_only_target: only PROJECT (USER filtered by project_only)
    assert (sample_target, Scope.USER) in pairs
    assert (sample_target, Scope.PROJECT) not in pairs
    assert (project_only_target, Scope.PROJECT) in pairs
    assert (project_only_target, Scope.USER) not in pairs


# ── build_plans ──────────────────────────────────────────────────────────────


def test_skip_action_produces_no_plans(sample_skill: SkillInfo, sample_target: CLITarget, fake_home: Path) -> None:
    plans = build_plans(
        [sample_skill],
        {sample_skill.dir_name: SkillAction.SKIP},
        [sample_target],
        [Scope.USER],
    )
    assert plans == []


def test_keep_action_produces_no_plans(sample_skill: SkillInfo, sample_target: CLITarget, fake_home: Path) -> None:
    plans = build_plans(
        [sample_skill],
        {sample_skill.dir_name: SkillAction.KEEP},
        [sample_target],
        [Scope.USER],
    )
    assert plans == []


def test_install_action_produces_plan(sample_skill: SkillInfo, sample_target: CLITarget, fake_home: Path) -> None:
    plans = build_plans(
        [sample_skill],
        {sample_skill.dir_name: SkillAction.INSTALL},
        [sample_target],
        [Scope.USER],
    )
    assert len(plans) == 1
    assert plans[0].action == SkillAction.INSTALL
    assert plans[0].skill is sample_skill


def test_update_action_produces_plan(sample_skill: SkillInfo, sample_target: CLITarget, fake_home: Path) -> None:
    plans = build_plans(
        [sample_skill],
        {sample_skill.dir_name: SkillAction.UPDATE},
        [sample_target],
        [Scope.USER],
    )
    assert len(plans) == 1
    assert plans[0].action == SkillAction.UPDATE


def test_uninstall_only_when_installed(sample_skill: SkillInfo, sample_target: CLITarget, fake_home: Path) -> None:
    # Not installed → no uninstall plan
    plans = build_plans(
        [sample_skill],
        {sample_skill.dir_name: SkillAction.UNINSTALL},
        [sample_target],
        [Scope.USER],
    )
    assert plans == []


def test_uninstall_when_installed_produces_plan(
    sample_skill: SkillInfo, sample_target: CLITarget, fake_home: Path
) -> None:
    # Pre-install the skill
    dest = fake_home / ".testcli" / "skills" / "alpha-skill"
    dest.mkdir(parents=True)
    (dest / "SKILL.md").write_text("installed", encoding="utf-8")

    plans = build_plans(
        [sample_skill],
        {sample_skill.dir_name: SkillAction.UNINSTALL},
        [sample_target],
        [Scope.USER],
    )
    assert len(plans) == 1
    assert plans[0].action == SkillAction.UNINSTALL


def test_missing_action_defaults_to_skip(sample_skill: SkillInfo, sample_target: CLITarget, fake_home: Path) -> None:
    plans = build_plans(
        [sample_skill],
        {},  # no action entry for this skill
        [sample_target],
        [Scope.USER],
    )
    assert plans == []
