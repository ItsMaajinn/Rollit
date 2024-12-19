import copy
from fltk import *
import wx


# Interface pour choisir le nombre de joueurs
app = wx.App()
nb_joueurs = int(wx.GetTextFromUser("Nombre de joueurs (entre 2 et 4)"))
LARGEUR_FENETRE, HAUTEUR_FENETRE = 854, 480
TAILLE_GRILLE = 8
TAILLE_CASE = (HAUTEUR_FENETRE - 4) // TAILLE_GRILLE
MARGE_GAUCHE_DROITE = (LARGEUR_FENETRE - (TAILLE_CASE * TAILLE_GRILLE)) // 2
nb_joueurs = 2
COULEURS = ["assets/pionRouge.png", "assets/pionBleu.png", "assets/pionJaune.png", "assets/pionVert.png"][:nb_joueurs]
bordureDroite = MARGE_GAUCHE_DROITE + (TAILLE_GRILLE * TAILLE_CASE)
milieu = TAILLE_GRILLE // 2


def creer_grille():
    return [[None for _ in range(TAILLE_GRILLE)] for _ in range(TAILLE_GRILLE)]

def dessiner_grille(grille, lenGrille, couleurs):
    coul = changerCouleur(grille, lenGrille, couleurs)
    for i in range(TAILLE_GRILLE):
        for j in range(TAILLE_GRILLE):
            x1 = MARGE_GAUCHE_DROITE + j * TAILLE_CASE
            y1 = 4 + i * TAILLE_CASE
            x2, y2 = x1 + TAILLE_CASE, y1 + TAILLE_CASE
            rectangle(x1, y1, x2, y2, remplissage=coul[0])
            if grille[i][j]:  # Si une couleur est présente
                image((x1 + x2) // 2, (y1 + y2) // 2, grille[i][j],
                      largeur=TAILLE_CASE, hauteur=TAILLE_CASE, ancrage="center", tag="pion")
def changerCouleur(grille, lenGrille, couleurs):
    score = tabScore(grille, lenGrille, couleurs)  # On récupère les scores
    scoreTrie = []
    for i, (s, c) in enumerate(zip(score, couleurs)):
        scoreTrie.append((s, c))
    scoreTrie.sort(reverse=True)
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


# Placer un pion sur la grille
def placer_pion(grille, ligne, colonne, couleur):
    grille[ligne][colonne] = couleur




def tabScore(grille, lenGrille, couleurs):
    """
    Fonction qui retourne le score de chaque joueur
    :param grille: tab de tab avec None ou path
    :param lenGrille: taille de la grille
    :param couleurs: tab de path
    :return: tab de score (int)
    """
    score = [0, 0, 0, 0]
    for i in range(lenGrille):
        for j in range(lenGrille):
            if grille[i][j] is not None: # Si la case n'est pas vide
                index = couleurs.index(grille[i][j]) # On récupère l'index de la couleur
                score[index] += 1 # On incrémente le score

    return score

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

