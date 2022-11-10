# Python & Data Engineering

On considère ici un projet très simple, avec un seul repository et une seul pipeline (2 si on considère le calcul du journal avec le plus de citations)

## Compatibilité avec un orchestrateur type DAG

Le code de ce projet à été orienté pour être facilement compatible avec un projet Dagster (l'orchestrateur que je connais le mieux) 

ainsi avec un minimum de modification il serait possible de transformer ce code pour le rendre compatible avec Dagster ou un autre orchestrateur.

les fonctions dans `ops.py` sont des tâches atomique et distribuables (les steps), tandis que le contenu de `job.py` représente la pipeline sous la forme d'un dag complet.


## *Quels sont les éléments à considérer pour faire évoluer votre code afin qu’il puisse gérer de grosses volumétries de données (fichiers de plusieurs To ou millions de fichiers par exemple) ?*
 - La taille des fichiers, si ceux-ci ne tiennent plus en ram alors il faut considérer de découper les fichiers en chunk, avec potentiellement des générateurs pour ne charger que la donnée en cours de traitement et pas le dataframe entier comme c'est le cas ici. Il sera ensuite possible de distribuer les calculs sur un cluster 

 - le nombre de fichiers, si il y en a énorméments alors il ne faut pas un filesystem mais un datalake (avec cloud storage / BigQuery) avec des lieux de stockages pour ces différentes sources et type de donné, ainsi que gérer des métadonnées sur le cycle de vie pour ne pas les retraiter plusieurs fois et avoir les données les plus à jour possible en permanence.

 - Il serait aussi important d'utiliser une base de données plutot que des objets en ram avec une sauvegarde seulement à la fin, il faut mettre en place des datamarts (ici représenté par le json), par exemple des datasets dans Google Big Querty, afin de mettre ces données à disposition des utilisateurs de celle ci. afin de gérer les erreurs sans perdre du temps de calcul qui peut être précieux, en plus de faire courir un risque à la qualité des données en cas de traitement partiels / multiples.


## *Pourriez-vous décrire les modifications qu’il faudrait apporter, s’il y en a, pour prendre en considération de telles volumétries ?*

 - Tout d'abord, il faudrait modifier le code afin de permettre d'avoir des entrées de fichier différentes

 - Utiliser des chunks dans le chargement des fichiers, et ainsi permettre le partitionnement des calculs
donc faire une réelle implémentation dans un orchestrateur afin de pouvoir gérer ce multi processing

 - si il y a énorméments de fichiers d'un type, alors tous les disposer dans un bucket, rendre paramétrique la step pour pubmed afin de gérer les entrées de manière dynamique depuis le bucket pour ne charger que ce qui tiens sur la machine qui effectue le calcul.
 - Faire le même traitement pour les clinical trials
 - Idem pour drugs à la différence qu'il faut soit les pré aggrérer, soit le gérer dans les opérateurs qui utilisent drugs pour utiliser des chunks, par exemple avec un dataset bigquery

 - Utiliser une autre librairie que pandas (spark par exemple) pour la gestion de dataframe de grande taille avec du streaming. ou alors en python pur, en faisant le chargement des lignes des différents fichiers en batch avec des générateurs
 - il faudrait modifier l'implémentation pour ne pas faire des boucles et utiliser uniquement l'api de la librairies choisie
avec des map reduce pour permettre la paraléllisation, ou alors de découper le dataframe en chunk afin d'éclater les opérateurs en plusieurs instances sur des parties différentes qui seront aggrégées à la fin
 - utiliser des format de fichiers plus efficace (par exemple parquet) ou distribué (hdfs / Dataproc) dans un datalake
