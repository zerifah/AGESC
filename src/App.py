from tkinter import *
from tkinter import filedialog
import affectations
from constantes import SUJET_NON_INSCRIT
import listes_des_participants


class App:
    """
    Application qui permet de choisir les fichiers sources
    pour lancer l'algorithme  d'affectation
    ou générer les listes de présence.
    """
    ###########################################################################
    #                           CONSTANTES                                    #
    ###########################################################################

    txt_consigne_fichier = "Sélectionnez les fichiers CSV contenant "
    txt_consigne_fichier += "les sujets et les choix des élèves."
    txt_consigne_attention = "Attention, il faut que chaque "
    txt_consigne_attention += "éleve ait soit trois choix, soit un sujet attribué.\n"
    txt_consigne_attention += "Les élèves non inscrit·e·s sont "
    txt_consigne_attention += "par défaut attribué·e·s au sujet n°" + str(SUJET_NON_INSCRIT) + "."
    txt_consigne_listes_pdf = "Il faut sélectionner le fichier des élèves"
    txt_consigne_listes_pdf += " avec les attributions.\n"
    txt_consigne_listes_pdf += "L'ordre des élèves et des sujets dépend "
    txt_consigne_listes_pdf += "de l'ordre des fichiers csv."
    police1 = ('courier', 15)

    def __init__(self):
        self.nom_du_fichier_sujets = ""
        self.nom_du_fichier_eleves = ""

        # Fenetre principale
        self.fenetre = Tk()
        self.fenetre.title('Organisation de la SET')
        hauteur_ecran = self.fenetre.winfo_screenheight()
        largeur_ecran = self.fenetre.winfo_screenwidth()
        self.fenetre.geometry(str(largeur_ecran) + "x" + str(hauteur_ecran))

        # Selection des fichiers
        encadre1 = LabelFrame(
            self.fenetre,
            text="1. Importation des fichiers CSV",
            padx=10,
            pady=10,
            font=("Courier", 18))
        encadre1.pack(padx='30', pady='10')
        cadre_sujet = Frame(encadre1)
        cadre_eleve = Frame(encadre1)

        self.texte_fichier_sujet = Label(
                                    cadre_sujet,
                                    text="",
                                    fg="blue",
                                    bg="white",
                                    anchor="w")

        consigne_fichier = Label(
                                encadre1,
                                text=App.txt_consigne_fichier,
                                width=1200,
                                wraplength=1200,
                                justify='left',
                                anchor="w",
                                font=App.police1)

        consigne_fichier_attention = Label(
                                            encadre1,
                                            text=App.txt_consigne_attention,
                                            width=1200,
                                            wraplength=1200,
                                            fg="red",
                                            anchor="w",
                                            justify='left',
                                            font=App.police1)

        self.texte_fichier_eleve = Label(
                                    cadre_eleve,
                                    text="",
                                    fg="blue",
                                    bg="white",
                                    anchor="w")

        bouton_sujet = Button(
                                cadre_sujet,
                                text="Selectionnez le fichier des sujets",
                                command=self.__parcourir_sujet)

        bouton_eleve = Button(
                                cadre_eleve,
                                text="Selectionnez le fichier des éleves",
                                command=self.__parcourir_eleve)

        consigne_fichier.pack(fill='x', padx=10, pady=1)
        consigne_fichier_attention.pack(fill='x', padx=10, pady=10)
        bouton_sujet.pack(side=LEFT, padx=10, pady=1)
        self.texte_fichier_sujet.pack(side=LEFT, fill='x', expand=True, padx=10, pady=1)
        bouton_eleve.pack(side=LEFT, padx=10, pady=1)
        self.texte_fichier_eleve.pack(side=LEFT, fill='x', ex=True, padx=10, pady=1)
        cadre_sujet.pack(side=TOP, fill='x', padx=10, pady=1)
        cadre_eleve.pack(side=TOP, fill='x', padx=10, pady=1)

        # Encadre 2
        encadre2 = LabelFrame(
            self.fenetre,
            text="2. Affectez les élèves aux sujets",
            padx=10,
            pady=10,
            font=("Courier", 18))
        encadre2.pack(padx='30', pady='10', fill='x')

        bouton_go = Button(
                        encadre2,
                        text="Lancer l'algorithme d'affectation",
                        command=self.__algorithme)

        self.texte_algorithme_reussi = Label(
                encadre2,
                text="",
                font=('courier', 18),
                justify='left',
                anchor="w")

        bouton_go.pack(padx=10, pady=1, anchor='w')
        self.texte_algorithme_reussi.pack(padx=10, pady=1, anchor='w')

        # Encadre 3
        encadre3 = LabelFrame(
            self.fenetre,
            text="3. Créez les listes des participants par sujet",
            padx=10,
            pady=10,
            font=("Courier", 18))
        encadre3.pack(padx='30', pady='10', fill='x')
        txt_consigne_listes_pdf = Label(
                encadre3,
                text=App.txt_consigne_listes_pdf,
                width=1200,
                wraplength=1200,
                justify='left',
                anchor="w",
                font=App.police1)
        txt_consigne_listes_pdf.pack(fill='x', padx=10, pady=10)

        bouton_creer_pdf = Button(
                encadre3,
                text="Créez les listes",
                command=self.__creer_listes)
        bouton_creer_pdf.pack(padx=10, pady=1, anchor='w')

        self.texte_listes_pdf_reussi = Label(
                encadre3,
                text="",
                font=('courier', 18),
                justify='left',
                anchor="w")
        self.texte_listes_pdf_reussi.pack(padx=10, pady=1, anchor='w')

        self.fenetre.mainloop()

    def __parcourir_sujet(self):
        """ Action du bouton parcourir les sujets"""
        self.nom_du_fichier_sujets = filedialog.askopenfilename(
                                            initialdir="",
                                            title="Sélectionnez le fichier",
                                            filetypes=((
                                                    "Fichier CSV",
                                                    "*.csv*"),
                                                ("Tous les fichiers",
                                                    "*.*")))
        self.texte_fichier_sujet.configure(text="Fichier ouvert: " + self.nom_du_fichier_sujets)

    def __parcourir_eleve(self):
        """ Action du bouton parcourir les élèves"""
        self.nom_du_fichier_eleves = filedialog.askopenfilename(
                                            initialdir="",
                                            title="Sélectionnez le fichier",
                                            filetypes=(
                                                ("Fichier CSV", "*.csv*"),
                                                ("Tous les fichiers", "*.*")))
        self.texte_fichier_eleve.configure(text="Fichier ouvert: " + self.nom_du_fichier_eleves)

    def __algorithme(self):
        """ Lance l'algorithme d'affectation"""
        self.nom_du_fichier_sujets
        self.nom_du_fichier_eleves
        self.texte_algorithme_reussi.configure(
            text="Algorithme en cours, cela peut prendre 2-3 minutes...",
            fg="blue")
        self.fenetre.update()
        try:
            f_eleves, f_sujets, profil, duree = affectations.principal(
                    self.nom_du_fichier_eleves,
                    self.nom_du_fichier_sujets)
            msg = "Terminé avec succès en " + str(round(duree, 3)) + " secondes! "
            msg += "(Profil = " + str(profil) + ")\n"
            msg += "Les résultats de trouvent dans les fichiers :\n- "
            msg += str(f_eleves) + "\n- "
            msg += str(f_sujets)
            self.texte_algorithme_reussi.configure(text=msg, fg="green")
            self.fenetre.update()
        except Exception as e:
            self.texte_algorithme_reussi.configure(
                text="L'algorithme a rencontré une erreur : " + str(e) +
                     "\nVérifiez la consistance des données.",
                fg="red")
            self.fenetre.update()

    def __creer_listes(self):
        """ Lance la créaction des listes des participants"""
        self.nom_du_fichier_sujets
        self.nom_du_fichier_eleves
        msg = "Exportation des listes réussie --> listes_des_participants.pdf."

        try:
            listes_des_participants.Listes_des_participants().creer_listes_de_controle(
                 self.nom_du_fichier_eleves,
                 self.nom_du_fichier_sujets)
            self.texte_listes_pdf_reussi.configure(text=msg, fg="green")
            self.fenetre.update()
        except Exception as e:
            self.texte_listes_pdf_reussi.configure(
                text="L'exportation a échouée : " + str(e) + "\nVérifiez la consistance des données.",
                fg="red")
            self.fenetre.update()

App()
