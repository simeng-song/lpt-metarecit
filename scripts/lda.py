import json
import jieba
from collections import Counter
from gensim import corpora, models
import csv

# Fichier JSON : sous-corpus de phrases contenant « 新时代 »
INPUT_FILE = "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/contexte.json"

# Pivot étudié 
FOCUS = "新时代"

# Mots génériques institutionnels (bruit)
STOP = set([
    "推动","构建","发展","促进","坚持","加强","提升","深化","推进","完善",
    "落实","实现","显著","持续","加快","一体化","水平","能力"
])

NUM_TOPICS = 5

MIN_TOKEN_LEN = 2       # enlever les tokens trop courts
MIN_GLOBAL_FREQ = 5     # enlever les mots trop rares 

# Fichiers de sortie
OUT_TOPICS_TXT = "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/lda_topics_topwords.txt"
OUT_PREVALENCE_CSV = "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/lda_topic_prevalence.csv"
OUT_SENT_TOPICS_CSV = "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/lda_sentence_topics.csv"


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

sentences = [item["sentence"] for item in data]

texts = []
for s in sentences:
    toks = [t.strip() for t in jieba.lcut(s) if t.strip()]
    # Filtrage : enlever pivot, stopwords, tokens trop courts
    toks = [t for t in toks if len(t) >= MIN_TOKEN_LEN and t not in STOP and t != FOCUS]
    texts.append(toks)

# Enlever les mots trop rares
freq = Counter(w for doc in texts for w in doc)
texts = [[w for w in doc if freq[w] >= MIN_GLOBAL_FREQ] for doc in texts]

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(doc) for doc in texts]

# Entraînement du modèle LDA
lda = models.LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=NUM_TOPICS,
    random_state=42,
    passes=12,
    alpha="auto",
    eta="auto"
)

with open(OUT_TOPICS_TXT, "w", encoding="utf-8") as f:
    for k in range(NUM_TOPICS):
        f.write(f"Topic {k}\n")
        f.write(lda.print_topic(k, topn=15) + "\n\n")

# On va aussi calculer la "prévalence" : combien de phrases ont tel topic comme topic principal
topic_main_count = Counter()

with open(OUT_SENT_TOPICS_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["sent_index", "main_topic", "main_prob", "sentence"])

    for i, bow in enumerate(corpus):
        # Distribution des topics pour cette phrase
        dist = lda.get_document_topics(bow, minimum_probability=0.0)
        # dist = liste de (topic_id, prob)
        main_topic, main_prob = max(dist, key=lambda x: x[1])

        topic_main_count[main_topic] += 1
        writer.writerow([i, main_topic, round(main_prob, 4), sentences[i]])

# Prévalence des topics
total = len(corpus)
with open(OUT_PREVALENCE_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["topic_id", "count_main_topic", "percentage_main_topic"])
    for k in range(NUM_TOPICS):
        c = topic_main_count[k]
        writer.writerow([k, c, round(c / total * 100, 2)])
