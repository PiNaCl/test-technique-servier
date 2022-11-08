# Python & Data Engineering

On considère ici un projet très simple, avec un seul repository et une seul pipeline (2 si on considère le calcul du journal avec le plus de citations)

## Compatibilité avec un orchestrateur type DAG

Le code de ce projet à été orienté pour être facilement compatible avec un projet Dagster (l'orchestrateur que je connais le mieux) 

ainsi avec un minimum de modification il serait possible de transformer ce code pour le rendre compatible avec Dagster ou un autre orchestrateur.

les fonctions dans `ops.py` sont des tâches atomique et distribuables (les steps), tandis que le contenu de `job.py` représente la pipeline sous la forme d'un dag complet.


## *Quels sont les éléments à considérer pour faire évoluer votre code afin qu’il puisse gérer de grosses volumétries de données (fichiers de plusieurs To ou millions de fichiers par exemple) ?*
 - La taille des fichiers, si ceux-ci ne tiennent plus en ram alors il faut considérer de découper les fichiers en chunk, avec potentiellement des générateurs pour ne charger que la donnée en cours de traitemetn et pas le dataframe entier comme c'est le cas ici

 - le nombre de fichiers, si il y en a énorméments alors il ne faut pas un filesystem mais un datalake avec des lieux de stockages pour ces différentes sources et type de donné, ainsi que gérer des métadonnées sur le cycle de vie pour ne pas les retraiter plusieurs fois

- Il serait aussi important d'utiliser une base de données robuste plutot que des objets en ram avec une sauvegarde seulement à la fin, il faut mettre en place des datamarts (ici représenté par le json) afin de mettre ces données à disposition des utilisateurs de cette donnée. afin de gérer les erreurs sans perdre du temps de calcul qui peut être précieux, en plus de faire courir un risque à la qualité des données en cas de traitement partiels / multiples.


## *Pourriez-vous décrire les modifications qu’il faudrait apporter, s’il y en a, pour prendre en considération de telles volumétries ?*

 - Tout d'abord, il faudrait modifier le code afin de permettre d'avoir des entrées de fichier différentes


 - Utiliser des chunks dans le chargement des fichiers, et ainsi permettre le partitionnement des calculs
donc faire une réelle implémentation dans un orchestrateur afin de pouvoir gérer ce multi processing
 
 - si il y a énorméments de fichiers d'un type (exemple 500 fichiers pubmed): alors créer un dossier (potentiellement remote avec la gestion des accès), et rendre paramétrique la step pour pubmed afin de gérer les entrées de manière dynamique ou facilement modifiable
 - Faire le même traitement pour les clinical trials
 - Idem pour drugs à la différence qu'il faut soit les pré aggrérer, soit le gérer dans les opérateurs qui utilisent drugs pour utiliser des chunks

 - Utiliser une autre librairie que pandas (spark ou dask par exemple) pour la gestion de dataframe de grande taille. ou alors en python pur, en faisant le chargement des lignes des différents fichiers en batch avec des générateurs
 - il faudrait modifier l'implémentation pour ne pas faire des boucles et utiliser uniquement l'api de la librairies choisie
avec des map reduce pour permettre la paraléllisation, ou alors de découper le dataframe en chunk afin d'éclater les opérateurs en plusieurs instances sur des parties différentes qui seront aggrégées à la fin
 - utiliser des format de fichiers plus efficace (par exemple parquet) ou distribué (hdfs) dans un datalake
