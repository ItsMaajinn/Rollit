import string
from fltk import *

alphabetMaj = string.ascii_uppercase


def dictCode(alphabet):
    d = {}
    for i in range(8):
        d[alphabet[i]] = []
        for j in range(1, 9):
            d[alphabet[i]].append(alphabet[i] + str(j))
    return d


def detectCase(ev, d, alphabet):
    tev = type_ev(ev)

    if tev == "ClicGauche":
        taille_case = 90
        x1 = 280
        y1 = 0

        x, y = abscisse(ev), ordonnee(ev)
        if x1 <= x < x1 + 8 * taille_case and y1 <= y < y1 + 8 * taille_case:
            col = (x - x1) // taille_case
            row = 7 - (y - y1) // taille_case
            key = alphabet[col]
            return d[key][row]



# Création de la fenêtre
marge_supplementaire = 4  # Marge supplémentaire pour le haut et le bas
largeur_fenetre, hauteur_fenetre = 1280, 720 + marge_supplementaire  # Augmenter la hauteur de la fenêtre de 4 pixels
cree_fenetre(largeur_fenetre, hauteur_fenetre)

# Taille du quadrillage (8x8)
taille_grille = 8

# On réduit légèrement la taille des cases pour éviter les débordements
taille_case = (hauteur_fenetre - marge_supplementaire) // taille_grille

# Calcule l'espace à gauche pour centrer le quadrillage horizontalement
marge_gauche_droite = (largeur_fenetre - (taille_case * taille_grille)) // 2


def dessine_quadrillage():
    # Dessine les lignes horizontales (exactement 8 lignes)
    for i in range(taille_grille + 1):
        y = i * taille_case + (marge_supplementaire // 2)  # Ajouter la marge supplémentaire en haut
        if y <= hauteur_fenetre:  # S'assurer de ne pas dépasser la fenêtre
            ligne(marge_gauche_droite, y, largeur_fenetre - marge_gauche_droite, y)

    # Dessine les lignes verticales (exactement 8 colonnes)
    for i in range(taille_grille + 1):
        x = marge_gauche_droite + i * taille_case
        if x <= largeur_fenetre:  # S'assurer de ne pas dépasser la fenêtre
            ligne(x, (marge_supplementaire // 2), x, (taille_case * taille_grille) + (
                    marge_supplementaire // 2))  # Utilise juste la hauteur nécessaire pour le quadrillage


# Appel de la fonction pour dessiner le quadrillage centré
dessine_quadrillage()

# Attente d'un événement pour fermer la fenêtre
while True:
    ev = donne_ev()
    tev = type_ev(ev)

    # Détecter et traiter l'événement dans detectCase
    case_detectee = detectCase(ev, dictCode(alphabetMaj), alphabetMaj)
    if case_detectee:
        print("Case détectée:", case_detectee)

    # Action dépendant du type d'événement reçu
    if tev == 'Touche':
        print('Appui sur la touche', touche(ev))
    elif tev == "ClicDroit":
        print("Clic droit au point", (abscisse(ev), ordonnee(ev)))
    elif tev == "ClicGauche":
        print("Clic gauche au point", (abscisse(ev), ordonnee(ev)))
    elif tev == 'Quitte':  # on sort de la boucle
        break
    else:  # dans les autres cas, on ne fait rien
        pass

    mise_a_jour()

ferme_fenetre()
