"""Textual TUI application for installing AI coding assistant skills."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import ClassVar

from rich.text import Text
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widgets import (
    DataTable,
    Footer,
    Label,
    RichLog,
    SelectionList,
    Static,
)
from textual.widgets.selection_list import Selection
from textual.worker import get_current_worker

from bx_skills.core import (
    CLI_TARGETS,
    CLITarget,
    InstallPlan,
    Scope,
    SkillAction,
    SkillInfo,
    SkillsError,
    build_plans,
    check_installed,
    discover_skills,
    get_active_targets,
    install_skill,
    uninstall_skill,
)
from bx_skills.theme import CATPPUCCIN_MOCHA, SUBTEXT0, SURFACE1, TEAL

# ── Cell state for DataTable ─────────────────────────────────────────────────


class CellState(Enum):
    """State of a single cell in the skills DataTable."""

    SELECT = "X"  # will install (new) or update (installed)
    KEEP = "-"  # installed, will NOT be updated
    SKIP = " "  # not installed, will NOT be installed
    DELETE = "D"  # will be deleted


# ── CSS ───────────────────────────────────────────────────────────────────────

APP_CSS = (
    """\
Screen {
    background: $background;
}

.screen-title {
    dock: top;
    width: 100%;
    text-align: center;
    padding: 1 0;
    text-style: bold;
    color: $primary;
    background: $panel;
}

.screen-subtitle {
    dock: top;
    width: 100%;
    text-align: center;
    padding: 0 0 1 0;
    color: """
    + SUBTEXT0
    + """;
    background: $panel;
}

.screen-body {
    padding: 1 2;
}

.error-label {
    color: $error;
    text-style: bold;
    padding: 1 2;
    display: none;
}

.error-label.visible {
    display: block;
}

.nothing-label {
    color: $warning;
    text-style: bold;
    padding: 1 2;
    display: none;
}

.nothing-label.visible {
    display: block;
}

SelectionList {
    background: $background;
    height: 1fr;
}

SelectionList:focus > .option-list--option-highlighted {
    background: """
    + SURFACE1
    + """;
    color: $foreground;
    text-style: bold;
}

SelectionList > .option-list--option-highlighted {
    background: $surface;
    color: $foreground;
}

SelectionList > .option-list--option-hover {
    background: $surface;
}

DataTable {
    background: $background;
    height: 1fr;
}

DataTable:focus > .datatable--cursor {
    background: """
    + SURFACE1
    + """;
    color: $foreground;
    text-style: bold;
}

DataTable > .datatable--header {
    background: $panel;
    color: $primary;
    text-style: bold;
}

HelpScreen {
    align: center middle;
}

HelpScreen .help-container {
    width: 72;
    max-height: 80%;
    background: $surface;
    border: thick $primary;
    padding: 1 2;
}

HelpScreen .help-title {
    text-align: center;
    text-style: bold;
    color: $primary;
    padding-bottom: 1;
}

HelpScreen .help-body {
    color: $foreground;
}

RichLog {
    padding: 1 2;
}

.summary-line {
    dock: bottom;
    height: 1;
    padding: 0 2;
    text-style: bold;
    color: """
    + TEAL
    + """;
    background: $panel;
}
"""
)


# ── HelpScreen ────────────────────────────────────────────────────────────────

HELP_TEXT = """\
[bold]Navigation[/bold]
  Enter       Next step
  Escape      Previous step / close help
  q           Quit

[bold]Targets[/bold]
  Multiple CLIs can be selected simultaneously.
  Detected CLIs are pre-selected based on ~/.<cli-dir>/ existence.

[bold]Skills Screen[/bold]
  DataTable with User and Project scope columns.
  Space       Cycle cell state under cursor
  a           Select all (set all to X)
  n           Reset to defaults

[bold]Cell Symbols[/bold]
  X           Will install (new) or update (installed)  [green]
  -           Installed, will NOT be updated             [dim]
  (blank)     Not installed, will NOT be installed
  D           Will be deleted                            [red]

[bold]Cycling[/bold]
  Installed skills:  X -> - -> D -> X
  New skills:        (blank) -> X -> (blank)
