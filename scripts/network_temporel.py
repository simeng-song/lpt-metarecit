import json
import jieba
import networkx as nx
import csv

INPUT_FILE = "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/contexte.json"


# 1) Marqueurs temporels (ancres narratives)
# Pour identifier l’articulation du récit entre passé, présent (nouvelle ère) et futur
TEMPORAL = {
    "历史", "过去", "以来", "时代", "征程",
    "当前", "如今", "今天",
    "新时代",
    "未来", "将来", "面向未来", "走向", "迈向"
}

# 2) Concepts narratifs
# Ensemble de notions centrales du méta-récit étudié (acteurs collectifs, valeurs, objectifs, ouverture au monde)
CONCEPTS = {
    "命运", "共同体", "人类", "世界", "国际", "合作",
    "和平", "安全", "发展", "现代化", "强国",
    "文化", "精神", "理论", "思想", "社会主义", "特色", "中国式",
    "国家", "人民", "我们", "建设", "创新", "战略"
}

# 3) Unités très génériques du discours institutionnel
STOP = {
    "推动", "构建", "促进", "坚持", "加强", "提升",
    "深化", "推进", "完善", "落实", "实现", "显著",
    "持续", "加快", "一体化", "水平", "能力", "习近平", "总书记"
}

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extraire des phrases
sentences = [item["sentence"] for item in data]

# Construire le réseau lexical temporel

G = nx.Graph() # Créer un graphe non orienté

# Ajouter des noeuds temporels 
for t in TEMPORAL:
    G.add_node(t, node_type="temporal")
# Ajouter des noeuds conceptuels 
for c in CONCEPTS:
    G.add_node(c, node_type="concept")

# Calculer des cooccurrences 
for s in sentences:
    tokens = [t.strip() for t in jieba.lcut(s) if t.strip()]
    tokens = [t for t in tokens if len(t) >= 2 and t not in STOP] 

    token_set = set(tokens)

    # Marqueurs temporels présents dans la phrase
    present_temporal = [t for t in TEMPORAL if t in token_set]

    # Concepts présents dans la phrase
    present_concepts = [c for c in CONCEPTS if c in token_set]

    # Relier chaque marqueur temporel aux concepts apparaissant dans le même contexte
    for t in present_temporal:
        for c in present_concepts:
            if t == c:
                continue

            # Si l’arête existe déjà, on incrémente son poids
            if G.has_edge(t, c):
                G[t][c]["weight"] += 1
            else:
                # Sinon, on crée une nouvelle arête pondérée
                G.add_edge(t, c, weight=1)

# Visualisation
nx.write_gexf(G, "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/temporal_lexical_network.gexf")

# Tri des arêtes par poids décroissant
edges = sorted(G.edges(data=True), key=lambda x: -x[2]["weight"])

SORTIE_CSV = "/Users/songsimeng/INALCOM2/lpt-metarecit/resultats/temporal_edges_top.csv"
with open(SORTIE_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["temporal_marker", "concept", "weight"])

    for u, v, d in edges[:200]:
        if G.nodes[u]["node_type"] != "temporal":
            u, v = v, u
        writer.writerow([u, v, d["weight"]])

