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

## 2. Aperçu des résultats 

Après extraction et nettoyage des données, l'utilisation de <code>mapbox</code> et <code>plotly</code> permettent de visulaliser les données des hôtels :
<p align='center'><img src="https://i.ibb.co/kBP5K5k/Capture-d-cran-2022-10-02-113802.png" alt="Capture-d-cran-2022-10-02-113802" border="0"></p>

Mais aussi les données concernant la météo :
<p align='center'><img src="https://i.ibb.co/n6np9sq/Sans-titre.jpg" alt="Sans-titre" border="0"></p>

Le reste de l'étude est détaillé dans <a href='https://github.com/Chedeta/the_north_face_nlp/blob/main/NorthFace_final.ipynb'>le notebook</a> mis à disposition et en vidéo pour la visualisation des graphiques.

## 3. Crédits

Auteur : Jean Ivars

