import json
import jieba
from collections import defaultdict

# Chaque entrée correspond à une phrase contenant l’expression "新时代"
INPUT_FILE = "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/contexte.json"

FOCUS = "新时代" # marqueur central du méta-récit (pivot discursif)

# Liste de mots très génériques du discours institutionnel
# Ces unités sont volontairement exclues afin de réduire le bruit lexical
STOP = set([
    "推动","构建","发展","促进","坚持","加强","提升","深化","推进","完善",
    "落实","实现","显著","持续","加快","一体化","水平","能力","习近平","总书记"
])

# Dictionnaire pour stocker les cooccurrences
cooc_focus = defaultdict(int)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data:
    sent = item["sentence"]
    if FOCUS not in sent: 
        continue

    toks = [t for t in jieba.lcut(sent) if t.strip()]
    tokset = set(toks)

    for w in tokset:
        if w == FOCUS: # Exclure le pivot lui-même
            continue
        if w in STOP: # Exclure les mots définis dans la liste
            continue
        if len(w) < 2:
            continue
        cooc_focus[w] += 1

print("Top 30 des unités cooccurrentes avec le pivot：")
for w, c in sorted(cooc_focus.items(), key=lambda x: -x[1])[:30]:
    print(w, c)
