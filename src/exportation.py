from datetime import datetime  # pour indiquer la date
from pathlib import Path       # Pour tester si un fichier existe déjà
from pandas import read_csv    # Pour modifier document csv


class Exportation:
    """
        Classe contenant les méthodes pour l'exportation des données :
        1- exportation_statistiques(f_sujets_sortie, G)
        2- exportation_eleves(f_eleves, f_eleves_sortie, G)
    """
    @staticmethod
    def __genere_nouveau_nom_de_fichier(nom, extension=".csv"):
        """
            retourne une chaine de caractre du type nomX avec
            X le premier entier tel que nomX ne correspond pas
            à un fichier qui existe deja.
        """
        fichier_objet = Path(nom + extension)
        nouveau_nom = fichier_objet
        nombre = -1
        while fichier_objet.is_file():
            nombre += 1
            nouveau_nom = nom + str(nombre) + extension
            fichier_objet = Path(nouveau_nom)
        return nouveau_nom

    @staticmethod
    def creer_csv_statistiques_sujets(f_sujets_sortie, G):
        """Cree un fichier CSV avec les statistique des sujets stockés dans G :
            - nombre d'inscrits
            - nombre de garçons
            - nombre de filles
            - nombre d'éleves par classe
        Entrées :
            - le nom du fichier de sortie
            - le graphe G contenant les donnees
        Sortie : String f_eleves
        """
        f_sujets_sortie = Exportation.__genere_nouveau_nom_de_fichier(f_sujets_sortie, ".csv")
        f = open(f_sujets_sortie, 'w')
        # Entete
        date = str(datetime.today().year) \
            + str(datetime.today().month) \
            + str(datetime.today().day) \
            + " " + str(datetime.today().hour) \
            + ":" + str(datetime.today().minute)
        f.write(f"sujet,min,max,effectifs,")
        for e in sorted(G.genres):
            f.write(e + ",")

        for e in sorted(G.classes):
            f.write(e + ",")
        f.write(date + "\n")

        # Entrees
        for n in G.sujets:
            f.write(str(n) + "," +
                    str(G.nodes[n]['c_min']) + "," +
                    str(G.nodes[n]['c_max']) + "," +
                    str(G.nodes[n]['effectif']) + ",")

            for e in sorted(G.genres):
                if e in G.nodes[n]['genres'].keys():
                    f.write(str(G.nodes[n]['genres'][e]) + ",")
                else:
                    f.write(",")

            for e in sorted(G.classes):
                if e in G.nodes[n]['classes'].keys():
                    f.write(str(G.nodes[n]['classes'][e]) + ",")
                else:
                    f.write(",")
            f.write("\n")

        f.close()

        print(f"Exportation des statistiques des sujets dans le fichier {f_sujets_sortie}.")
        return f_sujets_sortie

    @staticmethod
    def ajoute_attributions_aux_fichiers_eleves(f_eleves, f_eleves_sortie, G):
        """
            Ajoute les attributions des élèves stocké
            dans le graphe G dans le fichier f_eleves
            Sortie : String f_eleves
        """
        # Lecture du fichier csv à compléter
        df = read_csv(f_eleves)  # df pour dataframe

        # Iteration sur les entrees du fichier csv (sans l'entete)
        for entree in df.itertuples():
            id_eleve = df.loc[entree.Index, 'eleve']  # Recuperation de l'id de l'eleve
            sujet_attribue = G.nodes[id_eleve]['attribue']
            if sujet_attribue != "":
                df.loc[entree.Index, 'attribue'] = str(sujet_attribue)  # Ecriture du sujet attribué pour cet id
            else:
                sujet_attribue = 0
                df.loc[entree.Index, 'attribue'] = str(sujet_attribue)  # Ecriture du sujet attribué pour cet id
                print("L'éleve " + str(id_eleve) + " n'a pas pu être placé·e!")

        # Ecriture sur un nouveau document :
        f_eleves_sortie = Exportation.__genere_nouveau_nom_de_fichier(f_eleves_sortie, ".csv")
        df.to_csv(f_eleves_sortie, index=False)
        print(f"Exportation des affectations dans le fichier {f_eleves_sortie}.")
        return f_eleves_sortie
