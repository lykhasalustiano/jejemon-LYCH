# from memory import load_history

# COLORS = {
#     'reset': '\033[0m',
#     'red': '\033[91m',
#     'green': '\033[92m',
#     'yellow': '\033[93m',
#     'blue': '\033[94m'
# }

# def display(original, normalized):
#     border = "=" * 50
#     print(f"\n{border}")
#     print(f"{COLORS['red']}Original: {COLORS['reset']}{original}")
#     print(f"{COLORS['green']}Translated: {COLORS['reset']}{normalized}")
#     print(border)

# def show_history():
#     history = load_history()
#     print("\nTranslation History:")
#     for i, entry in enumerate(history[-5:], 1):  # last 5 entries
#         print(f"{i}. {entry['original']} → {entry['normalized']}")

from memory import load_history
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
from rich.align import Align
from shutil import get_terminal_size

custom_theme = Theme({
    "title": "bold yellow",
    "border": "yellow",
    "jejemon": "bold red",
    "translated": "bold orange1",
})

console = Console(theme=custom_theme)

def display(original, normalized):
    title_text = Text("JEJEMON TRANSLATOR", style="title")
    centered_title = Align.center(title_text)

    console.print("\n")
    console.print(centered_title)  
    console.print()

    jejemon_panel = Panel(Text(original, style="jejemon"), title="Jejemon Text", border_style="red")

    translated_panel = Panel(Text(normalized, style="translated"), title="Translated", border_style="orange1")

    console.print(jejemon_panel)
    console.print(translated_panel)

def show_history():
    history = load_history()
    console.print("\n[bold yellow]Translation History:[/bold yellow]")
    for i, entry in enumerate(history[-5:], 1):
        console.print(f"[{i}] {entry['original']} → {entry['normalized']}")