def bouleNextTo(grille, ligne, colonne):
    """
    Fonction qui vérifie si une boule est à côté de la case
    :param grille:
    :param ligne:
    :param colonne:
    :return:
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # 8 directions possibles
    for d_l, d_c in directions:
        if 0 <= ligne + d_l < TAILLE_GRILLE and 0 <= colonne + d_c < TAILLE_GRILLE: # Si la case est dans la grille
            if grille[ligne + d_l][colonne + d_c] is not None: # Si la case n'est pas vide
                return True
    return False




def coups_possibles(grille, couleurs):
    coups = []
    for i in range(TAILLE_GRILLE):
        for j in range(TAILLE_GRILLE):
            if grille[i][j] is None and bouleNextTo(grille, i, j):
                coups.append((i, j))

    return coups

def simuler_coups(grille, coup, couleur):
    copie = copy.deepcopy(grille)
    ligne, colonne = coup
    placer_pion(copie, ligne, colonne, couleur)
    encadrer_pions(copie, ligne, colonne, couleur)
    return copie




def evaluation(grille, couleurs, lenGrille):
    scores = tabScore(grille, lenGrille, couleurs)
    scoreIA = scores[1]
    scoreJoueur = scores[0]
    return scoreIA - scoreJoueur

def fin(grille):
    for ligne in grille:
        if None in ligne:
            return False
    return True


def minimax(grille, profondeur, maximisant, couleurs, lenGrille):
    # Conditions d'arrêt
    if profondeur == 0 or fin(grille):
        return evaluation(grille, couleurs, lenGrille), None

    # Coups possibles
    coups = coups_possibles(grille, couleurs)

    if maximisant:
        best_score = float('-inf')
        best_move = None
        for coup in coups:
            # Simuler le coup sur une copie de la grille
            grilleTemp = simuler_coups(grille, coup, couleurs[1])
            score, _ = minimax(grilleTemp, profondeur - 1, False, couleurs, lenGrille)
            if score > best_score:
                best_score = score
                best_move = coup
        return best_score, best_move

    else:
        best_score = float('inf')
        best_move = None
        for coup in coups:
            # Simuler le coup sur une copie de la grille
            grilleTemp = simuler_coups(grille, coup, couleurs[0])
            score, _ = minimax(grilleTemp, profondeur - 1, True, couleurs, lenGrille)
            if score < best_score:
                best_score = score
                best_move = coup
        return best_score, best_move

def affichageScore(score, couleursTab, grille, TAILLE_GRILLE):
    """
    Fonction qui affiche le score des joueurs
    :param score: tab de score (int
    :param couleursTab: # tab de path
    :return:
    """
    coul = changerCouleur(grille, TAILLE_GRILLE, couleursTab)
    rectangle(bordureDroite, 4, LARGEUR_FENETRE - 1, TAILLE_CASE + 4, couleur="black", remplissage=coul[1])
    rectangle(bordureDroite, TAILLE_CASE + 4, LARGEUR_FENETRE - 1, HAUTEUR_FENETRE - 4, couleur="black",
              remplissage=coul[0])
    texte((LARGEUR_FENETRE + bordureDroite) // 2, 32, "Scores", police="Arial", taille=20, ancrage="center")
    scoreTrie = []

    for i, (s, c) in enumerate(zip(score, couleursTab)): # zip crée un tuple avec les éléments de chaque tab
        scoreTrie.append((s, c))

    scoreTrie.sort(reverse=True) # On trie le tableau par score décroissant

    for  i in range(len(scoreTrie)):
        image((LARGEUR_FENETRE + bordureDroite) // 2 - 60, 70 + i * 60, scoreTrie[i][1], largeur=50, hauteur=50,
              ancrage="nw")
        texte((LARGEUR_FENETRE + bordureDroite) // 2 + 20, 80 + i * 60, str(scoreTrie[i][0]), police="Arial", taille=20,
              ancrage="nw")




def affichageGauche(couleurs, nb_joueurs, tour, lenGrille, grille):
    """
    Fonction qui affiche le tour actuel et le nombre de tours restants
    :param couleurs:
    :param nb_joueurs:
    :param tour:
    :param lenGrille:
    :return:
    """
    coul = changerCouleur(grille, lenGrille, couleurs)
    # Rectangle en haut à gauche
    rectangle(0, 4, MARGE_GAUCHE_DROITE, TAILLE_CASE+4, couleur="black", remplissage=coul[1])

    couleur = couleurs[tour % nb_joueurs]

    texte(MARGE_GAUCHE_DROITE // 2 - 30, 32, f"Tour :", police="Arial", taille=20, ancrage="center")
    image(MARGE_GAUCHE_DROITE // 2 + 30, 32, couleur, largeur=50, hauteur=50, ancrage="center")

    # Rectangle en bas à gauche
    rectangle(0, HAUTEUR_FENETRE-TAILLE_CASE-4, MARGE_GAUCHE_DROITE, HAUTEUR_FENETRE-4, couleur="black", remplissage=coul[1])

    texte(MARGE_GAUCHE_DROITE // 2, HAUTEUR_FENETRE - 32, f"{tour + nb_joueurs} / {lenGrille ** 2}", police="Arial",
          taille=20, ancrage="center")

    # Vide
    rectangle(0, TAILLE_CASE+4, MARGE_GAUCHE_DROITE, HAUTEUR_FENETRE-TAILLE_CASE-4, couleur="black",
              remplissage=coul[0])


def jouer():
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    grille = creer_grille()

    positions = [(milieu - 1, milieu - 1), (milieu, milieu),
                 (milieu - 1, milieu), (milieu, milieu - 1)]
    for i, (l, c) in enumerate(positions[:nb_joueurs]):
        placer_pion(grille, l, c, COULEURS[i])
        print(COULEURS[i])

    tour = 0
    while not fin(grille):
        ev = donne_ev()
        tev = type_ev(ev)

        if tev == "Quitte":
            break
        if tour % 2 == 0:
            if tev == "ClicGauche":
                x, y = abscisse(ev), ordonnee(ev)
                ligne, colonne = (y - 4) // TAILLE_CASE, (x - MARGE_GAUCHE_DROITE) // TAILLE_CASE
                if 0 <= ligne < TAILLE_GRILLE and 0 <= colonne < TAILLE_GRILLE:
                    if grille[ligne][colonne] is None:  # Si la case est vide
                        couleur = COULEURS[tour % nb_joueurs]
                        if bouleNextTo(grille, ligne, colonne):
                            placer_pion(grille, ligne, colonne, couleur)
                            encadrer_pions(grille, ligne, colonne, couleur)
                            tour += 1  # Prochain joueur
        else:
            score, coup = minimax(grille, 3, True, COULEURS, TAILLE_GRILLE)
            grille = simuler_coups(grille, coup, COULEURS[1])
            tour += 1
        efface_tout()
        dessiner_grille(grille, TAILLE_GRILLE, COULEURS)
        affichageScore(tabScore(grille, TAILLE_GRILLE, COULEURS), COULEURS, grille, TAILLE_GRILLE)
        affichageGauche(COULEURS, nb_joueurs, tour, TAILLE_GRILLE, grille)
        mise_a_jour()


jouer()