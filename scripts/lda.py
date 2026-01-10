import json
import jieba
from collections import Counter, defaultdict
from gensim import corpora, models
import csv

# Fichier JSON : sous-corpus de phrases contenant « 新时代 »
INPUT_FILE = "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/contexte.json"

# Pivot étudié 
FOCUS = "新时代"

# Mots génériques institutionnels (bruit)
STOP_GENERIC = {
    "推动","构建","发展","促进","坚持","加强","提升","深化","推进","完善",
    "落实","实现","显著","持续","加快","一体化","水平","能力"
}
# Pour éviter que tous les topics soient dominés par les mêmes mots
STOP_FRAME = {
    "时代", "中国", "我们", "我国", "重要", "全面", "工作", "不断","建设",
    "以来", "征程", "国家", "人民", "特色", "理论", 
}



STOP = STOP_GENERIC | STOP_FRAME

NUM_TOPICS = 5

MIN_TOKEN_LEN = 2       # enlever les tokens trop courts
MIN_GLOBAL_FREQ = 3     # enlever les mots trop rares 

USE_FILTER_EXTREMES = True
NO_BELOW = 2
NO_ABOVE = 0.8

# Fichiers de sortie
OUT_TOPICS_TXT = "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/lda_topics_topwords.txt"
OUT_PREVALENCE_CSV = "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/lda_topic_prevalence.csv"
OUT_DOC_TOPICS_CSV = "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/lda_doc_topics.csv"


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Regrouper toutes les phrases ayant le même doc_index
docs_sentences = defaultdict(list)  # doc_index -> list[str]
docs_title = {}
for item in data:
    doc_id = item.get("doc_index", "unknown")
    title = item.get("title", "")
    sent = item.get("sentence", "")

    docs_sentences[doc_id].append(sent)

    if doc_id not in docs_title:
        docs_title[doc_id] = title

doc_ids = list(docs_sentences.keys())
doc_titles = [docs_title.get(d, "") for d in doc_ids]
doc_texts_raw = [" ".join(docs_sentences[d]) for d in doc_ids]


texts = []
for s in doc_texts_raw:
    toks = [t.strip() for t in jieba.lcut(s) if t.strip()]
    # Filtrage : enlever pivot, stopwords, tokens trop courts
    toks = [t for t in toks if len(t) >= MIN_TOKEN_LEN and t not in STOP and t != FOCUS]
    texts.append(toks)

# Enlever les mots trop rares
freq = Counter(w for doc in texts for w in doc)
texts = [[w for w in doc if freq[w] >= MIN_GLOBAL_FREQ] for doc in texts]

dictionary = corpora.Dictionary(texts)

if USE_FILTER_EXTREMES:
    dictionary.filter_extremes(no_below=NO_BELOW, no_above=NO_ABOVE)

corpus = [dictionary.doc2bow(doc) for doc in texts]


# ---- Diagnostics (IMPORTANT) ----
doc_count = len(corpus)
vocab_size = len(dictionary)
avg_doc_len = sum(len(doc) for doc in texts) / max(1, len(texts))
print(f"[DIAG] doc_count={doc_count} | vocab_size={vocab_size} | avg_doc_len={avg_doc_len:.1f}")



# Entraînement du modèle LDA
lda = models.LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=NUM_TOPICS,
    random_state=42,
    passes=12,
    iterations = 200,
    alpha="auto",
    eta="auto"
)

with open(OUT_TOPICS_TXT, "w", encoding="utf-8") as f:
    for k in range(NUM_TOPICS):
        f.write(f"Topic {k}\n")
        f.write(lda.print_topic(k, topn=15) + "\n\n")

# On va aussi calculer la "prévalence" : combien de phrases ont tel topic comme topic principal
topic_main_count = Counter()

with open(OUT_DOC_TOPICS_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["doc_index", "title", "n_sentences", "main_topic", "main_prob"])

    for doc_id, title, bow in zip(doc_ids, doc_titles, corpus):
        # Distribution des topics pour cette phrase
        dist = lda.get_document_topics(bow, minimum_probability=0.0)
        # dist = liste de (topic_id, prob)
        main_topic, main_prob = max(dist, key=lambda x: x[1])

        topic_main_count[main_topic] += 1
        n_sents = len(docs_sentences[doc_id])
        writer.writerow([doc_id, title, n_sents, main_topic, round(main_prob, 4)])

# Prévalence des topics
total = len(corpus)
with open(OUT_PREVALENCE_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["topic_id", "count_main_topic", "percentage_main_topic"])
    for k in range(NUM_TOPICS):
        c = topic_main_count[k]
        writer.writerow([k, c, round(c / total * 100, 2)])
