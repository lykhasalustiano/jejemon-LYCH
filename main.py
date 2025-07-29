import sys
from processor.core import enhanced_token_area  
from interface import display, show_history
from memory import save_translation

def clear_last_line():
    sys.stdout.write("\033[F")     
    sys.stdout.write("\033[K")   
    sys.stdout.flush()

def main():
    from rich.console import Console
    console = Console()

    console.print("[light]Type 'history' to view last 5 translations[/light]")
    console.print("[light]Type 'exit' to quit[/light]\n")

    while True:
        try:
            text = input("Enter text: ").strip()
            clear_last_line()  
        except (KeyboardInterrupt, EOFError):
            break

        if text.lower() == 'exit':
            break
        elif text.lower() == 'history':
            show_history()
            continue

        tokenized = enhanced_token_area(text)  
        save_translation(text, tokenized)
        display(text, tokenized)

if __name__ == "__main__":
    main()
