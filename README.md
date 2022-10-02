# Projet : Création d'un outil type Kayak - WebScraping et EDA

## 1. Data Overview et objectifs

Pas de dataset à proprement parler dans ce projet, les données sont à chercher soi-même. En effet, dans le but de re-créer un outil de type Kayak, qui permet de comparer les hotels et de donner des top-destinations, il a fallu récupérer des données sur les villes les plus visitées, les hôtels les mieux notés et enfin les météos associées à chacune des villes.

Pour cela, pas énormément de choix si ce n'est accéder à ces données soit par une <code>api</code>, soit par du <code>web-scraping</code>.

Ainsi, les données de chacuns des hôtels des villes phares du tourisme en France sont récupérées par scraping sur le site <i>Booking.com</i>.

Pour la méteo, les données sont récupérées via une <code>api</code> de <i>MétéoConcept</i>

L'étude s'articule ainsi autour de trois axes :
<ul>
  <li>La récupération des données sur les hôtels avec <code>Spyder</code></li>
  <li>Le nettoyage des données et l'export pour utilisation en tant que base de données</li>
  <li>Analyse exploratoire pour proposer des top destinations en fonction de critères tels que la météo ou encore les notes attribuées aux hôtels.</li>
</ul>

## 2. Aperçu
Après un fine-tuning des hyper-paramètres du `DBSCAN` pour trouver les paramètres optimaux du clustering, faisant la balance entre le nombre de clusters et le nombre d'outliers, l'analyse des mots représentatifs du cluster est possible par un `WordCloud`, dont voici un exemple pour le cluster n°6 :

Le cluster 6, par exemple, regroupe majoritairement des produits à base de laine ou des articles de montagne, ainsi si un utilisateur cherche un produit chaud pour la montagne, l'algorithme pourra proposer différents articles connexes à sa recherche.

Le reste de l'étude est détaillé dans <a href='https://github.com/Chedeta/the_north_face_nlp/blob/main/NorthFace_final.ipynb'>le notebook</a> mis à disposition.

## 3. Crédits
Le projet a été effectué en collaboration avec <a href='https://github.com/Bebock'>Hélène</a>, <a href=''>Henri</a> et <a href='https://github.com/NBridelance'>Nicolas</a>.

