from __future__ import annotations
from pathlib import Path
import typer
from rich.console import Console
from rich.prompt import Prompt

from .store import SessionStore
from .observer import Observer
from .reporting import generate_report

app = typer.Typer(add_completion=False)
console = Console()
DEFAULT_BASE = Path("sessions")

@app.command()
def observe(
    session: str = typer.Option(..., "--session", "-s", help="Session name"),
    tail: list[Path] = typer.Option([], "--tail", help="Allowlisted log file to snapshot (repeatable)"),
):
    \"\"\"Interactive, read-only observation session.\"\"\"
    store = SessionStore(DEFAULT_BASE, session)
    obs = Observer(store, allow_tails=tail)

    store.append({"type": "session_start", "session": session, "tails": [str(p) for p in tail]})
    console.print(f"[bold]Session:[/bold] {session}")
    console.print("[dim]Type commands to run. Specials: :note <t>, :checkpoint <t>, :tail, :exit[/dim]\\n")

    while True:
        cmd = Prompt.ask("$")
        if not cmd:
            continue
        if cmd in (":exit", ":quit"):
            break
        if cmd.startswith(":note "):
            obs.note(cmd[len(":note "):].strip())
            console.print("[green]Noted.[/green]")
            continue
        if cmd.startswith(":checkpoint "):
            obs.checkpoint(cmd[len(":checkpoint "):].strip())
            console.print("[cyan]Checkpoint saved.[/cyan]")
            continue
        if cmd == ":tail":
            obs.tails()
            console.print("[yellow]Captured allowlisted log snapshots.[/yellow]")
            continue

        obs.command(cmd)
        console.print("[dim]Captured output (redacted) in timeline.[/dim]")

    store.append({"type": "session_end", "session": session})
    console.print("\\n[bold]Session ended.[/bold]")

@app.command()
def report(session: str = typer.Option(..., "--session", "-s", help="Session name")):
    \"\"\"Generate a Markdown report for a session.\"\"\"
    path = generate_report(DEFAULT_BASE, session)
    console.print(f"[bold]Report written:[/bold] {path}")

if __name__ == "__main__":
    app()
