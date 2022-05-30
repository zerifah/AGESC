# **************************************************************************
# ************************ Constantes **************************************
# **************************************************************************

# Paramètres utiles lors de l'importation des fichiers CSV
MINIMUM_DE_CAPACITE = 2   # Nombre minimal d'élèves par défaut pour les sujets
MAXIMUM_DE_CAPACITE = 24  # Nombre maximal d'élèves par défaut por les sujets

# Texte apparaissant sur les listes de présence (exportation)
LISTES_CONSIGNE_A_RENDRE_A = "Olivier Simon (SIM)"
LISTES_CONSIGNE_JUSQUAU = "lundi 15 novembre 2022"

# **************************************************************************
#       Constantes pour le fonctionnement de l'algorithme d'affectation    *
# **************************************************************************

# Choisir le type d'affecation :
TYPE_APPARIEMENT = "genereux"  # minimise les derniers choix
# TYPE_APPARIEMENT = "glouton"  # maximise les premiers choix

# Autres constantes :
TYPE_BIPARTITE_ELEVE = 0  # sert a designer un noeud comme eleve
TYPE_BIPARTITE_SUJET = 1  # sert a designer un noeud comme sujet
SUJET_NON_INSCRIT = 0  # numero sujet pour les eleves non inscrits ou assignes
NON_ASSIGNE = ""  # valeur du champ "attribue" en cas de non-affectation
NBRE_CHOIX = 3            # Nombre de choix demandé aux élèves
