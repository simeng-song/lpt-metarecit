from __future__ import annotations
import re
from pathlib import Path

RAW_PATH = Path("data/raw/corpus_cn_raw.txt")
CLEAN_PATH = Path("data/processed/corpus_cn_clean.txt")
DOCS_PATH = Path("data/processed/docs_cn.txt")


def load_raw() -> str:
    text = RAW_PATH.read_text(encoding="utf-8", errors="ignore")
    return text


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text

def main():
    raw = load_raw()
    clean = clean_text(raw)

    CLEAN_PATH.write_text(clean, encoding="utf-8")

if __name__ == "__main__":
    main()

