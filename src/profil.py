from copy import copy
from copy import deepcopy


class profil:
    """
    Classe des profils definie ainsi :
    si p.value = [7, 6, 5], et p un chemin, cela signifie que :
        il y a 7 liens de poids 1 dans le chemin p.
        il y a 6 liens de poids 2 dans le chemin p.
        il y a 5 liens de poids 3 dans le chemin p.

    """
    def __init__(self, longueur):
        self.val = [0]*longueur

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, val):
        self._val = val

    def __add__(self, other):
        res = deepcopy(self)
        res.val[other] = res.val[other] + 1

        return res

    def __sub__(self, other):
        res = copy(self)
        res.val[other] = res.val[other] - 1
        return res

    def __getitem__(self, k):
        """ retourne valeur du profil pour le poids 1"""
        return self.val[k-1]

    def __gt__(self, other):
        """

        Opérateur >L pour comparer deux profils X et Y :
        Compare d'abord les premiers éléments des deux profils.
        Si celui de X est plus grand celui de Y,
        alors le profil est >L que l'autre.
        S'ils sont égaux, on regarde l'élément suivant et ainsi de suite...
        Cet opérateur est utile pour l'algorithme glouton maximum,
        car on cherche à maximiser le nombre de premiers choix.

        Exemple :
            X = <2, 1, 3>
            Y = <2, 0, 4>
            Ici, X > Y

        """
        k = 1
        nbre_choix = len(self.val)
        while self[k] == other[k] and k < nbre_choix:
            k += 1
        return self[k] > other[k]

    def __lt__(self, other):
        """
        Opérateur <R pour comparer deux profils X et Y :
        Compare d'abord les derniers éléments des deux profils.
        Si celui de X est plus petit que celui de Y,
        alors le profil est <R que l'autre.
        S'ils sont égaux, on regarde l'élément précédent et ainsi de suite...
        Cet opérateur est utile pour l'algorithme genereux maximum,
        car on cherche à minimiser le nombre de derniers choix.

        Exemple :
            X = <2, 1, 3>
            Y = <2, 0, 4>
            Ici, X < Y
        """
        nbre_choix = len(self.val)
        while self[nbre_choix] == other[nbre_choix] and nbre_choix > 1:
            nbre_choix -= 1
        return self[nbre_choix] < other[nbre_choix]

    def __eq__(self, other):
        return self.val == other.val

    def __str__(self):
        return str(self.val)

    def zero(longueur):
        return profil(longueur)

    def zero_R(longueur, valmax):
        """
            Retourne le profil zero O'_R pour l'operation <R
            valmax doit etre le nombre d'eleves plus 1
        """
        res = profil(longueur)
        res.val[longueur-1] = valmax
        return res

    def max_L(liste_de_profil):
        """ Retourne le profil maximum selon >L de la liste recue """
        profil_max = liste_de_profil[0]
        indice_max = 0
        indice = 0
        for e in liste_de_profil:
            if e > profil_max:
                profil_max = e
                indice_max = indice
            indice += 1
        return profil_max, indice_max

    def min_R(liste_de_profil):
        """ Retourne le profil minimum selon <R de la liste recue """
        profil_min = liste_de_profil[0]
        indice_min = 0
        indice = 0

        for e in liste_de_profil:
            if e < profil_min:
                profil_min = e
                indice_min = indice
            indice += 1
        return profil_min, indice_min