"""


class HelpScreen(ModalScreen[None]):
    """Modal help overlay."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("escape", "dismiss", "Close"),
        Binding("question_mark", "dismiss", "Close", key_display="?"),
    ]

    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="help-container"):
            yield Static("Skills Installer \u2014 Help", classes="help-title")
            yield Static(HELP_TEXT, classes="help-body")


# ── Typed base screen ────────────────────────────────────────────────────────


class InstallerScreen(Screen):
    """Base screen with typed access to SkillsInstallerApp."""

    @property
    def installer(self) -> SkillsInstallerApp:
        """Return the app instance typed as SkillsInstallerApp."""
        return self.app  # type: ignore[return-value]


# ── Screen 1: TargetsScreen ──────────────────────────────────────────────────


class TargetsScreen(InstallerScreen):
    """Select which CLI tools to install skills for."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("enter", "next", "Next", priority=True),
        Binding("escape", "quit_app", "Quit"),
        Binding("q", "quit_app", "Quit", show=False),
        Binding("question_mark", "help", "Help", key_display="?"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("Select Target CLIs", classes="screen-title")
        yield Static(
            "Choose which AI coding assistants to install skills for",
            classes="screen-subtitle",
        )

        selections: list[Selection[CLITarget]] = []
        for target in CLI_TARGETS:
            detected = (Path.home() / target.detect_dir).is_dir()
            path_display = target.project_path_tpl.rsplit("/{skill}", 1)[0] + "/"
            parts = [target.name, f" ({path_display})"]
            if detected:
                parts.append("  (detected)")
            if target.project_only:
                parts.append("  [project-level only]")
            label = "".join(parts)
            selections.append(Selection(label, target, initial_state=detected))

        yield SelectionList[CLITarget](*selections, id="targets-list")
        yield Label("", classes="error-label", id="targets-error")
        yield Footer()

    def action_next(self) -> None:
        sel_list = self.query_one("#targets-list", SelectionList)
        selected = list(sel_list.selected)
        error_label = self.query_one("#targets-error", Label)
        if not selected:
            error_label.update("Select at least one target CLI.")
            error_label.add_class("visible")
            return
        error_label.remove_class("visible")
        self.installer.selected_targets = selected
        self.app.push_screen(SkillsScreen())

    def action_quit_app(self) -> None:
        self.app.exit()

    def action_help(self) -> None:
        self.app.push_screen(HelpScreen())


# ── Screen 2: SkillsScreen ───────────────────────────────────────────────────

_SCOPE_COLUMNS: list[tuple[Scope, str]] = [(Scope.USER, "user"), (Scope.PROJECT, "project")]


class SkillsScreen(InstallerScreen):
    """Select skills to install/update/delete via a DataTable with per-scope columns."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("enter", "next", "Next", priority=True),
        Binding("escape", "go_back", "Back"),
        Binding("q", "quit_app", "Quit", show=False),
        Binding("space", "toggle_cell", "Toggle", priority=True),
        Binding("a", "select_all", "All", key_display="a"),
        Binding("n", "deselect_all", "None", key_display="n"),
        Binding("question_mark", "help", "Help", key_display="?"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._states: dict[tuple[str, Scope], CellState] = {}
        self._installed_at: dict[tuple[str, Scope], bool] = {}
        self._skill_order: list[str] = []
        self._user_col_active: bool = True
        self._project_col_active: bool = True

    def compose(self) -> ComposeResult:
        yield Static("Select Skills", classes="screen-title")
        yield Static(
            "Space: toggle  |  a: all  |  n: none  |  X=install  -=keep  D=delete  \u00b7=skip",
            classes="screen-subtitle",
        )
        yield DataTable(id="skills-table", cursor_type="cell")
        yield Label("", classes="nothing-label", id="nothing-label")
        yield Footer()

    def on_mount(self) -> None:
        skills: list[SkillInfo] = self.installer.skills
        targets: list[CLITarget] = self.installer.selected_targets
        active_pairs = get_active_targets(targets, [Scope.USER, Scope.PROJECT])
        self._user_col_active = any(s == Scope.USER for _, s in active_pairs)
        self._project_col_active = any(s == Scope.PROJECT for _, s in active_pairs)

        table = self.query_one("#skills-table", DataTable)
        table.add_column("Skill", key="skill", width=32)
        table.add_column("User", key="user", width=8)
        table.add_column("Project", key="project", width=8)
        table.add_column("Description", key="desc")

        for skill in skills:
            self._skill_order.append(skill.dir_name)
            for scope in (Scope.USER, Scope.PROJECT):
                installed = any(
                    check_installed(skill, t, scope) for t in targets if not (scope == Scope.USER and t.project_only)
                )
                self._installed_at[(skill.dir_name, scope)] = installed
                col_inactive = (scope == Scope.USER and not self._user_col_active) or (
                    scope == Scope.PROJECT and not self._project_col_active
                )
                if col_inactive:
                    self._states[(skill.dir_name, scope)] = CellState.SKIP
                elif installed:
                    self._states[(skill.dir_name, scope)] = CellState.SELECT
                else:
                    self._states[(skill.dir_name, scope)] = CellState.SKIP

            table.add_row(
                Text(skill.dir_name),
                self._render_cell(skill.dir_name, Scope.USER),
                self._render_cell(skill.dir_name, Scope.PROJECT),
                Text(skill.description, style="dim"),
                key=skill.dir_name,
                height=None,
            )

    def _render_cell(self, dir_name: str, scope: Scope) -> Text:
        """Return styled Rich Text for a cell based on its state."""
        if scope == Scope.USER and not self._user_col_active:
            return Text("\u00b7", style="dim", justify="center")
        if scope == Scope.PROJECT and not self._project_col_active:
            return Text("\u00b7", style="dim", justify="center")
        state = self._states.get((dir_name, scope), CellState.SKIP)
        if state == CellState.SELECT:
            return Text("X", style="bold green", justify="center")
        if state == CellState.KEEP:
            return Text("-", style="dim", justify="center")
        if state == CellState.DELETE:
            return Text("D", style="bold red", justify="center")
        return Text(" ", justify="center")

    def action_toggle_cell(self) -> None:
        """Cycle the cell state under the cursor."""
        table = self.query_one("#skills-table", DataTable)
        coord = table.cursor_coordinate
        col = coord.column
        if col not in (1, 2):
            return
        scope = Scope.USER if col == 1 else Scope.PROJECT
        if scope == Scope.USER and not self._user_col_active:
            return
        if scope == Scope.PROJECT and not self._project_col_active:
            return
        row = coord.row
        if row >= len(self._skill_order):
            return
        dn = self._skill_order[row]
        installed = self._installed_at.get((dn, scope), False)
        current = self._states.get((dn, scope), CellState.SKIP)
        if installed:
            cycle = [CellState.SELECT, CellState.KEEP, CellState.DELETE]
        else:
            cycle = [CellState.SKIP, CellState.SELECT]
        idx = cycle.index(current) if current in cycle else 0
        new_state = cycle[(idx + 1) % len(cycle)]
        self._states[(dn, scope)] = new_state
        col_key = "user" if col == 1 else "project"
        table.update_cell(dn, col_key, self._render_cell(dn, scope))

    def _to_skill_action(self, dir_name: str, scope: Scope) -> SkillAction:
        """Map a CellState to a SkillAction."""
        state = self._states.get((dir_name, scope), CellState.SKIP)
        installed = self._installed_at.get((dir_name, scope), False)
        if state == CellState.SELECT:
            return SkillAction.UPDATE if installed else SkillAction.INSTALL
        if state == CellState.KEEP:
            return SkillAction.KEEP
        if state == CellState.DELETE:
            return SkillAction.UNINSTALL
        return SkillAction.SKIP

    def action_next(self) -> None:
        has_actionable = any(
            self._to_skill_action(dn, scope) not in (SkillAction.KEEP, SkillAction.SKIP)
            for dn in self._skill_order
            for scope in (Scope.USER, Scope.PROJECT)
        )
        if not has_actionable:
            label = self.query_one("#nothing-label", Label)
            label.update("Nothing to do \u2014 select skills to install, update, or uninstall.")
            label.add_class("visible")
            return
        self.query_one("#nothing-label", Label).remove_class("visible")
        plans: list[InstallPlan] = []
        for scope in (Scope.USER, Scope.PROJECT):
            scope_actions = {dn: self._to_skill_action(dn, scope) for dn in self._skill_order}
            plans.extend(
                build_plans(
                    self.installer.skills,
                    scope_actions,
                    self.installer.selected_targets,
                    [scope],
                )
            )
        self.installer._plans = plans
        self.app.push_screen(ConfirmScreen())

    def action_select_all(self) -> None:
        table = self.query_one("#skills-table", DataTable)
        for dn in self._skill_order:
            for scope, col_key in _SCOPE_COLUMNS:
                if scope == Scope.USER and not self._user_col_active:
                    continue
                if scope == Scope.PROJECT and not self._project_col_active:
                    continue
                self._states[(dn, scope)] = CellState.SELECT
                table.update_cell(dn, col_key, self._render_cell(dn, scope))

    def action_deselect_all(self) -> None:
        table = self.query_one("#skills-table", DataTable)
        for dn in self._skill_order:
            for scope, col_key in _SCOPE_COLUMNS:
                if scope == Scope.USER and not self._user_col_active:
                    continue
                if scope == Scope.PROJECT and not self._project_col_active:
                    continue
                installed = self._installed_at.get((dn, scope), False)
                self._states[(dn, scope)] = CellState.KEEP if installed else CellState.SKIP
                table.update_cell(dn, col_key, self._render_cell(dn, scope))

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def action_quit_app(self) -> None:
        self.app.exit()

    def action_help(self) -> None:
        self.app.push_screen(HelpScreen())


# ── Screen 3: ConfirmScreen ──────────────────────────────────────────────────


class ConfirmScreen(InstallerScreen):
    """Review planned operations before executing."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("enter", "execute", "Execute"),
        Binding("escape", "go_back", "Back"),
        Binding("q", "quit_app", "Quit", show=False),
        Binding("question_mark", "help", "Help", key_display="?"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("Confirm Operations", classes="screen-title")
        yield Static(
            "Review changes below. Enter to execute, Escape to go back.",
            classes="screen-subtitle",
        )

        log = RichLog(id="confirm-log", highlight=True, markup=True)
        yield log
        yield Static("", classes="summary-line", id="summary-line")
        yield Footer()

    def on_mount(self) -> None:
        plans: list[InstallPlan] = self.installer._plans
        skills: list[SkillInfo] = self.installer.skills
        log = self.query_one("#confirm-log", RichLog)

        # Group by action type
        installs = [p for p in plans if p.action in (SkillAction.INSTALL, SkillAction.UPDATE)]
        uninstalls = [p for p in plans if p.action == SkillAction.UNINSTALL]

        # Count skills with no plans at all
        actionable_skills = {p.skill.dir_name for p in plans}
        keep_count = sum(1 for s in skills if s.dir_name not in actionable_skills)

        if installs:
            log.write("[bold]Will Install/Update:[/bold]")
            log.write("\u2500" * 40)
            self._write_grouped(log, installs)
            log.write("")

        if uninstalls:
            log.write("[bold red]Will Uninstall:[/bold red]")
            log.write("\u2500" * 40)
            self._write_grouped(log, uninstalls)
            log.write("")

        if keep_count:
            log.write(f"Unchanged: {keep_count} skills kept/skipped")
            log.write("")

        summary = f"Summary: {len(installs)} install(s), {len(uninstalls)} uninstall(s), {keep_count} unchanged"
        self.query_one("#summary-line", Static).update(summary)

    def _write_grouped(self, log: RichLog, plans: list[InstallPlan]) -> None:
        """Write plans grouped by (target, scope)."""
        groups: dict[str, list[InstallPlan]] = {}
        for p in plans:
            scope_label = "User" if p.scope == Scope.USER else "Project"
            base = "~/" if p.scope == Scope.USER else str(Path.cwd()) + "/"
            tpl = p.target.user_path_tpl if p.scope == Scope.USER else p.target.project_path_tpl
            path_base = tpl.rsplit("/{skill}", 1)[0] + "/"
            key = f"{p.target.name} \u00b7 {scope_label} ({base}{path_base})"
            groups.setdefault(key, []).append(p)

        for group_key, group_plans in groups.items():
            log.write(f"  [bold]{group_key}[/bold]")
            for p in group_plans:
                if p.action == SkillAction.INSTALL:
                    log.write(f"    [blue]\\[+][/blue] {p.skill.dir_name}/  [blue](new)[/blue]")
                elif p.action == SkillAction.UPDATE:
                    log.write(f"    [blue]\\[+][/blue] {p.skill.dir_name}/  [blue](update)[/blue]")
                elif p.action == SkillAction.UNINSTALL:
                    log.write(f"    [red]\\[-][/red] {p.skill.dir_name}/")

    def action_execute(self) -> None:
        self.app.push_screen(ResultsScreen())

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def action_quit_app(self) -> None:
        self.app.exit()

    def action_help(self) -> None:
        self.app.push_screen(HelpScreen())


# ── Screen 4: ResultsScreen ──────────────────────────────────────────────────


class ResultsScreen(InstallerScreen):
    """Execute plans and show progressive results."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("escape", "quit_app", "Quit"),
        Binding("q", "quit_app", "Quit", show=False),
        Binding("question_mark", "help", "Help", key_display="?"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("Executing...", classes="screen-title", id="results-title")
        yield RichLog(id="results-log", highlight=True, markup=True)
        yield Static("", classes="summary-line", id="results-summary")
        yield Footer()

    def on_mount(self) -> None:
        self._execute_plans()

    @work(thread=True)
    def _execute_plans(self) -> None:
        worker = get_current_worker()
        plans: list[InstallPlan] = self.installer._plans
        log = self.query_one("#results-log", RichLog)

        succeeded = 0
        failed = 0

        for plan in plans:
            if worker.is_cancelled:
                break

            scope_label = "User" if plan.scope == Scope.USER else "Project"
            desc = f"{plan.skill.dir_name} \u2192 {plan.target.name} \u00b7 {scope_label}"

            try:
                if plan.action == SkillAction.UNINSTALL:
                    uninstall_skill(plan)
                    self.app.call_from_thread(
                        log.write,
                        f"[green]\\[OK][/green] {desc} (uninstalled)",
                    )
                elif plan.action == SkillAction.INSTALL:
                    install_skill(plan)
                    self.app.call_from_thread(
                        log.write,
                        f"[green]\\[OK][/green] {desc} (installed)",
                    )
                else:  # UPDATE
                    install_skill(plan)
                    self.app.call_from_thread(
                        log.write,
                        f"[green]\\[OK][/green] {desc} (updated)",
                    )
                succeeded += 1
            except SkillsError as exc:
                failed += 1
                self.app.call_from_thread(
                    log.write,
                    f"[red]\\[!!][/red] {desc} - {exc}",
                )

        summary = f"{succeeded} succeeded, {failed} failed"
        self.app.call_from_thread(
            self.query_one("#results-title", Static).update,
            "Complete",
        )
        self.app.call_from_thread(
            self.query_one("#results-summary", Static).update,
            summary,
        )

    def action_quit_app(self) -> None:
        self.app.exit()

    def action_help(self) -> None:
        self.app.push_screen(HelpScreen())


# ── App ───────────────────────────────────────────────────────────────────────


class SkillsInstallerApp(App):
    """TUI for installing AI coding assistant skills."""

    TITLE = "Skills Installer"
    SUB_TITLE = "AI Coding Assistant Skills"
    CSS = APP_CSS

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("q", "quit", "Quit", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        # State — populated by screens
        self.skills: list[SkillInfo] = []
        self.selected_targets: list[CLITarget] = []
        self._plans: list[InstallPlan] = []

    def on_mount(self) -> None:
        self.register_theme(CATPPUCCIN_MOCHA)
        self.theme = "catppuccin-mocha"

        self.skills = discover_skills()
        if not self.skills:
            self.notify(
                "No skills found in catalog_skills. Check your installation.",
                severity="error",
                timeout=5,
            )
            self.exit()
            return

        self.push_screen(TargetsScreen())


def main() -> None:
    """Entry point for the bx-skills CLI."""
    app = SkillsInstallerApp()
    app.run()


if __name__ == "__main__":
    main()
