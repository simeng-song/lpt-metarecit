from pathlib import Path

RAW_PATH = Path("data/raw/corpus_cn_raw.txt")

def main():
    text = RAW_PATH.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    print(f"caractères : {len(text)}")
    print(f"lignes : {len(lines)}")

    key = "人类命运共同体"
    count = text.count(key)
    print(f"\n「{key}」fréquence：{count}")

    for i, line in enumerate(lines[:10], start=1):
        print(f"{i:02d}: {line}")


if __name__ == "__main__":
    main()
