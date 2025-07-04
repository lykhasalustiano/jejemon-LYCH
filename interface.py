class ConsoleInterface:
    COLORS = {
        'reset': '\033[0m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m'
    }

    @classmethod
    def display(cls, original, normalized):
        border = "=" * 50
        print(f"\n{border}")
        print(f"{cls.COLORS['red']}Original: {cls.COLORS['reset']}{original}")
        print(f"{cls.COLORS['green']}Normalized: {cls.COLORS['reset']}{normalized}")
        print(border)

    @classmethod
    def show_history(cls):
        from memory import TranslationMemory
        history = TranslationMemory.load()
        print("\nTranslation History:")
        for i, entry in enumerate(history[-5:], 1):
            print(f"{i}. {entry['original']} → {entry['normalized']}")
