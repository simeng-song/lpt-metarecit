import pandas as pd

DOC_CSV = "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/lda_doc_topics.csv"

df = pd.read_csv(DOC_CSV)

topic_id = 1
top = (df[df["main_topic"] == topic_id]
       .sort_values("main_prob", ascending=False)
       .head(20))

top.to_csv("/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/topic1_top_docs.csv",
           index=False, encoding="utf-8-sig")

print(top[["doc_index", "main_prob", "title", "n_sentences"]].head(10))
print("[OK] Export -> topic1_top_docs.csv")
