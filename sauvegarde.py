from fltk import *
import wx
from asyncio import *
import ast

# Interface pour choisir le nombre de joueurs
app = wx.App()
nb_joueurs = int(wx.GetTextFromUser("Nombre de joueurs (entre 2 et 4)"))

# Configuration
largeur_fenetre, hauteur_fenetre = 854, 480
taille_grille = 8
marge = 4

taille_case = (hauteur_fenetre - marge) // taille_grille
marge_gauche_droite = (largeur_fenetre - (taille_case * taille_grille)) // 2
couleurs = ['assets/pionRouge.png', 'assets/pionBleu.png', 'assets/pionJaune.png', 'assets/pionVert.png'][:nb_joueurs]
bordure_droite = marge_gauche_droite + (taille_grille * taille_case)
cree_fenetre(largeur_fenetre, hauteur_fenetre)

nb_parties = 1

# Création de la grille
def creer_grille():
    return [[None for _ in range(taille_grille)] for _ in range(taille_grille)]

# Dessiner la grille et les pions
def dessiner_grille(grille, len_grille, couleurs):
    coul = changer_couleur(grille, len_grille, couleurs)
    for i in range(taille_grille):
        for j in range(taille_grille):
            x1 = marge_gauche_droite + j * taille_case
            y1 = 4 + i * taille_case
            x2, y2 = x1 + taille_case, y1 + taille_case
            rectangle(x1, y1, x2, y2, remplissage=coul[0])
            if grille[i][j]:  # Si une couleur est présente
                image((x1 + x2) // 2, (y1 + y2) // 2, grille[i][j],
                      largeur=taille_case, hauteur=taille_case, ancrage="center", tag="pion")

# Placer un pion sur la grille
def placer_pion(grille, ligne, colonne, couleur):
    grille[ligne][colonne] = couleur


def tab_score(grille, len_grille, couleurs):
    """
    Fonction qui retourne le score de chaque joueur
    :param grille: tab de tab avec None ou path
    :param len_grille: taille de la grille
    :param couleurs: tab de path
    :return: tab de score (int)
    """
    score = [0, 0, 0, 0]
    for i in range(len_grille):
        for j in range(len_grille):
            if grille[i][j] is not None: # Si la case n'est pas vide
                index = couleurs.index(grille[i][j]) # On récupère l'index de la couleur
                score[index] += 1 # On incrémente le score

    return score

