import json
from pathlib import Path
import re
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

INPUT_FILE = "corpus_clean.json"
OUTPUT_GLOBAL = "tfidf_top.txt"
CONTENT_FIELD = "full_content"
TITLE_FIELD = "title"

TOP_K_GLOBAL = 80

STOPWORDS = {
    "的", "了", "和", "与", "及", "在", "对", "为", "是", "着", "也", "都", "同", "有", "好", "并",
    "10", "08", "cn", "n1", "html", "我们", "他们", "这些", "那些", "一个", "这个", "那个",
    "title", "full", "从", "到", "让", "下", "url", "http", "cpc", "通过", "更加", "更",
    "年", "月", "中", "以", "等", "日", "将", "要", "上", "有", "多", "大", "people", 
    "com", "summary"
}

RE_CHINESE = re.compile(r"^[\u4e00-\u9fa5]+$")
PUNCTUATION = set(".,;!?！？。()（）[]【】、《》\"“”‘’:：/—-·… ")

def load_docs(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    metas = []
    for idx, item in enumerate(data):
        text = item.get(CONTENT_FIELD, "") or ""
        title = item.get(TITLE_FIELD, "") if TITLE_FIELD else ""
        if not text.strip():
            continue
        docs.append(text)
        metas.append({
            "idx": idx,
            "title": title,
        })
    return docs, metas


def clean_tokenizer(text):
    tokens = jieba.lcut(text)
    cleaned = []

    for tok in tokens:
        tok = tok.strip()
        if not tok:
            continue

        if tok in STOPWORDS:
            continue

        if tok in PUNCTUATION:
            continue

        if "�" in tok:
            continue

        if tok.isdigit():
            continue

        if re.fullmatch(r"[A-Za-z]+", tok):
            continue

        if RE_CHINESE.match(tok):
            cleaned.append(tok)
            continue

        continue

    return cleaned

def main():
    if not Path(INPUT_FILE).exists():
        raise FileNotFoundError(INPUT_FILE)

    docs, metas = load_docs(INPUT_FILE)
    print(f"Loaded {len(docs)} documents.")

    vectorizer = TfidfVectorizer(
        tokenizer=clean_tokenizer,
        token_pattern=None,
        max_df=0.9,
        min_df=2
    )
    X = vectorizer.fit_transform(docs)
    vocab = vectorizer.get_feature_names_out()

    import numpy as np
    mean_tfidf = X.mean(axis=0).A1
    idx_sorted = np.argsort(mean_tfidf)[::-1]

    with open(OUTPUT_GLOBAL, "w", encoding="utf-8") as f:
        for i in idx_sorted[:TOP_K_GLOBAL]:
            f.write(f"{vocab[i]}\t{mean_tfidf[i]:.6f}\n")

    print("Fini dans :", OUTPUT_GLOBAL)

if __name__ == "__main__":
    main()
