from analysis import normalize
from interface import ConsoleInterface
from memory import TranslationMemory

def main():
    print("=== Jejemon Translator ===")
    print("Type 'history' to view last 5 translations")
    print("Type 'exit' to quit\n")

    while True:
        text = input("Enter text: ").strip()
        
        if text.lower() == 'exit':
            break
        elif text.lower() == 'history':
            ConsoleInterface.show_history()
            continue

        normalized = normalize(text)
        TranslationMemory.save(text, normalized)
        ConsoleInterface.display(text, normalized)

if __name__ == "__main__":
    main()
