## Projet Linguistique pour le TAL - métarécit

### 1. Objectif

**Analyse du méta-récit chinois : Communauté de destin pour l'humanité (人类命运共同体)**

Ce projet s'inscrit dans le cadre du cours Linguistique pour le TAL (M. Mathieu Valette). Notre objectif est d'étudier un méta-récit civilisationnel à travers un corpus de discours institutionnels chinois. Nous avons choisi le méta-récit de **« 人类命运共同体 » (communauté de destin pour l'humanité)**, concept central de plusieurs discours politiques récents (discours officiels et interventions diplomatiques).  

Nous allons analyser le méta-récit en adoptant un angle spécifique : **新时代 (Nouvelle ère)** dans un cadre temporel qui permet : 
- d'interpréter le présent
- d'articuler les défis mondiaux
- de légitimer l'appel à un futur partagé
- d'inscrire la communauté de destin pour l'humanité dans une vision évolutive de l'histoire
 

### 2. Corpus

Le corpus a été collecté via le site institutionnel [people.cn](http://www.people.com.cn/) avec le mot-clé : **« 人类命运共同体 » (communauté de destin pour l'humanité)**
On a fait un script pour récupérer les 80 pages du site qui contiennent le mot-clé, et puis mettre dans un fichier json.

### 3. Prétraitement

- nettoyage des balises
- segementation avec outil jieba
- statistique générale (fréquence des mots)
- extraction des contextes autour de "nouvelle ère" et "communauté de destin pour l'humanité" : 1660 sentences avec 新时代 enreigistré dans contexte.json

### 4. Analyse 

- analyse lexicale (wordcloud, TF-IDF)
- cooccurrences ciblées
- clustering (KMeans / LDA)
- réseaux lexicaux : pour visualiser l'articulation temporelle du récit (NetworkX)

### 5. Analyse narrative

- Analyse actancielle (modèle de Greimas) : Idéalement, nous visons à identifier les 6 rôles. Sujet, objet, destinateur, destinataire, adjuvants(helper), opposants. Et construirons un schéma actanciel global du méta-récit.

- Zonage anthropique : zone identitaire, zone proximale, zone distale

Référence : https://arxiv.org/pdf/2409.06540

### 6. Résultat attendu

- structure l'interprétation du monde
- légitime un avenir collectif (« communauté de destin pour l'humanité »)
- organise un récit du présent comme moment charnière
- et crée une dynamique narrative liant passé → présent → futur