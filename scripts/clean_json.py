import json
import re

INPUT_FILE = "corpus.json"
OUTPUT_FILE = "corpus_clean.json"

TAG_PATTERN = re.compile(r"</?em>")


def clean_text(text):
    if not isinstance(text, str):
        return text
    return TAG_PATTERN.sub("", text)


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = []
    for item in data:
        new_item = {}
        for k, v in item.items():
            if isinstance(v, str):
                new_item[k] = clean_text(v)
            else:
                new_item[k] = v
        cleaned.append(new_item)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
