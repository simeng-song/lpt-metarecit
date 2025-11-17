## Projet Linguistique pour le TAL - métarécit

**Analyse du méta-récit chinois : Communauté de destin pour l'humanité (人类命运共同体)**

Ce projet s'inscrit dans le cadre du cours Linguistique pour le TAL (M. Mathieu Valette). Notre objectif est d'étudier un méta-récit civilisationnel à travers un corpus de discours institutionnels chinois. Nous avons choisi le méta-récit de **« 人类命运共同体 » (communauté de destin pour l’humanité)**, concept central de plusieurs discours politiques récents (discours officiels et interventions diplomatiques).  
   
Ce méta-récit relève à la fois :  

- systèmes narratifs (vision globale de l'ordre international)
- identités narratives (positionnement identitaire de la Chine)
- issues narratives (mécanismes concrets, par exemple les initiatives de "la Ceinture et la Route" 一带一路)  


 
11/17
Nous avons constitué un corpus cohérent d'articles institutionnels chinois portant sur le méta-récit. Les textes proviennent de sources officielles telles que le Quotidien du Peuple, Xinhua et plusieurs discours diplomatiques ou politiques. Après avoir regroupé l’ensemble des documents en un fichier brut, nous avons développé un premier script (`inspect_raw.py`) permettant d’inspecter la taille, la structure et les occurrences des mots clés du corpus. Cette étape a confirmé que le corpus contient environ 60 000 caractères, 695 lignes, et que l’expression centrale « 人类命运共同体 » apparaît 185 fois, ce qui valide sa position de pivot narratif.   
  
Après le nettoyage, nous avons effectué une première analyse lexicale avec `tokeniez_freq.py`, utilisant la segmentation chinoise (jieba) et un filtrage de mots vides. Les fréquences obtenues montrent une forte domination de termes tels que « 发展 », « 合作 », « 共建 », « 世界 », « 人类 », « 共同体 », « 命运 », « 文明 » et « 一带一路 ». Ce champ lexical confirme la présence d'un méta-récit centré sur le développement, la coopération internationale, la vision civilisationnelle et les initiatives globales.  
  
**Travail à venir :**  


- [ ] Analyse par document (TF-IDF, variations inter-discours)
- [ ] Extraction de collocations (PMI, cooccurrences)
- [ ] Wordclouds globaux et par document
- [ ] Clustering (KMeans / LDA) pour dégager des thématiques
- [ ] Analyse comparative (possibilité : versions anglaises ou françaises)
- [ ] Construction d’un réseau lexical (NetworkX)
