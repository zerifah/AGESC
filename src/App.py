from tkinter import *
from tkinter import filedialog
import tkinter
import affectations
from constantes import SUJET_NON_INSCRIT
from listes_des_participants import Listes_des_participants


class Zone_Parcourir:
    """
    Classe pour définir un bouton 'Parcourir'
    avec une zone de texte pour afficher le chemin
    et stocke dans le champ 'fichier' le fichier choisi.
    """

    def __init__(self, cadre_parent, texte_du_bouton):
        self.fichier = ''
        self.cadre = Frame(cadre_parent)
        self.bouton = Button(
                self.cadre,
                text=texte_du_bouton,
                font=App.police_bouton,
                command=self.__parcourir)
        self.texte_fichier = Label(
                self.cadre,
                text="",
                fg="blue",
                bg="white",
                anchor="w")
        self.bouton.pack(side=LEFT, padx=10, pady=1)
        self.texte_fichier.pack(side=LEFT, fill='x', ex=True, padx=10, pady=1)
        self.cadre.pack(side=TOP, fill='x', padx=0, pady=1)

    def __parcourir(self):
        """
        Action des boutons parcourir.
        Le fichier sélectionné est stocké dans nom_du_fichier
        (avec son chemin). Le texte indiquant le chemin du fichier
        sélectionné est mis à jour.
        """
        self.fichier = filedialog.askopenfilename(
                initialdir="",
                title="Sélectionnez le fichier",
                filetypes=(
                    ("Fichier CSV", "*.csv*"),
                    ("Tous les fichiers", "*.*")))
        self.texte_fichier.configure(text="Fichier ouvert: " + self.fichier)


class Module_Affectation:
    """
    Module d'une fenêtre contenant
    - la consigne
    - les boutons 'parcourir'
    - le bouton 'lancer l'algoritme'
    - la commande pour lancer l'algorithme
    """

    consigne = "Sélectionnez les fichiers CSV contenant "
    consigne += "les sujets et les choix des élèves, puis"
    consigne += "cliquez sur le bouton pour lancer l'algorithme."
    txt_attention = "Attention, il faut que chaque "
    txt_attention += "éleve ait soit trois choix, soit un sujet attribué.\n"
    txt_attention += "Les élèves non inscrit·e·s sont "
    txt_attention += "par défaut attribué·e·s au sujet n°"
    txt_attention += str(SUJET_NON_INSCRIT) + "."

    def __init__(self, cadre_parent):
        self.cadre = LabelFrame(
            cadre_parent,
            text="Affectations des élèves",
            padx=10,
            pady=10,
            font=App.police_titre_encadre)
        self.cadre.pack(padx='30', pady='10')

        self.consigne_fichier = Label(
            self.cadre,
            text=Module_Affectation.consigne,
            width=1200,
            wraplength=1200,
            justify='left',
            anchor="w",
            font=App.police_corps_de_texte)

        self.consigne_fichier_attention = Label(
            self.cadre,
            text=Module_Affectation.txt_attention,
            width=1200,
            wraplength=1200,
            fg="red",
            anchor="w",
            justify='left',
            font=App.police_corps_de_texte)

        self.bouton_affectation = Button(
                self.cadre,
                text="Lancer l'algorithme d'affectation",
                font=App.police_bouton,
                command=self.__algorithme)

        self.texte_algorithme_reussi = Label(
                self.cadre,
                text="",
                font=App.police_algo_reussi,
                justify='left',
                anchor="w")

        # Affichage
        self.consigne_fichier.pack(fill='x', padx=10, pady=1)
        self.consigne_fichier_attention.pack(fill='x', padx=10, pady=10)
        self.sujets = Zone_Parcourir(self.cadre, "Sélectionnez les sujets...")
        self.eleves = Zone_Parcourir(self.cadre, "Sélectionnez les éleves...")
        self.bouton_affectation.pack(padx=10, pady=1, anchor='w')
        self.texte_algorithme_reussi.pack(padx=10, pady=1, anchor='w')

    def __algorithme(self):
        """ Lance l'algorithme d'affectation"""
        self.texte_algorithme_reussi.configure(
            text="Algorithme en cours, cela peut prendre 2-3 minutes...",
            fg="blue")
        self.cadre.update()
        try:
            f_eleves, f_sujets, profil, duree = affectations.principal(
                    self.eleves.fichier,
                    self.sujets.fichier)
            msg = "Terminé avec succès en " + str(round(duree, 3))
            msg += " secondes! " + "(Profil = " + str(profil) + ")\n"
            msg += "Les résultats de trouvent dans les fichiers :\n- "
            msg += str(f_eleves) + "\n- "
            msg += str(f_sujets)
            self.texte_algorithme_reussi.configure(text=msg, fg="green")
        except Exception as e:
            self.texte_algorithme_reussi.configure(
                text="L'algorithme a rencontré une erreur : " + str(e) +
                     "\nVérifiez la consistance des données.",
                fg="red")

        self.cadre.update()
        canevas = self.cadre.master.master
        # Adaptation de la zone de défilement à la nouvelle taille des cadres
        canevas.configure(scrollregion= canevas.bbox("all"))              


