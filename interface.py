from memory import load_history

COLORS = {
    'reset': '\033[0m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m'
}

def display(original, normalized):
    border = "=" * 50
    print(f"\n{border}")
    print(f"{COLORS['red']}Original: {COLORS['reset']}{original}")
    print(f"{COLORS['green']}Translated: {COLORS['reset']}{normalized}")
    print(border)

def show_history():
    history = load_history()
    print("\nTranslation History:")
    for i, entry in enumerate(history[-5:], 1):  # last 5 entries
        print(f"{i}. {entry['original']} → {entry['normalized']}")
