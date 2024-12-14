from fltk import *
import wx

# Interface pour choisir le nombre de joueurs
app = wx.App()  # Crée l'application wxWidgets
nb_joueurs = int(wx.GetTextFromUser("Nombre de joueurs (entre 2 et 4)"))  # Demande à l'utilisateur combien de joueurs (entre 2 et 4)

# Configuration de la fenêtre et du jeu
largeur_fenetre, hauteur_fenetre = 1280, 720  # Dimensions de la fenêtre
taille_grille = 8  # Nombre de cases dans la grille
taille_case = (hauteur_fenetre - 4) // taille_grille  # Taille de chaque case (calculée pour que la grille s'adapte à la fenêtre)
marge_gauche_droite = (largeur_fenetre - (taille_case * taille_grille)) // 2  # Marge gauche et droite pour centrer la grille
couleurs = ["assets/pionRouge.png", "assets/pionBleu.png", "assets/pionJaune.png", "assets/pionVert.png"][:nb_joueurs]  # Liste des pions en fonction du nombre de joueurs

cree_fenetre(largeur_fenetre, hauteur_fenetre)  # Création de la fenêtre avec la taille définie


# Fonction pour créer une grille vide
def creer_grille():
    return [[None for _ in range(taille_grille)] for _ in range(taille_grille)]  # Retourne une grille vide (8x8 par défaut)

# Fonction pour dessiner la grille et afficher les pions
def dessiner_grille(grille):
    for i in range(taille_grille):  # Parcours chaque ligne
        for j in range(taille_grille):  # Parcours chaque colonne
            x1 = marge_gauche_droite + j * taille_case  # Calcul des coordonnées x de la case
            y1 = 4 + i * taille_case  # Calcul des coordonnées y de la case
            x2, y2 = x1 + taille_case, y1 + taille_case  # Coordonnées de la case opposée
            rectangle(x1, y1, x2, y2)  # Dessine le rectangle de la case
            if grille[i][j]:  # Si la case contient un pion
                image((x1 + x2) // 2, (y1 + y2) // 2, grille[i][j], largeur=taille_case, hauteur=taille_case, ancrage="center")  # Affiche le pion centré dans la case

# Fonction pour placer un pion sur la grille
def placer_pion(grille, ligne, colonne, couleur):
    grille[ligne][colonne] = couleur  # Met la couleur de la boule dans la case spécifiée


# Fonction pour vérifier une direction spécifique (optimisation pour parcourir la grille)
def verifier_direction(grille, ligne, colonne, couleur, d_l, d_c):
    a_encadrer = []  # Liste des pions à encadrer
    l, c = ligne + d_l, colonne + d_c  # Calcul des nouvelles coordonnées en fonction de la direction
    while 0 <= l < taille_grille and 0 <= c < taille_grille:  # Tant que les coordonnées sont valides
        case = grille[l][c]
        if case is None:  # Si la case est vide, on arrête la vérification
            return []
        if case == couleur:  # Si on rencontre un pion de la même couleur, on retourne les pions à encadrer
            return a_encadrer
        a_encadrer.append((l, c))  # Ajoute la case à la liste des pions à encadrer
        l, c = l + d_l, c + d_c  # On continue dans la direction choisie
    return []

# Fonction pour encadrer les pions dans toutes les directions
def encadrer_pions(grille, ligne, colonne, couleur, directions):
    for d_l, d_c in directions:
        a_encadrer = verifier_direction(grille, ligne, colonne, couleur, d_l, d_c)  # Vérifie chaque direction
        print(a_encadrer)  # Affiche les cases à encadrer
        for l, c in a_encadrer:
            grille[l][c] = couleur  # Encadre les pions dans la direction donnée

# Fonction principale pour démarrer le jeu
def jouer():
    grille = creer_grille()  # Crée une grille vide
    tour = 0  # Tour du joueur
    milieu = taille_grille // 2  # Position du centre de la grille pour le placement initial des pions
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # 8 directions possibles

    # Placement initial des pions au centre de la grille
    positions = [(milieu - 1, milieu - 1), (milieu, milieu),
                 (milieu - 1, milieu), (milieu, milieu - 1)]  # Coordonnées des 4 pions initiaux (en fonction du nombre de joueurs)
    for i, (l, c) in enumerate(positions[:nb_joueurs]):
        placer_pion(grille, l, c, couleurs[i])  # Place les pions au centre

    while True:  # Boucle de jeu
        ev = donne_ev()  # Récupère l'événement
        tev = type_ev(ev)  # Récupère le type de l'événement

        if tev == "Quitte":  # Si l'utilisateur ferme la fenêtre
            break
        elif tev == "ClicGauche":  # Si un clic gauche est détecté
            x, y = abscisse(ev), ordonnee(ev)  # Récupère la position du clic
            ligne, colonne = (y - 4) // taille_case, (x - marge_gauche_droite) // taille_case  # Convertit les coordonnées en indices de la grille
            if 0 <= ligne < taille_grille and 0 <= colonne < taille_grille:  # Si les coordonnées sont valides
                if grille[ligne][colonne] is None:  # Si la case est vide
                    couleur = couleurs[tour % nb_joueurs]  # Détermine la couleur du joueur actuel
                    for d_l, d_c in directions :
                        if grille[ligne + d_l][colonne + d_c] is None :
                            print('non')
                        else :
                            placer_pion(grille, ligne, colonne, couleur)  # Place le pion
                            encadrer_pions(grille, ligne, colonne, couleur, directions)  # Encadre les pions selon les règles du jeu
                            encadrer_pions(grille, ligne, colonne, couleur, directions)  # Redouble l'encadrement pour toutes les directions
                            tour += 1  # Passe au tour suivant

        efface_tout()  # Efface l'écran
        dessiner_grille(grille)  # Redessine la grille avec les pions
        mise_a_jour()  # Met à jour l'affichage

    ferme_fenetre()  # Ferme la fenêtre du jeu lorsque la boucle est terminée

# Lancement du jeu
jouer()
