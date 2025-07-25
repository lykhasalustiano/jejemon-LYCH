import json

def convert_json_to_txt(json_path, output_txt_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
        for word in data:
            txt_file.write(f"{word}\n")  

    print(f"✅ Converted and saved to {output_txt_path}")

# === Example usage ===
convert_json_to_txt(
    json_path='lexicon/corpora_words.json',
    output_txt_path='lexicon/clean_words.txt'
)
