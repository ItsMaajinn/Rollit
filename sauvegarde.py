from fltk import *
import ast
import os
import os
from tkinter import Tk, filedialog

def load_save(file_path):
    """
    Fonction qui permet de charger les informations sauvegardées depuis un fichier
    :param file_path: Chemin complet du fichier de sauvegarde
    :return: Un dictionnaire contenant les informations de la partie
    """
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas.")
        return None

    with open(file_path, 'r', encoding='utf8') as save_file:
        data = save_file.readlines()

    if len(data) < 5:
        print("Le fichier de sauvegarde est corrompu ou incomplet.")
        return None

    try:
        grille = eval(data[0].strip())
        tour = int(data[1].strip())
        nb_joueurs = int(data[2].strip())
        taille_grille = int(data[3].strip())
        couleurs = eval(data[4].strip())

        return {
            "grille": grille,
            "tour": tour,
            "nb_joueurs": nb_joueurs,
            "taille_grille": taille_grille,
            "couleurs": couleurs
        }
    except Exception as e:
        print(f"Erreur lors du chargement de la sauvegarde : {e}")
        return None
def open_save_folder():
    # Open a file dialog to select a file in the save folder
    root = Tk()
    root.withdraw()  # Hide the root window

    # Get the save folder path (modify as needed)
    save_folder_path = os.path.expanduser("~/sauvegarde")

    # Ensure the save folder exists
    if not os.path.exists(save_folder_path):
        print("Le dossier 'sauvegarde' n'existe pas.")
        return None

    # Open the file dialog in the save folder
    file_path = filedialog.askopenfilename(initialdir=save_folder_path, title="Sélectionnez un fichier")

    # Check if a file was selected
    if file_path:
        return file_path
    else:
        return None


