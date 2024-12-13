from fltk import *
import wx


# Interface pour choisir le nombre de joueurs
app = wx.App()
nb_joueurs = int(wx.GetTextFromUser("Nombre de joueurs (entre 2 et 4)"))

# Configuration
LARGEUR_FENETRE, HAUTEUR_FENETRE = 854, 480
TAILLE_GRILLE = 8
TAILLE_CASE = (HAUTEUR_FENETRE - 4) // TAILLE_GRILLE
MARGE_GAUCHE_DROITE = (LARGEUR_FENETRE - (TAILLE_CASE * TAILLE_GRILLE)) // 2
COULEURS = ["assets/pionRouge.png", "assets/pionBleu.png", "assets/pionJaune.png", "assets/pionVert.png"][:nb_joueurs]
bordureDroite = MARGE_GAUCHE_DROITE + (TAILLE_GRILLE * TAILLE_CASE)
cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)

# Création de la grille
def creer_grille():
    return [[None for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)]

# Dessiner la grille et les pions
def dessiner_grille(grille):
    for i in range(TAILLE_GRILLE):
        for j in range(TAILLE_GRILLE):
            x1 = MARGE_GAUCHE_DROITE + j * TAILLE_CASE
            y1 = 4 + i * TAILLE_CASE
            x2, y2 = x1 + TAILLE_CASE, y1 + TAILLE_CASE
            rectangle(x1, y1, x2, y2, remplissage="#ECCFC3")
            if grille[i][j]:  # Si une couleur est présente
                image((x1 + x2) // 2, (y1 + y2) // 2, grille[i][j],
                      largeur=TAILLE_CASE, hauteur=TAILLE_CASE, ancrage="center", tag="pion")

# Placer un pion sur la grille
def placer_pion(grille, ligne, colonne, couleur):
    grille[ligne][colonne] = couleur




def tabScore(grille, lenGrille, couleurs):
    score = [0, 0, 0, 0]
    for i in range(lenGrille):
        for j in range(lenGrille):
            if grille[i][j] is not None:
                index = couleurs.index(grille[i][j])
                score[index] += 1

    return score

def affichageScore(score, couleursTab):
    rectangle(bordureDroite, 4, LARGEUR_FENETRE - 1, TAILLE_CASE + 4, couleur="black", remplissage="#ECB8A5")
    rectangle(bordureDroite, TAILLE_CASE + 4, LARGEUR_FENETRE - 1, HAUTEUR_FENETRE - 4, couleur="black",
              remplissage="#ECCFC3")
    texte((LARGEUR_FENETRE + bordureDroite) // 2, 32, "Scores", police="Arial", taille=20, ancrage="center")
    scoreTrie = []

    for i, (c, s) in enumerate(zip(couleursTab, score)):
        scoreTrie.append((s, c))

    scoreTrie.sort(reverse=True)

    for  i in range(len(scoreTrie)):
        image((LARGEUR_FENETRE + bordureDroite) // 2 - 60, 70 + i * 60, scoreTrie[i][1], largeur=50, hauteur=50,
              ancrage="nw")
        texte((LARGEUR_FENETRE + bordureDroite) // 2 + 20, 80 + i * 60, str(scoreTrie[i][0]), police="Arial", taille=20,
              ancrage="nw")

# Vérification dans une direction (optimisée)
def verifier_direction(grille, ligne, colonne, couleur, d_l, d_c):
    a_encadrer = []
    l, c = ligne + d_l, colonne + d_c
    while 0 <= l < TAILLE_GRILLE and 0 <= c < TAILLE_GRILLE:
        case = grille[l][c]
        if case is None:  # Si vide, arrêt
            return []
        if case == couleur:  # Si couleur identique, valide
            return a_encadrer
        a_encadrer.append((l, c))
        l, c = l + d_l, c + d_c
    return []

# Encadrer les pions
def encadrer_pions(grille, ligne, colonne, couleur):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for d_l, d_c in directions:
        a_encadrer = verifier_direction(grille, ligne, colonne, couleur, d_l, d_c)
        for l, c in a_encadrer:
            grille[l][c] = couleur




# Fonction principale
def jouer():
    grille = creer_grille()
    tour = 0
    milieu = TAILLE_GRILLE // 2

    # Placement initial
    positions = [(milieu - 1, milieu - 1), (milieu, milieu),
                 (milieu - 1, milieu), (milieu, milieu - 1)]
    for i, (l, c) in enumerate(positions[:nb_joueurs]):
        placer_pion(grille, l, c, COULEURS[i])

    while True:
        ev = donne_ev()
        tev = type_ev(ev)

        if tev == "Quitte":
            break
        elif tev == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)
            print(x, y)
            ligne, colonne = (y - 4) // TAILLE_CASE, (x - MARGE_GAUCHE_DROITE) // TAILLE_CASE
            print(ligne, colonne)
            if 0 <= ligne < TAILLE_GRILLE and 0 <= colonne < TAILLE_GRILLE:
                if grille[ligne][colonne] is None:  # Si la case est vide
                    couleur = COULEURS[tour % nb_joueurs]
                    placer_pion(grille, ligne, colonne, couleur)
                    encadrer_pions(grille, ligne, colonne, couleur)
                    tour += 1  # Prochain joueur
        efface_tout()
        dessiner_grille(grille)
        affichageScore(tabScore(grille, TAILLE_GRILLE, COULEURS), COULEURS)
        mise_a_jour()

    ferme_fenetre()

# Lancement du jeu
jouer()





