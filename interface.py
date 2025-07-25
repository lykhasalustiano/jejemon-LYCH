from memory import load_history
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

custom_theme = Theme({
    "title": "bold yellow",
    "border": "yellow",
    "jejemon": "bold red",
    "translated": "bold orange1",
})

console = Console(theme=custom_theme)

FIXED_WIDTH = 50  # Width of the display

def display(original, normalized):
    # Print centered title between equal signs
    border_line = "=" * FIXED_WIDTH
    centered_title = "JEJEMON TRANSLATOR".center(FIXED_WIDTH)

    console.print(f"\n{border_line}")
    console.print(f"[title]{centered_title}[/title]")
    console.print(f"{border_line}\n")

    # Jejemon panel
    jejemon_panel = Panel.fit(
        Text(original, style="jejemon"),
        title="Jejemon Text",
        border_style="red",
        width=FIXED_WIDTH
    )

    # Translated panel
    translated_panel = Panel.fit(
        Text(normalized, style="translated"),
        title="Translated",
        border_style="orange1",
        width=FIXED_WIDTH
    )

    console.print(jejemon_panel)
    console.print(translated_panel)

def show_history():
    history = load_history()
    console.print("\n[bold yellow]Translation History:[/bold yellow]")
    if not history:
        console.print("[italic]No history found.[/italic]")
    for i, entry in enumerate(history[-5:], 1):
        console.print(f"[{i}] [red]{entry['original']}[/red] → [orange1]{entry['normalized']}[/orange1]")
