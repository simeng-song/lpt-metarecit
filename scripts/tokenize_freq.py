from __future__ import annotations
import re
from collections import Counter
from pathlib import Path

import jieba 

CLEAN_PATH = Path("data/processed/corpus_cn_clean.txt")
FREQ_PATH = Path("data/processed/freq_top50.csv")

STOPWORDS = {
    "的", "了", "和", "与", "及", "在", "对", "为", "是", "着", "也", "都",
    "我们", "他们", "这些", "那些", "一个", "这个", "那个",
    "通过", "更加", "进一步",
}

def tokenize(text: str) -> list[str]:
    tokens = [t.strip() for t in jieba.cut(text) if t.strip()]
    return tokens


def filter_tokens(tokens: list[str]) -> list[str]:
    out = []
    for t in tokens:
        if t in STOPWORDS:
            continue
        if len(t) == 1 and not re.match(r"[\u4e00-\u9fff]", t):
            continue
        out.append(t)
    return out


def main():
    text = CLEAN_PATH.read_text(encoding="utf-8")
    tokens = tokenize(text)
    tokens = filter_tokens(tokens)

    freq = Counter(tokens)
    top50 = freq.most_common(50)

    print(f"nb de tokens filtre{len(tokens)}")
    for w, c in top50:
        print(f"{w}\t{c}")

    with FREQ_PATH.open("w", encoding="utf-8") as f:
        f.write("token,freq\n")
        for w, c in top50:
            w_clean = w.replace(",", "，")
            f.write(f"{w_clean},{c}\n")

if __name__ == "__main__":
    main()
