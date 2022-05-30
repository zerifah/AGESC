import pandas   # pour importer les données des fichiers CSV
import datetime  # pour la date
from constantes import SUJET_NON_INSCRIT
from constantes import LISTES_CONSIGNE_A_RENDRE_A  # txt de la consigne des listes
from constantes import LISTES_CONSIGNE_JUSQUAU  # txt de la consigne des listes
from fpdf import FPDF  # pour générer un PDF


class Listes_des_participants(FPDF):
    """ Classe pour générer les listes de présences """

    # Titre
    date = datetime.date.today()
    annee = date.strftime("%Y")
    titre = "SET " + annee + " : Contrôle des présences"

    def header(self):
        """ En-tête """
        # Police
        self.set_font('Arial', '', 15)
        # Positionnement centre
        w = self.get_string_width(Listes_des_participants.titre) + 6
        self.set_x((297 - w) / 2)
        # Couleurs du cadre, du fond et du texte
        self.set_draw_color(80, 80, 80)
        self.set_fill_color(230, 230, 230)
        self.set_text_color(0, 0, 0)
        # Epaisseur du cadre (1 mm)
        self.set_line_width(0.3)
        # Texte
        self.cell(w, 9, Listes_des_participants.titre, 1, 1, 'C', 1)
        # Espacement vertical après
        self.ln(5)

    def footer(self):
        """ Pied de page"""
        # Position à 1.5 cm de bas de la page
        self.set_y(-15)
        # Police et couleur d'arrière-plan
        self.set_font('Arial', 'I', 6)
        self.set_text_color(128)
        # Numéro de page
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def titre_sujet(self, num, texte, res):
        """ Mise en forme du titre """
        # Police et couleur d'arrière-plan
        self.set_font('Arial', '', 15)
        self.set_fill_color(230, 230, 230)
        # Titre
        self.cell(0, 6, 'Sujet n°%d : %s (%r)' % (num, texte, res), 0, 1, 'L', 1)
        # Espacement vertical dessous
        self.ln(1)

    def tableau_eleves(self, pdf, sujet):
        hauteur_ligne = 5
        largeur_col1 = 85
        largeur_col2 = 16
        largeur_col3 = 16
        largeur_col4 = 297-largeur_col1-largeur_col2-10*largeur_col3-2*10
        # Times 12
        self.set_font('Times', '', 12)
        self.ln()
        # Mention in italics
        self.set_font('', 'B')

        # Consignes de départ
        consigne1 = "- En cas d'absence, inscrire le nombre de périodes de"
        consigne1 += " 45 minutes manquées par demi-journée"
        consigne2 = "- Feuille à rendre à " + LISTES_CONSIGNE_A_RENDRE_A
        consigne2 += " jusqu'au " + LISTES_CONSIGNE_JUSQUAU
        consigne3 = "- Veuillez également prendre note des consignes au recto"

        pdf.cell(270, 5, consigne1, 0, 0, 'L')
        self.ln()
        pdf.cell(270, 5, consigne2, 0, 0, 'L')
        self.ln()
        pdf.cell(270, 5, consigne3, 0, 0, 'L')
        self.ln(10)

        # Ligne d'entête
        pdf.cell(largeur_col1, hauteur_ligne, "Nom et prénom", 1, 0, 'L')
        pdf.cell(largeur_col2, hauteur_ligne, "Classe", 1, 0, 'C')
        pdf.cell(largeur_col3, hauteur_ligne, "Lu mat.", 1, 0, 'C')
        pdf.cell(largeur_col3, hauteur_ligne, "Lu a.-m", 1, 0, 'C')
        pdf.cell(largeur_col3, hauteur_ligne, "Ma mat.", 1, 0, 'C')
        pdf.cell(largeur_col3, hauteur_ligne, "Ma a.-m", 1, 0, 'C')
        pdf.cell(largeur_col3, hauteur_ligne, "Me mat.", 1, 0, 'C')
        pdf.cell(largeur_col3, hauteur_ligne, "Me a.-m", 1, 0, 'C')
        pdf.cell(largeur_col3, hauteur_ligne, "Je mat.", 1, 0, 'C')
        pdf.cell(largeur_col3, hauteur_ligne, "Je a.-m", 1, 0, 'C')
        pdf.cell(largeur_col3, hauteur_ligne, "Ve mat.", 1, 0, 'C')
        pdf.cell(largeur_col3, hauteur_ligne, "Ve a.-m", 1, 0, 'C')
        pdf.cell(largeur_col4, hauteur_ligne, "Total", 1, 0, 'C')
        self.ln(1+hauteur_ligne)

        # Lignes des participants
        self.set_font('', '')
        for eleve in sujet['participants']:
            pdf.cell(largeur_col1, hauteur_ligne, eleve['nom'], 1, 0, 'L')
            pdf.cell(largeur_col2, hauteur_ligne, eleve['classe'], 1, 0, 'C')
            pdf.cell(largeur_col3, hauteur_ligne, "", 1, 0, 'C')
            pdf.cell(largeur_col3, hauteur_ligne, "", 1, 0, 'C')
            pdf.cell(largeur_col3, hauteur_ligne, "", 1, 0, 'C')
            pdf.cell(largeur_col3, hauteur_ligne, "", 1, 0, 'C')
            pdf.cell(largeur_col3, hauteur_ligne, "", 1, 0, 'C')
            pdf.cell(largeur_col3, hauteur_ligne, "", 1, 0, 'C')
            pdf.cell(largeur_col3, hauteur_ligne, "", 1, 0, 'C')
            pdf.cell(largeur_col3, hauteur_ligne, "", 1, 0, 'C')
            pdf.cell(largeur_col3, hauteur_ligne, "", 1, 0, 'C')
            pdf.cell(largeur_col3, hauteur_ligne, "", 1, 0, 'C')
            pdf.cell(largeur_col4, hauteur_ligne, "", 1, 0, 'C')
            self.ln(hauteur_ligne)

    def affiche_sujet(self, pdf, sujet):
        self.add_page()
        self.titre_sujet(sujet['sujet'], sujet['titre'], sujet['res'])
        self.tableau_eleves(pdf, sujet)

    @staticmethod
    def importer_donnees(fichier_eleves, fichier_sujets):
        """
        Importe :
        -   le fichier csv contenant les données des élèves avec leur attribution
        -   le fichier csv contenant les données des sujets
        """
        lecture_sujets = pandas.read_csv(fichier_sujets)
        lecture_eleves = pandas.read_csv(fichier_eleves)

        sujets = {}
        sujet_non_inscrit_ok = False
        for ligne in lecture_sujets.itertuples():
            titre = ligne.titre
            # Remplacement caractères problématiques pour l'encodage PDF
            if not pandas.isna(titre):
                titre = titre.replace('’', "'")
                titre = titre.replace('‘', "'")
                titre = titre.replace('–', "-")

            id_sujet = int(ligne.sujet)
            if id_sujet == SUJET_NON_INSCRIT:
                sujet_non_inscrit_ok = True

            sujets[id_sujet] = {
                    'sujet': id_sujet,
                    'titre': titre,
                    'res': ligne.res,
                    'participants': []}
        # Si le sujet des non-inscrits n'était pas dans le fichier
        # On l'ajoute
        if not sujet_non_inscrit_ok:
            sujets[SUJET_NON_INSCRIT] = {
                'sujet': SUJET_NON_INSCRIT,
                'titre': 'Sans sujet',
                'res': 'Direction',
                'participants': []}

        for ligne in lecture_eleves.itertuples():
            eleve = {
                'eleve': int(ligne.eleve),
                'nom': ligne.nom + " " + ligne.prenom,
                'classe': ligne.classe}
            sujet_attribue = int(ligne.attribue)
            sujets[sujet_attribue]['participants'].append(eleve)

        return sujets

    @staticmethod
    def creer_listes_de_controle(fichier_eleves, fichier_sujets):
        """
        Créer un PDF avec les listes de contrôles à partir des 2 fichiers CSV
        contenant
        1) la liste des sujets
        2) la liste des élèves une fois affectés
        Note : l'ordre des élèves sera dans l'ordre du fichier CSV.
        """

        # Créaction du document PDF
        pdf = Listes_des_participants(orientation='L', unit='mm', format='A4')

        # Importation des données
        donnees = pdf.importer_donnees(fichier_eleves, fichier_sujets)

        # Mise en place du titre
        pdf.set_title(Listes_des_participants.titre)

        # Page par sujet
        for sujet in donnees.values():
            pdf.affiche_sujet(pdf, sujet)

        # Exportation en PDF
        pdf.output('listes_des_participants.pdf', 'F')
        print(
            "Les listes d'absences ont été exportées",
            "dans le fichier listes_des_participants.pdf")

# Pour tester ce module, décommenter la ligne suivante
# Listes_des_participants().creer_listes_de_controle('./exemples/eleves_affectes.csv', './exemples/sujets.csv')