class Module_listes_participants:
    """
    Module d'une fenêtre contenant
    - la consigne
    - les boutons 'parcourir'
    - le bouton 'Créer listes'
    - la commande pour générer les listes en PDF
    """

    consigne = "Sélectionner le fichier des sujets et celui des élèves"
    consigne += " avec les affectations.\n"
    consigne += "L'ordre des élèves et des sujets dépend "
    consigne += "de l'ordre des lignes dans les fichiers csv."
    txt_attention = "Attention, chaque élève doit être attribué·e à un sujet."

    def __init__(self, cadre_parent):
        self.cadre = LabelFrame(
            cadre_parent,
            text="Création des listes des participants par sujet",
            padx=10,
            pady=10,
            font=App.police_titre_encadre)

        self.consigne = Label(
                self.cadre,
                text=Module_listes_participants.consigne,
                width=1200,
                wraplength=1200,
                justify='left',
                anchor="w",
                font=App.police_corps_de_texte)

        self.consigne_fichier_attention = Label(
            self.cadre,
            text=Module_listes_participants.txt_attention,
            width=1200,
            wraplength=1200,
            fg="red",
            anchor="w",
            justify='left',
            font=App.police_corps_de_texte)

        self.bouton_creer_pdf = Button(
            self.cadre,
            text="Créez les listes en PDF",
            font=App.police_bouton,
            command=self.__creer_listes)
        self.texte_listes_pdf_reussi = Label(
                self.cadre,
                text="",
                font=App.police_algo_reussi,
                justify='left',
                anchor="w")

        # Affichage
        self.consigne.pack(fill='x', padx=10, pady=10)
        self.consigne_fichier_attention.pack(fill='x', padx=10, pady=10)
        self.sujets = Zone_Parcourir(self.cadre, "Sélectionnez les sujets...")
        self.eleves = Zone_Parcourir(self.cadre, "Sélectionnez les éleves...")
        self.bouton_creer_pdf.pack(padx=10, pady=1, anchor='w')
        self.texte_listes_pdf_reussi.pack(padx=10, pady=1, anchor='w')
        self.cadre.pack(padx='30', pady='10', fill='x')

    def __creer_listes(self):
        """ Lance la création des listes des participants"""

        msg = "Exportation des listes réussie --> listes_des_participants.pdf."

        try:
            Listes_des_participants().creer_listes_de_controle(
                 self.eleves.fichier,
                 self.sujets.fichier)
            self.texte_listes_pdf_reussi.configure(text=msg, fg="green")

        except Exception as e:
            self.texte_listes_pdf_reussi.configure(
                text="L'exportation a échouée : " + str(e) + "\nVérifiez la consistance des données.",
                fg="red")

        self.cadre.update()
        canevas = self.cadre.master.master
        # Adaptation de la zone de défilement à la nouvelle taille des cadres
        canevas.configure(scrollregion= canevas.bbox("all"))         


class App:
    """
    Application qui permet de choisir les fichiers sources
    pour lancer l'algorithme  d'affectation
    ou générer les listes de présence.
    """

    # Définitions des polices
    police_bouton = ('courier', 16)
    police_titre_encadre = ("courier", 20, 'bold')
    police_corps_de_texte = ('courier', 16)
    police_algo_reussi = ('courier', 16)

    def __init__(self):

        # Fenetre principale
        self.fenetre = Tk()
        self.fenetre.title('Organisation de la SET')
        hauteur_ecran = self.fenetre.winfo_screenheight()
        largeur_ecran = self.fenetre.winfo_screenwidth()
        self.fenetre.geometry(str(largeur_ecran) + "x" + str(hauteur_ecran))

        # Préparation du canevas pour la barre de défilement
        self.canevas =  tkinter.Canvas(self.fenetre)
        defilement_y =  tkinter.Scrollbar(self.fenetre, orient="vertical", command=self.canevas.yview)
        cadre_pour_defilement =  tkinter.Frame(self.canevas)
        self.canevas.create_window(0, 0, anchor='nw', window=cadre_pour_defilement)

        # Ajout des modules dans le cadre défilant
        Module_Affectation(cadre_pour_defilement)
        Module_listes_participants(cadre_pour_defilement)
        
        # S'assure que tout est sélectionné
        # avant de configurer la région de défilement
        self.canevas.update_idletasks()
        self.canevas.configure(scrollregion=self.canevas.bbox('all'),
            yscrollcommand=defilement_y.set)
        self.canevas.pack(fill='both', expand=True, side='left')
        defilement_y.pack(fill='y', side='right')

        self.fenetre.mainloop()

App()
