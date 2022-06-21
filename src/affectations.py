from networkx import Graph     # Structure de données en graphe
from networkx import subgraph  # Renvoie un sous-graphe
from copy import deepcopy      # pour faire de la copie profonde d'objets
from time import time          # Pour mesurer la performance de mes algorithmes
from profil import *           # Classe maison pour l'algorithme genereux
from constantes import *       # Les constantes du programme
from importation_csv import *  # Classe maison pour l'importation
from exportation import *      # Classe maison pour l'importation
# import shelve # Sauvegarder ou charger des données pour tests


def sujet_incremente_statistiques(G, sujet, eleve):
    classe = G.nodes[eleve]['classe']
    genre = G.nodes[eleve]['genre']
    if classe in G.nodes[sujet]["classes"]:
        G.nodes[sujet]["classes"][classe] = G.nodes[sujet]["classes"][classe] + 1
    else:
        G.nodes[sujet]["classes"][classe] = 1

    if genre in G.nodes[sujet]["genres"]:
        G.nodes[sujet]["genres"][genre] = G.nodes[sujet]["genres"][genre] + 1
    else:
        G.nodes[sujet]["genres"][genre] = 1


def assigne_eleve_au_sujet(G, eleve, sujet):
    """ Assigne l'eleve au sujet dans la structure de G"""
    G.nodes[eleve]['attribue'] = sujet
    sujet_incremente_statistiques(G, sujet, eleve)
    G.nodes[sujet]['effectif'] += 1


def suppression_sujets_non_populaires(G):
    """
    Supprime les sujets dont le nombre de choix d'eleves est inferieur a sa capacite minimum
    retourne la liste des sujets supprimes.
    """
    sujets = {n for n, d in G.nodes(data=True) if d["bipartite"] == TYPE_BIPARTITE_SUJET}
    sujets_supprimes = []
    for n in sujets:
        if G.degree[n] < G.nodes[n]["c_min"]:
            sujets_supprimes.append(n)
            print(f"Le sujet n°{n} a été supprimé faute d'assez d'interessés.")
            G.remove_node(n)  # Supprime un noeud et tous ses liens
    return sujets_supprimes


def liste_sujets_en_sous_effectifs(G, M):
    """
    Retourne la liste des sujets de G qui n'ont pas atteint la capacite minimum
    ou None s'il n'y en a aucun.
    """
    sujets = {n for n, d in G.nodes(data=True) if d["bipartite"] == TYPE_BIPARTITE_SUJET}
    res = []
    for s in sujets:
        if s in M and M.degree[s] < G.nodes[s]["c_min"]:
            res.append(s)

    if res == []:
        print("Tous les sujets sont suffisamments remplis!")
        return None

    return res


def liste_eleves_exposes(G, M):
    """ Retourne la liste des eleves de G sans affectation dans M"""
    eleves = [n for n, d in G.nodes(data=True) if d["bipartite"] == TYPE_BIPARTITE_ELEVE]
    for e in M.edges:
        if e[0] in eleves:
            eleves.remove(e[0])
        if e[1] in eleves:
            eleves.remove(e[1])
    return eleves


def liste_sujets_incomplets(G, M):
    """
        Entree : liste de noeuds "sujets", appariement M.
        Sortie : liste des sujets incomplets dans M
    """
    res = []
    for s in G.sujets:
        if s not in M:
            res.append(s)
        else:
            if M.degree(s) < G.nodes[s]['c_max']:
                res.append(s)
    return res


