from pandas import read_csv    # Pour modifier document csv
from pandas import isna        # Pour tester si une entrée du CSV est défini
from networkx import Graph     # Structure de données en graphe
from time import time          # Pour mesurer la performance de mes algorithmes
from constantes import *       # Les constantes du programme


class Sujet_inexistant(Exception):
    """
    Exception lorsqu'un choix ne correspond à pas un sujet existant
    """
    def __init__(self, eleve, choix):
        self.eleve = eleve
        self.choix = choix

    def __str__(self):
        return f"Un choix de l'élève n°{self.eleve} ne correspond pas à un sujet existant : {self.choix}!"


class Importation_csv:
    """
    Importe les données CSV dans la structure d'un graphe NetworkX
    """

    @staticmethod
    def __importe_sujet(G, num_sujet, ligne):
        """
        Importe un sujet dans la structure G de networkX
        à partir d'une entree du fichier CSV
        """
        num_sujet = int(ligne.sujet)
        G.add_node(num_sujet)
        G.nodes[num_sujet]['bipartite'] = TYPE_BIPARTITE_SUJET  # indique que ce noeud fait parti de l'ensemble des sujets
        G.nodes[num_sujet]['effectif'] = 0   # initialise de nombre de participants du sujet
        G.nodes[num_sujet]['classes'] = {}   # utile pour les statistiques des classes
        G.nodes[num_sujet]['genres'] = {}    # utile pour les statistiques des genres

        # Stockage de l'id et des capacités min et max
        if not isna(ligne.c_min):  # s'il y a un c_min :
            G.nodes[num_sujet]["c_min"] = int(ligne.c_min)
        else:
            G.nodes[num_sujet]["c_min"] = MINIMUM_DE_CAPACITE

        if not isna(ligne.c_max):  # s'il y a un c_min :
            G.nodes[num_sujet]["c_max"] = int(ligne.c_max)
        else:
            G.nodes[num_sujet]["c_max"] = MAXIMUM_DE_CAPACITE
        G.sujets.append(num_sujet)

    @staticmethod
    def __importe_eleve(G, lecture_CSV_eleves, ligne):
        """
        Importe l'élève d'une ligne du CSV des élèves et l'insère dans le graphe G de networkX
        """
        num_eleve = int(ligne.eleve)
        G.add_node(num_eleve)
        G.nodes[num_eleve]['bipartite'] = TYPE_BIPARTITE_ELEVE
        G.nodes[num_eleve]['genre'] = ligne.genre
        G.nodes[num_eleve]['classe'] = ligne.classe
        G.genres.add(ligne.genre)  # maj de la listes des genres
        G.classes.add(ligne.classe)  # maj de la listes des classes
        G.nbre_eleves += 1

        # S'il y a déjà un sujet attribué
        # (Les cellules vides sont interprêtées par pandas comme Not A Number)
        if not isna(ligne.attribue):
            sujet_attribue = int(ligne.attribue)
            G.eleves_deja_affectes[num_eleve] = sujet_attribue

        else:  # S'il n'y a pas de sujet déjà attribué
            G.nodes[num_eleve]['attribue'] = NON_ASSIGNE  # numero du sujet

            if isna(ligne.choix1):
                    G.eleves_deja_affectes[num_eleve] = SUJET_NON_INSCRIT
                    print(f"L'élève n°{num_eleve} n'a pas de 1er choix --> assignation au sujet n°{SUJET_NON_INSCRIT}'!")
            else:
                NUM_COL_CHOIX1 = lecture_CSV_eleves.columns.get_loc('choix1') + 1  # + 1 car pandas ajoute à la lecture une colonne 0 'Index'
                for choix in range(0, NBRE_CHOIX):
                    # Importation des choix
                    if int(ligne[NUM_COL_CHOIX1 + choix]) not in G.nodes:
                        raise Sujet_inexistant(num_eleve, int(ligne[NUM_COL_CHOIX1 + choix]))
                    G.add_edge(num_eleve, int(ligne[NUM_COL_CHOIX1 + choix]), weight=choix)

        # Maj des listes :
        G.eleves.append(num_eleve)

    def importer_donnees(fichier_eleves, fichier_sujets):
        """
        En entree :
            1- le fichier CSV des eleves avec leurs choix avec une ligne d'entete :
            eleve,genre,classe,choix1,choix2,choix3,attribue
            2- le fichier CSV des sujets avec leurs contraintes avec une ligne d'entete :
            Sujet,min,max
            Attention : il faut impérativement qu'aucun numéro ne soit partagé par plus
            d'un élève ou sujet
        En sortie : le graphe G du probleme. Par defaut :
            1- les sujets ont des numéros < 100
            2- les eleves ont des numeros > 100

        Note : comme les sujets ont ete ajoutes d'abord, les liens de G sont
            de la forme [s_i, e_j] et non le contraire!
        """
        tic = time()  # Pour mesurer la performance du programme

        # Initialisation du graphe
        G = Graph()
        G.nbre_sujets = 0  # compteur du nombre de sujets
        G.nbre_eleves = 0  # compteur du nombre d'eleves
        G.sujets = []
        G.classes = set()  # listes des classes des eleves
        G.genres = set()  # listes des classes des eleves
        G.eleves = []  # listes des eleves
        G.eleves_deja_affectes = {}  # clé = n° élève, valeur = sujet déjà attribué

        # Importation des sujets #####################################################################
        lecture_sujets = read_csv(fichier_sujets)

        nombre_sujets = 0  # compteur pour ne pas importer l'entete

        for ligne in lecture_sujets.itertuples():
            Importation_csv.__importe_sujet(G, lecture_sujets, ligne)
            nombre_sujets += 1

        G.nbre_sujets = nombre_sujets  # Nombre total de sujets
        print(f"{G.nbre_sujets} sujets ont été importés!")

        # Ajout du sujet dédié aux élèves non-inscrits :
        num_sujet = SUJET_NON_INSCRIT
        G.add_node(num_sujet)
        G.nodes[num_sujet]['bipartite'] = TYPE_BIPARTITE_SUJET  # indique que ce noeud fait parti de l'ensemble des sujets
        G.nodes[num_sujet]['effectif'] = 0  # initialise de nombre de participants du sujet
        G.nodes[num_sujet]['classes'] = {}  # utile pour les statistiques des classes
        G.nodes[num_sujet]['genres'] = {}  # utile pour les statistiques des classes
        G.nodes[num_sujet]["c_max"] = 99999
        G.nodes[num_sujet]["c_min"] = 0
        G.sujets.append(num_sujet)

        # Importation des eleves #############################################
        nombre_eleves = 0
        # Ouvrir le CSV avec pandas et l'enregistre comme "dataframe"
        lecture_eleves = read_csv(fichier_eleves)

        # Iteration sur les lignes
        for ligne in lecture_eleves.itertuples():
            Importation_csv.__importe_eleve(G, lecture_eleves, ligne)
            nombre_eleves += 1

        print(f"{G.nbre_eleves} éleves ont été importés! ({time()-tic} s)")
        return G