def affichage_score(score, couleurs_tab, grille, taille_grille):
    """
    Fonction qui affiche le score des joueurs
    :param score: tab de score (int
    :param couleurs_tab: # tab de path
    :return:
    """
    coul = changer_couleur(grille, taille_grille, couleurs_tab)
    rectangle(bordure_droite, 4, largeur_fenetre - 1, taille_case + 4, couleur="black", remplissage=coul[1])
    rectangle(bordure_droite, taille_case + 4, largeur_fenetre - 1, hauteur_fenetre - 4, couleur="black",
              remplissage=coul[0])
    texte((largeur_fenetre + bordure_droite) // 2, 32, "Scores", police="Arial", taille=20, ancrage="center")
    score_trie = []

    for i, (s, c) in enumerate(zip(score, couleurs_tab)): # zip crée un tuple avec les éléments de chaque tab
        score_trie.append((s, c))

    score_trie.sort(reverse=True) # On trie le tableau par score décroissant

    for  i in range(len(score_trie)):
        image((largeur_fenetre + bordure_droite) // 2 - 60, 70 + i * 60, score_trie[i][1], largeur=50, hauteur=50,
              ancrage="nw")
        texte((largeur_fenetre + bordure_droite) // 2 + 20, 80 + i * 60, str(score_trie[i][0]), police="Arial", taille=20,
              ancrage="nw")


def affichage_gauche(couleurs, nb_joueurs, tour, len_grille, grille):
    """
    Fonction qui affiche le tour actuel et le nombre de tours restants
    :param couleurs:
    :param nb_joueurs:
    :param tour:
    :param len_grille:
    :return:
    """
    coul = changer_couleur(grille, len_grille, couleurs)
    # Rectangle en haut à gauche
    rectangle(0, 4, marge_gauche_droite, taille_case+4, couleur="black", remplissage=coul[1])

    couleur = couleurs[tour % nb_joueurs]

    texte(marge_gauche_droite // 2 - 30, 32, f"Tour :", police="Arial", taille=20, ancrage="center")
    image(marge_gauche_droite // 2 + 30, 32, couleur, largeur=50, hauteur=50, ancrage="center")

    # Rectangle en bas à gauche
    rectangle(0, hauteur_fenetre-taille_case-4, marge_gauche_droite, hauteur_fenetre-4, couleur="black", remplissage=coul[1])

    texte(marge_gauche_droite // 2, hauteur_fenetre - 32, f"{tour + nb_joueurs} / {len_grille ** 2}", police="Arial",
          taille=20, ancrage="center")

    # Vide
    rectangle(0, taille_case+4, marge_gauche_droite, hauteur_fenetre-taille_case-4, couleur="black",
              remplissage=coul[0])
    
    #Bouton sauvegarde
    rectangle(15, (hauteur_fenetre//2)-35, marge_gauche_droite-15, (hauteur_fenetre//2)+35, couleur="black",
              remplissage='pink')
    texte(marge_gauche_droite // 2,(hauteur_fenetre//2) , f"SAUVEGARDER", police="Arial", taille=15, ancrage="center")
    

# Vérification dans une direction (optimisée)
def verifier_direction(grille, ligne, colonne, couleur, d_l, d_c):
    a_encadrer = []
    l, c = ligne + d_l, colonne + d_c
    while 0 <= l < taille_grille and 0 <= c < taille_grille:
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

def boule_next_to(grille, ligne, colonne):
    """
    Fonction qui vérifie si une boule est à côté de la case
    :param grille:
    :param ligne:
    :param colonne:
    :return:
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # 8 directions possibles
    for d_l, d_c in directions:
        if 0 <= ligne + d_l < taille_grille and 0 <= colonne + d_c < taille_grille: # Si la case est dans la grille
            if grille[ligne + d_l][colonne + d_c] is not None: # Si la case n'est pas vide
                return True
    return False

def fin(tour, grille, len_grille, couleurs, nb_joueurs):
    """
    Fonction qui vérifie si la partie est terminée
    :param tour:
    :param grille:
    :param len_grille:
    :param couleurs:
    :param nb_joueurs:
    :return:
    """
    if tour == (len_grille**2) - nb_joueurs: # Si le nombre de tours est égal au nombre de cases - nombre de joueurs
        score = tab_score(grille, len_grille, couleurs) # On récupère les scores
        score_trie = []
        for i, (s, c) in enumerate(zip(score, couleurs)):
            score_trie.append((s, c))
        score_trie.sort(reverse=True)
        return (True, score_trie[0]) # On retourne True et le gagnant
    return (False, None) # Sinon on retourne False et donc pas de gagnant (None)

def changer_couleur(grille, len_grille, couleurs):
    score = tab_score(grille, len_grille, couleurs)  # On récupère les scores
    score_trie = []
    for i, (s, c) in enumerate(zip(score, couleurs)):
        score_trie.append((s, c))
    score_trie.sort(reverse=True)
    if score_trie[0][1] == "assets/pionRouge.png":
        return ("#eccfc3", "#ecb8a5")
    elif score_trie[0][1] == "assets/pionBleu.png":
        return ("#add7f6", "#87bfff")
    elif score_trie[0][1] == "assets/pionJaune.png":
        return ("#fade7f", "#fdf47f")
    elif score_trie[0][1] == "assets/pionVert.png":
        return ("#c6ebbe", "#a9dbb8")
    else:
        return ("#ffffff", "#000000")

def affichage_v(gagnant):
    """
    Affichage temporaire qui affiche le gagnant
    :param gagnant:
    :return:
    """
    texte(largeur_fenetre // 2, hauteur_fenetre // 2, f"Le gagnant est {gagnant[1]}", police="Arial", taille=30, ancrage="center")


def sauv(tour,grille,tev,ev,nb_parties):
    """
    Fonction qui permet de réaliser la sauvegarde d'une partie
    :param tour:
    :param grille:
    :param tev:
    :param ev:
    :param nb_parties:
    """
    if tev == "ClicGauche":
        x, y = abscisse(ev), ordonnee(ev)
        #si le joueur clique sur le bouton sauvegarder
        if 15 <= x <= marge_gauche_droite-15 and (hauteur_fenetre//2)-35 <= y <= (hauteur_fenetre//2)+35:
            sauvegarde = open("".join(('sauvegarde_partie',str(nb_parties),'.txt')),'w',encoding = 'utf8')
            #les informations de la partie sont enregistrees dans une fichier texte
            nb_parties += 1
            sauvegarde.write(str(nb_joueurs)+'\n')
            sauvegarde.write(str(tour)+'\n')
            sauvegarde.write(str(grille)+'\n')
            sauvegarde.write(str(nb_parties))
            sauvegarde.close()
            
            
def recup_val_sauv(partie):
    """
    Fonction qui permet de recuperer la sauvegarde d'une partie
    :param partie:
    """
    #on lit les elements du fichier texte correpondant à la partie choisie
    lire_sauv = open(partie,'r',encoding = 'utf8') 
    nb_joueurs = int(lire_sauv.readline())
    tour = int(lire_sauv.readline())
    chaine = lire_sauv.readline()
    nb_parties = int(lire_sauv.readline())
    grille = ast.literal_eval(chaine)  #conversion de la chaine de caractere sous forme de liste en liste
    lire_sauv.close()
    print(grille)
    return nb_joueurs,tour,grille,nb_parties

# Fonction principale
def jouer():
    """
    Fonction principale qui gère le jeu
    :return:
    """
    
    if "partie choisie au menu" :
        nb_joueurs,tour,grille,nb_parties = recup_val_sauv(partie)
        milieu = taille_grille // 2

    else :
        
         grille = creer_grille()
        tour = 0
        milieu = taille_grille // 2

        
        # Placement initial
        positions = [(milieu - 1, milieu - 1), (milieu, milieu),
                    (milieu - 1, milieu), (milieu, milieu - 1)]
        for i, (l, c) in enumerate(positions[:nb_joueurs]):
            placer_pion(grille, l, c, couleurs[i])


    while fin(tour, grille, taille_grille, couleurs, nb_joueurs)[0] is not True:
        ev = donne_ev()
        tev = type_ev(ev)

        if tev == "Quitte":
            break
        elif tev == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)
            print(x, y)
            ligne, colonne = (y - 4) // taille_case, (x - marge_gauche_droite) // taille_case
            print(ligne, colonne)
            if 0 <= ligne < taille_grille and 0 <= colonne < taille_grille:
                if grille[ligne][colonne] is None:  # Si la case est vide
                    couleur = couleurs[tour % nb_joueurs]
                    if boule_next_to(grille, ligne, colonne):
                        placer_pion(grille, ligne, colonne, couleur)
                        encadrer_pions(grille, ligne, colonne, couleur)
                        tour += 1  # Prochain joueur
                        print(tour)
                        print(nb_joueurs)
                        print(fin(tour, grille, taille_grille, couleurs, nb_joueurs))
        efface_tout()
        dessiner_grille(grille, taille_grille, couleurs)
        affichage_score(tab_score(grille, taille_grille, couleurs), couleurs, grille, taille_grille)
        affichage_gauche(couleurs, nb_joueurs, tour, taille_grille, grille)
        sauv(tour,grille,tev,ev,nb_parties)
        
        mise_a_jour()

    ferme_fenetre()

    cree_fenetre(largeur_fenetre, hauteur_fenetre)
    affichage_v(fin(tour, grille, taille_grille, couleurs, nb_joueurs)[1])
    attend_ev()

# Lancement du jeu
jouer()