def Max_Aug(G, k, M):  # Manlove, Algorithme 8.3 page 401
    """ Sous-fonction de maximum gourmand """
    # Initiation
    ##################################################################
    P = Graph()
    G.eleves_exposes = liste_eleves_exposes(G, M)
    profils = {}  # Liste des profils des sujets
    predecesseurs = {}  # Liste des predecesseurs des sujets
    liens_de_G_pas_dans_M = G.edges - M.edges

    # Initialisation de la liste des sujets incomplets
    sujets_incomplets = liste_sujets_incomplets(G, M)

    # Initialise les profils d'amélioration possible
    for s in G.sujets:
        profils[s] = profil.zero(NBRE_CHOIX)
        predecesseurs[s] = None
        for e in G.eleves_exposes:
            if (e, s) in G.edges:
                rang = G.edges[e, s]['weight']
                rho = profil.zero(NBRE_CHOIX) + rang
                if rho > profils[s]:
                    profils[s] = rho
                    predecesseurs[s] = e

    # Boucle principale
    ############################################################
    changement = True
    compteur = 1
    while compteur <= k and changement:
        changement = False
        # Pour tous les liens de G qui ne sont pas dans M
        for [s_j, e_i] in liens_de_G_pas_dans_M:
            # Si l'eleve  est deja assigne
            if e_i in M:
                sujet_assigne_dans_M = list(M[e_i])[0]
                # Avec list(M[e_i])[0] qui donne le noeud assigne a l'eleve dans M et
                # G.edge[e_i][s_j]['weight'] qui donne le rang de preference de l'eleve pour le sujet :
                rho = profils[sujet_assigne_dans_M] + G.edges[e_i, s_j]['weight'] - G.edges[e_i, sujet_assigne_dans_M]['weight']
                if rho > profils[s_j]:
                    profils[s_j] = rho
                    predecesseurs[s_j] = e_i
                    changement = True
        compteur += 1

    # Phase finale
    ###############################################################

    rho, indice_max = profil.max_L([profils[s] for s in sujets_incomplets] + [profil.zero(NBRE_CHOIX)])

    if rho > profil.zero(NBRE_CHOIX):
        # Recherche du sujet non complet qui peut augmenter son profil :
        s_max = sujets_incomplets[indice_max]
        P = [s_max]
        noeud_actif = s_max
        stop = True
        while stop:
            pred = predecesseurs[noeud_actif]
            P.append(pred)
            if pred not in M:  # Si eleve pas assigne, on a fini le chemin
                stop = False
            else:  # Si l'eleve assigne, on suit son affectation
                noeud_actif = list(M[pred])[0]
                P.append(noeud_actif)
        return P
    else:
        return None  # Il n'existe pas de chemin augmente


def Min_Aug(G, k, M):
    """ Sous-fonction de maximum genereux """
    tic0 = time()
    # Initiation
    ##################################################################
    P = Graph()
    eleves_exposes = liste_eleves_exposes(G, M)
    profils = {}  # Liste des profils des sujets
    predecesseurs = {}  # Liste des predecesseurs des sujets
    liens_de_G_pas_dans_M = G.edges - M.edges

    # Initialisation de la liste des sujets incomplets
    sujets_incomplets = liste_sujets_incomplets(G, M)

    # Initialise les profils d'amélioration possible
    for s in G.sujets:
        profils[s] = profil.zero_R(NBRE_CHOIX, G.nbre_eleves + 1)
        predecesseurs[s] = None
        for e in eleves_exposes:
            if (e, s) in G.edges:
                rang = G.edges[e, s]['weight']
                rho = profil.zero(NBRE_CHOIX) + rang
                if rho < profils[s]:
                    profils[s] = rho
                    predecesseurs[s] = e

    # Boucle principale
    ############################################################
    changement = True
    compteur = 1
    while compteur <= k and changement:
        changement = False
        for [s_j, e_i] in liens_de_G_pas_dans_M:  # Jadis,c'était for [s_j, e_i] in (G.edges - M.edges)):
            # Si l'eleve  est deja assigne
            if e_i in M:
                sujet_assigne_dans_M = list(M[e_i])[0]
                # Avec list(M[e_i])[0] qui donne le noeud assigne a l'eleve dans M et
                # G.edge[e_i][s_j]['weight'] qui donne le rang de preference de l'eleve
                rho = profils[sujet_assigne_dans_M] + G.edges[e_i, s_j]['weight'] - G.edges[e_i, sujet_assigne_dans_M]['weight']
                if rho < profils[s_j]:
                    profils[s_j] = rho
                    predecesseurs[s_j] = e_i
                    changement = True
        compteur += 1

    # Phase finale
    ###############################################################

    # TODO modifier min_R pour qu'en cas d'égalité entre plusieurs profils,
    # il choisisse selon une certaine heuristique
    rho, indice_min = profil.min_R([profils[s] for s in sujets_incomplets] + [profil.zero_R(NBRE_CHOIX, G.nbre_eleves + 1)])

    if rho < profil.zero_R(NBRE_CHOIX, G.nbre_eleves + 1):
        # Recherche du sujet non complet qui peut augmenter son profil :
        s_min = sujets_incomplets[indice_min]
        P = [s_min]
        noeud_actif = s_min
        stop = True
        while stop:
            pred = predecesseurs[noeud_actif]
            P.append(pred)
            if pred not in M:  # Si l'eleve n'est pas assigne, on a fini le chemin
                stop = False
            else:  # Si l'eleve assigne, on suit son affectation
                noeud_actif = list(M[pred])[0]
                P.append(noeud_actif)
        return P

    else:
        return None  # Il n'existe pas de chemin augmente


