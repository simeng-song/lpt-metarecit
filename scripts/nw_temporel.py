import json
import jieba
import networkx as nx
import csv
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent               
RESULT_DIR = PROJECT_DIR / "resultats"
RESULT_DIR.mkdir(parents=True, exist_ok=True)

INPUT_FILE = RESULT_DIR / "contexte.json"
OUT_GEXF = RESULT_DIR / "tempo_lexical_nw.gexf"
OUT_CSV = RESULT_DIR / "tempo_edges_top.csv"

TEMPORAL = {
    "历史", "过去", "以来", "时代", "征程",
    "当前", "如今", "今天",
    "新时代",
    "未来", "将来", "面向未来", "走向", "迈向"
}

# Narrative concepts
CONCEPTS = {
    "命运", "共同体", "人类", "世界", "国际", "合作",
    "和平", "安全", "发展", "现代化", "强国",
    "文化", "精神", "理论", "思想", "社会主义", "特色", "中国式",
    "国家", "人民", "我们", "建设", "创新", "战略"
}

# Generic stop units
STOP = {
    "推动", "构建", "促进", "坚持", "加强", "提升",
    "深化", "推进", "完善", "落实", "实现", "显著",
    "持续", "加快", "一体化", "水平", "能力", "习近平", "总书记"
}

def tokens_from_sentence(s: str):
    toks = [t.strip() for t in jieba.lcut(s) if t.strip()]
    toks = [t for t in toks if len(t) >= 2 and t not in STOP]
    return toks

def find_temporal_markers(s: str, token_set: set):
    present = []
    for t in TEMPORAL:
        if t in token_set:
            present.append(t)
        else:
            # multi-word / phrase fallback
            if len(t) >= 3 and t in s:
                present.append(t)
    return present

# Load data
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

sentences = [item["sentence"] for item in data if "sentence" in item]

# compte concept global freq et downweight high-frequency concepts
concept_freq = Counter()
for s in sentences:
    token_set = set(tokens_from_sentence(s))
    for c in CONCEPTS:
        if c in token_set:
            concept_freq[c] += 1

for c in CONCEPTS:
    if concept_freq[c] == 0:
        concept_freq[c] = 1

# Construction du graph
G = nx.Graph()

for t in TEMPORAL:
    G.add_node(t, node_type="temporal")

for c in CONCEPTS:
    G.add_node(c, node_type="concept", freq=int(concept_freq[c]))

# cooccurrence avec downweighting:
# chaque fois (t, c) apparait ensemble, ajouter 1 / concept_freq[c]
# -> common concepts (国家/人民/发展...) contribute less per hit
for s in sentences:
    toks = tokens_from_sentence(s)
    token_set = set(toks)

    present_temporal = find_temporal_markers(s, token_set)
    present_concepts = [c for c in CONCEPTS if c in token_set]

    for t in present_temporal:
        for c in present_concepts:
            if t == c:
                continue
            incr = 1.0 / concept_freq[c]

            if G.has_edge(t, c):
                G[t][c]["weight"] += incr
                G[t][c]["count"] += 1
            else:
                G.add_edge(t, c, weight=incr, count=1)

# Outputs
nx.write_gexf(G, str(OUT_GEXF))

edges = sorted(G.edges(data=True), key=lambda x: -x[2]["weight"])

with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["temporal_marker", "concept", "weight", "raw_count"])

    for u, v, d in edges[:200]:
        if G.nodes[u].get("node_type") != "temporal":
            u, v = v, u
        writer.writerow([u, v, round(d["weight"], 6), d.get("count", 0)])

print(" - input :", INPUT_FILE)
print(" - gexf  :", OUT_GEXF)
print(" - csv   :", OUT_CSV)
