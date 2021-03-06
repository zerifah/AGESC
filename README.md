# AGESC
Programme python d'Affectation Généreux/Glouton d'Eleves Selon leur Choix.

# A quoi sert ce module?
Lors d'une semaine thématique, il y a différents sujets proposés par les profs, qui ont chacun une capacité limitée.
Chaque élève dresse la liste des sujets dans son ordre de préférence (par défaut, seulement les trois premiers).
Ce programme python permet :
* d'affecter automatiquement les sujets aux élèves de façon à en placer le maximum tout en minimisant les derniers choix des élèves.
* de générer les listes de présences.
Ce programme peut être adapté à d'autres situations où des agents doivent être affectés à des objets capacitifs selon leur préférence unilatéral.

# Installation
Ouvrir un terminal
Naviguer jusqu'au dossier `src` du projet
Exécuter `pip install -r requirements.txt`

# Lancer le programme
Naviguer dans jusqu'au dossier src.
Puis taper `python App.py` ou `python3 App.py`

# Paramètres
Le fichier constantes.py contient certains paramètres qui peuvent modifier le comportement de l'algorithme d'affectation.
* `TYPE_APPARIEMENT`:
  * si `TYPE_APPARIEMENT` = "genereux", l'algorithme minimise les derniers choix
  * si `TYPE_APPARIEMENT` = "glouton", l'algorithme maximise les premiers choix
* `NBRE_CHOIX` indique le nombre de choix maximum qu'un·e élève peut faire. Par défaut, `NBRE_CHOIX` = 3.

# Exemples d'entrées et de sorties
Le dossier exemples donne des fichiers pour tester l'algorithme ou voir les résultats.

* Fichiers d'entrée :
  * eleves.csv
  * sujets.csv

* Fichiers de sortie :
  * eleves_affectes.csv
  * sujets_statistiques.csv
  * listes_des_participants.pdf

# Formulaire d'acquisition des données
Un formulaire avec PHP, HTML, CSS, Vue.JS et MYSQL a été réalisé pour collecter les choix des élèves. Contactez-moi en cas d'intérêt intéressé à l'obtenir.
