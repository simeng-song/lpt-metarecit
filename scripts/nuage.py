import json
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba

os.chdir("/Users/songsimeng/INALCOM2/lpt")

with open("data/processed/corpus_clean.json", "r", encoding="utf-8") as f:
    data = json.load(f)

corpus_texts = []

for item in data:
    parts = [
        item.get("title", ""),
        item.get("summary", ""),
        item.get("full_content", "")
    ]
    combined = "\n".join([p for p in parts if p])
    corpus_texts.append(combined)

print("nb d'articles：", len(corpus_texts))
print(corpus_texts[0][:300])  

all_text = "\n".join(corpus_texts)

STOPWORDS = {
    "的", "了", "和", "与", "及", "在", "对", "为", "是", "着", "也", "都", "同", "有", "好", "并", "10", "08","cn", "n1", "html",
    "我们", "他们", "这些", "那些", "一个", "这个", "那个", "title", "full", "从", "到", "让", "下", "url", "http", "cpc",
    "通过", "更加", "更", "年", "月", "中", "以", "等", "日", "将", "要", "上", "有", "多", "大", "people", "com", "summary"
}

words = [w for w in jieba.lcut(all_text) if w.strip() and w not in STOPWORDS]


wordcloud = WordCloud(
    font_path="/System/Library/Fonts/PingFang.ttc",  
    width=1200,
    height=800,
    background_color="white",
    collocations=False
).generate(" ".join(words))

plt.figure(figsize=(10,6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
wordcloud.to_file("resultats/nuage.png")

