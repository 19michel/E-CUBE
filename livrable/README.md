# Fourniture électrique

Le sujet abordé consiste à essayer d'établir la valeur de la consommation électrique de chaque entreprise française. Ces informations peuvent être utiles à des fournisseurs électriques pour leur permettre de cibler leur clientèle. 
Pour obtenir des valeurs de consommation, il faut utiliser des données en libre accès sur les entreprises françaises et la consommation de chaque commune ou de chaque IRIS (Ilot Regroupé pour l'Information Statistique). Ensuite, le travail consiste à manipuler ces bases de données afin de garder les informations essentielles permettant de calculer la consommation électrique.

## Travail sur les IRIS

Dans un premier temps, nous nous sommes intéressés à localiser l'IRIS auquel appartient chaque entreprise. En s'aidant des données en libre accès de l'IGN sur le contour des ces ilots géographiques, nous avons pu mettre en place un algorithme renvoyant l'IRIS auquel appartient un point représenté par ces coordonnées géographiques.

## Travail sur les différentes bases de données.

En utilisant la librairie Pandas sur Python, on a pu manipuler et croiser les informations de plusieurs bases de données : la base SIRENE de l'INSEE, la base CLAP de l'INSEE, la base de la SDES... Grâce aux fonctionnalités de pivot, de réindexage et de regroupement, nous sommes parvenus à obtenir une base de données globale regroupant toutes les informations qui nous étaient utiles.
La difficulté résidait essentiellement dans le fait que les différentes bases de données ne s'appuient pas forcément sur la même maille géographique (IRIS ou commune).

## Elaboration d'une distribution

Après avoir récupérer les données, il a fallu créé une distribution statistique pour chaque secteur d'activité. Le but était de représenter le nombre de communes situé dans un intervalle de consommation par salarié dans le secteur d'activité fixé. A l'aide d'une regression effectuée grâce au module SciPy.Stats, on peut obtenir une loi de distribution ainsi que ses paramètres.

## Optimisation

La dernière étape consiste à utiliser les distributions précédentes afin d'obtenir une approximation de la consommation électrique des entreprises. Pour chaque IRIS en France, on construit pour chaque entreprise une courbe de probabilité de la consommation. Puis on effectue une résolution d'un problème d'optimisation sous contraintes afin de maximiser la probabilité pour chaque entreprise tout en respectant une valeur total de consommation dans l'IRIS donnée par une autre base de données.

##GUI

La visualisation a été faite à l'aide du package Shiny de R, car facile à prendre en main et adapté aux études statistiques. Cette visualisation permet d'avoir un premier aperçu des données grâce à l'estimation obtenue avec l'optimisation. On obtient des données en entrant un code SIRET, ou bien des informations par IRIS, région ou secteur d'activité (APE). 