def partie_en_cours(grille, tour, nb_joueurs, taille_grille, couleurs):
    # Configuration
    LARGEUR_FENETRE, HAUTEUR_FENETRE = 854, 480
    TAILLE_GRILLE = taille_grille
    MARGE = 4
    TAILLE_CASE = (HAUTEUR_FENETRE - MARGE) // TAILLE_GRILLE
    MARGE_GAUCHE_DROITE = (LARGEUR_FENETRE - (TAILLE_CASE * TAILLE_GRILLE)) // 2
    bordureDroite = MARGE_GAUCHE_DROITE + (TAILLE_GRILLE * TAILLE_CASE)
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)

    # Dessiner la grille et les pions
    def dessiner_grille(grille, couleurs):
        coul = changerCouleur(grille, couleurs)
        for i in range(TAILLE_GRILLE):
            for j in range(TAILLE_GRILLE):
                x1 = MARGE_GAUCHE_DROITE + j * TAILLE_CASE
                y1 = 4 + i * TAILLE_CASE
                x2, y2 = x1 + TAILLE_CASE, y1 + TAILLE_CASE
                rectangle(x1, y1, x2, y2, remplissage=coul[0])
                if grille[i][j]:  # Si une couleur est présente
                    image((x1 + x2) // 2, (y1 + y2) // 2, grille[i][j],
                          largeur=TAILLE_CASE, hauteur=TAILLE_CASE, ancrage="center", tag="pion")

    # Placer un pion sur la grille
    def placer_pion(grille, ligne, colonne, couleur):
        grille[ligne][colonne] = couleur

    def tabScore(grille, couleurs):
        score = [0] * len(couleurs)
        for i in range(TAILLE_GRILLE):
            for j in range(TAILLE_GRILLE):
                if grille[i][j] is not None:  # Si la case n'est pas vide
                    index = couleurs.index(grille[i][j])  # On récupère l'index de la couleur
                    score[index] += 1  # On incrémente le score

        return score
    
    def bouleNextTo(grille, ligne, colonne):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # 8 directions possibles
        for d_l, d_c in directions:
            if 0 <= ligne + d_l < TAILLE_GRILLE and 0 <= colonne + d_c < TAILLE_GRILLE:
                if grille[ligne + d_l][colonne + d_c] is not None:
                    return True
        return False

    def affichageScore(score, couleurs):
        rectangle(bordureDroite, 4, LARGEUR_FENETRE - 1, TAILLE_CASE + 4, couleur="black", remplissage="#ECCFC3")
        rectangle(bordureDroite, TAILLE_CASE + 4, LARGEUR_FENETRE - 1, HAUTEUR_FENETRE - 4, couleur="black", remplissage="#ECCFC3")
        texte((LARGEUR_FENETRE + bordureDroite) // 2, 32, "Scores", police="Arial", taille=20, ancrage="center")
        scoreTrie = sorted(zip(score, couleurs), reverse=True)

        for i, (s, c) in enumerate(scoreTrie):
            image((LARGEUR_FENETRE + bordureDroite) // 2 - 60, 70 + i * 60, c, largeur=50, hauteur=50, ancrage="nw")
            texte((LARGEUR_FENETRE + bordureDroite) // 2 + 20, 80 + i * 60, str(s), police="Arial", taille=20, ancrage="nw")

    def affichageGauche(couleurs, nb_joueurs, tour):
        couleur = couleurs[tour % nb_joueurs]
        rectangle(0, 4, MARGE_GAUCHE_DROITE, TAILLE_CASE + 4, couleur="black", remplissage="#ECCFC3")
        texte(MARGE_GAUCHE_DROITE // 2 - 30, 32, f"Tour :", police="Arial", taille=20, ancrage="center")
        image(MARGE_GAUCHE_DROITE // 2 + 30, 32, couleur, largeur=50, hauteur=50, ancrage="center")

        rectangle(0, HAUTEUR_FENETRE - TAILLE_CASE - 4, MARGE_GAUCHE_DROITE, HAUTEUR_FENETRE - 4, couleur="black", remplissage="#ECCFC3")
        texte(MARGE_GAUCHE_DROITE // 2, HAUTEUR_FENETRE - 32, f"{tour + nb_joueurs} / {TAILLE_GRILLE ** 2}", police="Arial", taille=20, ancrage="center")

    def fin(tour, grille, nb_joueurs):
        if tour == (TAILLE_GRILLE ** 2) - nb_joueurs:
            score = tabScore(grille, couleurs)
            scoreTrie = sorted(zip(score, couleurs), reverse=True)
            return (True, scoreTrie[0])  # Retourne True et le gagnant
        return (False, None)  # Sinon, continue le jeu

    def changerCouleur(grille, couleurs):
        score = tabScore(grille, couleurs)
        scoreTrie = sorted(zip(score, couleurs), reverse=True)
        if scoreTrie[0][1] == "assets/pionRouge.png":
            return ("#ECCFC3", "#ECB8A5")
        elif scoreTrie[0][1] == "assets/pionBleu.png":
            return ("#ADD7F6", "#87BFFF")
        elif scoreTrie[0][1] == "assets/pionJaune.png":
            return ("#F2E29F", "#FADF7F")
        elif scoreTrie[0][1] == "assets/pionVert.png":
            return ("#C6EBBE", "#A9DBB8")
        else:
            return ("#FFFFFF", "#000000")

    def affichageV(gagnant):
        texte(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2, f"Le gagnant est {gagnant[1]}", police="Arial", taille=30, ancrage="center")

    def jouer(tour):  # Passer tour en paramètre ici
        while fin(tour, grille, nb_joueurs)[0] is not True:
            ev = donne_ev()
            tev = type_ev(ev)

            if tev == "Quitte":
                break
            elif tev == "ClicGauche":
                x, y = abscisse(ev), ordonnee(ev)
                ligne, colonne = (y - 4) // TAILLE_CASE, (x - MARGE_GAUCHE_DROITE) // TAILLE_CASE
                if 0 <= ligne < TAILLE_GRILLE and 0 <= colonne < TAILLE_GRILLE:
                    if grille[ligne][colonne] is None:
                        if bouleNextTo(grille, ligne, colonne):# Si la case est vide
                            couleur = couleurs[tour % nb_joueurs]
                            placer_pion(grille, ligne, colonne, couleur)
                            tour += 1
            efface_tout()
            dessiner_grille(grille, couleurs)
            affichageScore(tabScore(grille, couleurs), couleurs)
            affichageGauche(couleurs, nb_joueurs, tour)
            mise_a_jour()

        ferme_fenetre()
        cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
        affichageV(fin(tour, grille, nb_joueurs)[1])
        attend_ev()

    # Lancer la partie en cours
    jouer(tour)


