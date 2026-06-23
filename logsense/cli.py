import time
from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .ai_analyzer import analyze_entries
from .log_parser import classify_line, parse_lines
from .storage import get_recent_events, init_db, save_event

app = typer.Typer(help="LogSense AI — scan or tail Linux logs and get AI root-cause analysis.")
console = Console()

def _render_analysis(analysis: dict) -> Panel:
    return Panel(
        f"[bold]Severity:[/bold] {analysis.get('severity')}\n"
        f"[bold]Root cause:[/bold] {analysis.get('root_cause')}\n"
        f"[bold]Suggested fix:[/bold] {analysis.get('suggested_fix')}\n\n"
        f"{analysis.get('summary')}",
        title="AI Analysis", border_style="cyan",
    )

@app.command()
def analyze(
    file: Path = typer.Argument(..., help="Path to the log file to analyze"),
    min_severity: int = typer.Option(40, help="Minimum severity (40=warning, 80=error, 100=fatal)"),
    no_ai: bool = typer.Option(False, "--no-ai", help="Skip AI, just show flagged lines"),
):
    """Analyze a static log file and surface the most important issues."""
    if not file.exists():
        console.print(f"[red]File not found: {file}[/red]")
        raise typer.Exit(1)
    lines = file.read_text(errors="ignore").splitlines()
    entries = [e for e in parse_lines(lines) if e.severity >= min_severity]
    if not entries:
        console.print("[green]No issues found above the severity threshold.[/green]")
        return
    table = Table(title=f"Flagged lines in {file.name}")
    table.add_column("Line")
    table.add_column("Severity")
    table.add_column("Text", overflow="fold")
    for e in entries[:30]:
        table.add_row(str(e.line_number), e.label, e.raw[:120])
    console.print(table)
    if not no_ai:
        console.print("\n[bold cyan]Running AI analysis...[/bold cyan]")
        analysis = analyze_entries([e.raw for e in entries])
        save_event(str(file), analysis, "\n".join(e.raw for e in entries))
        console.print(_render_analysis(analysis))

@app.command()
def watch(
    file: Path = typer.Argument(..., help="Log file to watch in real time"),
    min_severity: int = typer.Option(60, help="Minimum severity to count toward a batch"),
    batch_size: int = typer.Option(10, help="Flagged lines before calling AI"),
):
    """Tail a log file live and run AI analysis as issues accumulate."""
    if not file.exists():
        console.print(f"[red]File not found: {file}[/red]")
        raise typer.Exit(1)
    console.print(f"[cyan]Watching {file} — press Ctrl+C to stop[/cyan]")
    buffer = []
    with file.open("r", errors="ignore") as f:
        f.seek(0, 2)
        try:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                score, label = classify_line(line)
                if score >= min_severity:
                    console.print(f"[yellow]{label}[/yellow]: {line.strip()[:120]}")
                    buffer.append(line.strip())
                if len(buffer) >= batch_size:
                    console.print("[bold cyan]Analyzing batch with AI...[/bold cyan]")
                    analysis = analyze_entries(buffer)
                    save_event(str(file), analysis, "\n".join(buffer))
                    console.print(_render_analysis(analysis))
                    buffer = []
        except KeyboardInterrupt:
            console.print("\n[green]Stopped watching.[/green]")

@app.command()
def report(limit: int = typer.Option(20, help="Number of recent events to show")):
    """Show a summary of recently analyzed events from local history."""
    init_db()
    rows = get_recent_events(limit)
    if not rows:
        console.print("[yellow]No history yet. Run 'logsense analyze' first.[/yellow]")
        return
    table = Table(title="Recent LogSense Events")
    table.add_column("Time")
    table.add_column("Source")
    table.add_column("Severity")
    table.add_column("Summary", overflow="fold")
    for ts, source, severity, summary in rows:
        table.add_row(ts[:19], Path(source).name, severity, (summary or "")[:80])
    console.print(table)

def main():
    app()

if __name__ == "__main__":
    main()
