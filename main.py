from analysis import token_area
from interface import display, show_history
from memory import save_translation

def main():
    print("=== Jejemon Translator ===")
    print("Type 'history' to view last 5 translations")
    print("Type 'exit' to quit\n")

    while True:
        text = input("Enter text: ").strip()
        
        if text.lower() == 'exit':
            break
        elif text.lower() == 'history':
            show_history()
            continue

        tokenized = token_area(text)
        save_translation(text, tokenized)
        display(text, tokenized)

if __name__ == "__main__":
    main()
