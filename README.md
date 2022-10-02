# Projet : Création d'un outil type Kayak - WebScraping et EDA

## 1. Data Overview et objectifs

L'étude s'articule ainsi autour de trois axes :
<ul>
  <li>Le pré-processing des données, avec les librairies <code>spacy</code> et <code>re</code></li>
  <li>L'utilisation de <code>DBSCAN</code>, qui permet de faire du clustering sur les données, afin de rassembler les produits avec une description similaire</li>
  <li>Méthode LSA via <code>TruncatedSVD</code> de <code>scikit-learn</code>, ou <i>topic-modeling</i>, qui créé des topics pertinents en rapport avec la description des produits.
    Pour chaque produit, une note par topic est associée, plus celle-ci se rapproche de 1, mieux le topic explique le produit.</li>
</ul>

## 2. Aperçu
Après un fine-tuning des hyper-paramètres du `DBSCAN` pour trouver les paramètres optimaux du clustering, faisant la balance entre le nombre de clusters et le nombre d'outliers, l'analyse des mots représentatifs du cluster est possible par un `WordCloud`, dont voici un exemple pour le cluster n°6 :

Le cluster 6, par exemple, regroupe majoritairement des produits à base de laine ou des articles de montagne, ainsi si un utilisateur cherche un produit chaud pour la montagne, l'algorithme pourra proposer différents articles connexes à sa recherche.

Le reste de l'étude est détaillé dans <a href='https://github.com/Chedeta/the_north_face_nlp/blob/main/NorthFace_final.ipynb'>le notebook</a> mis à disposition.

## 3. Crédits
Le projet a été effectué en collaboration avec <a href='https://github.com/Bebock'>Hélène</a>, <a href=''>Henri</a> et <a href='https://github.com/NBridelance'>Nicolas</a>.