def augmente_M_selon_P(M, P, G):
    """
    definit l'operation + avec un cercle qui consiste en,
    pour chaque lien contenu dans le chemin P,
        1- s'il n'est pas dans M, on ajoute ce lien
        2- s'il est deja dans M, on supprime ce lien
    Le terme est 'différence symétrique'.

    Entrées : l'appariment M qu'on va modifier selon le chemin P et G qu'on met a jour
    Sortie : retourne M augmente avec P.
    """
    for i in range(1, len(P)):
        lien = [P[i-1], P[i]]

        if G.nodes[lien[0]]["bipartite"] == TYPE_BIPARTITE_ELEVE:
            eleve = lien[0]
            sujet = lien[1]
        else:
            sujet = lien[0]
            eleve = lien[1]
        classe = G.nodes[eleve]["classe"]
        genre = G.nodes[eleve]["genre"]

        if lien in M.edges:
            M.remove_edge(lien[0], lien[1])
            G.nodes[sujet]["classes"][classe] = G.nodes[sujet]["classes"][classe] - 1
            G.nodes[sujet]["genres"][genre] = G.nodes[sujet]["genres"][genre] - 1

        else:
            M.add_edge(lien[0], lien[1])
            sujet_incremente_statistiques(G, sujet, eleve)

    return M


def appariement_demarrage_rapide(G):
    """
    Apparie tous les agents possible a leur premier choix en tenant compte
    des capacites des sujets.
    Entree : le graphe du probleme
    Sortie : l'appariement M

    """
    M = Graph()

    # Crée tableau des effectifs de chaque sujet initié à 0.
    nbre_max_sujets = max(G.sujets)
    effectifs_sujets = [0]*(nbre_max_sujets+1)

    noeuds_affectes = 0
    for (sujet, agent, rang) in G.edges.data('weight'):
        if rang == 0:  # 0 est la valeur du poids des premiers choix
            if G.nodes[sujet]["bipartite"] == TYPE_BIPARTITE_ELEVE:
                sujet, agent = agent, sujet

            if effectifs_sujets[sujet] < G.nodes[sujet]["c_max"]:
                M.add_edge(agent, sujet)
                sujet_incremente_statistiques(G, sujet, agent)
                effectifs_sujets[sujet] += 1
                noeuds_affectes += 1
    print("Démarrage rapide : ", noeuds_affectes, " affectés.")
    return M


def trouve_appariement_maximum(G, type="genereux"):  # Manlove, Algorithme 8.2 page 399
    """
    Algorithme principal pour trouver un appariement genereux maximal par défaut
    ou un appariement glouton si type est different de "genereux"
    Entree : le graphe du probleme
    Sortie : l'appariement en question
    """
    debut = time()
    G.sujets = {n for n, d in G.nodes(data=True) if d["bipartite"] == TYPE_BIPARTITE_SUJET}  # Liste sujets
    G.eleves = {n for n, d in G.nodes(data=True) if d["bipartite"] == TYPE_BIPARTITE_ELEVE}  # Liste eleves
    G.nbre_eleves = len(G.eleves)  # Retourne nombre d'eleve, utile pour zero_R
    M = appariement_demarrage_rapide(G)  # Liste de appariements
    k = len(M.edges)  # cardinalite de M

    while True:
        if type == "genereux":
            P = Min_Aug(G, k, M)
        else:
            P = Max_Aug(G, k, M)
        print(f"Etape {k} - Chemin augmente trouvé : ", P)
        if P is not None:
            M = augmente_M_selon_P(M, P, G)
        else:
            duree = time() - debut
            print("Durée : ", duree)
            return M, duree    # Un appariment maximum a ete trouvé

        k += 1           # M est actuellement un appariement gourmand d'ordre k


def profil_de_M(G, M):
    """ redonne le profil de M par rapport à G"""
    res = profil(NBRE_CHOIX)
    for lien in M.edges():
        rang = G.edges[lien[0], lien[1]]['weight']
        res = res + rang
    return res


def assigne_eleves_deja_affectes(G):
    """
        Selon la liste de G contenue dans 'eleves_deja_affectes',
        Attribue les eleves à leur sujet attribué
        Ou, s'iels n'en n'ont pas mais qu'iels sont dans cette liste,
        les assigne au SUJET_NON_INSCRIT.
    """
    for eleve, sujet in G.eleves_deja_affectes.items():
        if sujet == NON_ASSIGNE:
            assigne_eleve_au_sujet(G, eleve, SUJET_NON_INSCRIT)
        else:
            assigne_eleve_au_sujet(G, eleve, sujet)

    return G


def effectuer_affectations(G, M):
    """
    Remplis le champ "attribue" des eleves de G selon l'appariement M.
    Met a jour les effectifs des sujets
    """
    for n in M.nodes:
        if G.nodes[n]['bipartite'] == TYPE_BIPARTITE_ELEVE:  # si le noeud n est un eleve
            sujet_attribue = list(M.adj[n].keys())[0]
            assigne_eleve_au_sujet(G, n, sujet_attribue)


