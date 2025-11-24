import json
import re
from pathlib import Path

INPUT_FILE = "corpus_clean.json"
OUTPUT_JSON = "contexte.json"

CONTENT_FIELD = "full_content"
TITLE_FIELD = "title"
KEYWORD = "新时代"

SPLIT_RE = re.compile(r"[。！？!?]")


def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_contexts(data):
    contexts = []
    for idx, item in enumerate(data):
        text = item.get(CONTENT_FIELD, "") or ""
        title = item.get(TITLE_FIELD, "") if TITLE_FIELD else ""
        if not text.strip():
            continue

        sentences = [s.strip() for s in SPLIT_RE.split(text) if s.strip()]
        for sent in sentences:
            if KEYWORD in sent:
                contexts.append({
                    "doc_index": idx,
                    "title": title,
                    "sentence": sent
                })
    return contexts


def main():
    if not Path(INPUT_FILE).exists():
        raise FileNotFoundError(INPUT_FILE)

    data = load_data(INPUT_FILE)
    contexts = extract_contexts(data)
    print(f"Found {len(contexts)} sentences with '{KEYWORD}'.")

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(contexts, f, ensure_ascii=False, indent=2)

    print("Saved to:", OUTPUT_JSON)


if __name__ == "__main__":
    main()