def principal(f_eleves, f_sujets, f_eleves_sortie="eleves_affectes", f_sujets_sortie="sujets_statistiques", type=TYPE_APPARIEMENT):
    """
    Programme principal qui :
    - 1. importe les donnees
    - 2. affectations les eleves aux sujets avec l'algo genereux :
    - 3. cherche des permutations améliorant la répartition des eleves :
        - 3a. genre : pas d'eleve isole
        - 3b. classe : pas trop d'eleves de la même classe
        - 3c. volee : pas trop d'eleves de la même volee
    - 4. statistiques
    - 5. exporte des resulats

    Entrees :
        fichier_eleves = (chemin +) nom des fichiers csv contenant la liste des eleves et leur choix
        fichier_sujets = (chemin +) nom des fichiers csv contenant la liste des sujets et leur choix
        type = type d'appariement (voir constantes.py), soit 'glouton', soit 'genereux'

    Sortie : deux fichiers :
        1) f_eleves_sortie, par défaut "eleves_affectations.csv" : fichier des eleves avec leur affectation
        2) f_sujets_sortie, par défaut "sujets_statistiques.csv") : fichier des sujets avec leur statistique
    """
    # 0. Initialisation des variables #################################################################
    sujets_supprimes = []  # sujets supprimes

    # 1. Importation des donnees ######################################################################
    G0 = Importation_csv.importer_donnees(f_eleves, f_sujets)  # Graphe contenant toutes les donnees
    G0 = assigne_eleves_deja_affectes(G0)

    # 2. Algorithme genereux ##########################################################################

    # Sortie des eleves deja attribues de l'algorithme car l'algorithme
    # peut defaire les liens.
    # On met alors a jour les capacites max et min associes.
    # Etape necessaire car l'algo genereux utilise les degres des noeuds
    # pour supprimer des sujets peu populaires
    G1 = Graph(subgraph(G0, G0.nodes - G0.eleves_deja_affectes))  # sans nx.Graph, le graphe est gele
    for e in G0.eleves_deja_affectes:
        sujet_attribue = G0.nodes[e]['attribue']
        G1.nodes[sujet_attribue]['c_max'] = G1.nodes[sujet_attribue]['c_max'] - 1
        G1.nodes[sujet_attribue]['c_min'] = G1.nodes[sujet_attribue]['c_min'] - 1

    # Sortie de l'algorithme les sujets qui n'ont aucune
    # chance d'atteindre l'effectif minmimum
    sujets_supprimes += suppression_sujets_non_populaires(G1)
    G2 = deepcopy(Graph(subgraph(G1, G1.nodes - sujets_supprimes)))
    M, duree = trouve_appariement_maximum(G2, type)  # affecte les eleves aux sujets

    while(liste_sujets_en_sous_effectifs(G2, M)) is not None:
        # Suppression pur et simple des sujets pas assez remplis.
        # Pas optimal s'il y en a plusieurs car
        # en reaffectant les eleves d'un sujet,
        # il se peut qu'on remplisse finalement
        # un des autres sujets pas assez remplis.
        # Mais c'est rare je pense. Je laisse ainsi pour le moment.
        # TODO ameliorer ce passage.
        sujets_a_suppr = liste_sujets_en_sous_effectifs(G2, M)
        sujets_supprimes += sujets_a_suppr
        print("Des sujets ne sont pas assez remplis : ", sujets_a_suppr)
        G2 = deepcopy(Graph(subgraph(G1, G1.nodes - sujets_a_suppr)))
        M, duree = trouve_appariement_maximum(G2, type)

    # sauvegardes des objets (uniquement pour les tests)
    # d = shelve.open('sauvegarde')
    # d['G2'] = G2
    # d['M'] = M
    # d.close()

    # recuperation des objets (uniquement pour les tests)
    # d = shelve.open('sauvegarde')
    # G2 = d['G2']
    # M = d['M']
    # d.close()

    # Statistique sur le profil produit par l'algorithme
    print("Le profil d'affectation des sujets est ", profil_de_M(G2, M))

    # On met a jour les affectations dans G0.
    effectuer_affectations(G0, M)
    # A ce stade G0 contient alors toutes les attributions.

    # 3. cherche des permutations améliorant la répartition des eleves :
    # TODO ce point reste a faire

    # 4. statisiques
    sortie_sujets = Exportation.creer_csv_statistiques_sujets(f_sujets_sortie, G0)

    # 5. exportation des resultats
    sortie_eleves = Exportation.ajoute_attributions_aux_fichiers_eleves(f_eleves, f_eleves_sortie, G0)

    return sortie_eleves, sortie_sujets, profil_de_M(G2, M), duree

# Pour tester uniquement ce module :
if __name__ == '__main__':
    principal("./exemples/eleves.csv", "./exemples/sujets.csv")

