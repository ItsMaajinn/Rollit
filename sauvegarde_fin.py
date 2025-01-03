from fltk import *
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
    COULEURS = ["assets/pionRouge.png", "assets/pionBleu.png", "assets/pionJaune.png", "assets/pionVert.png"][:nb_joueurs]
    bordureDroite = MARGE_GAUCHE_DROITE + (TAILLE_GRILLE * TAILLE_CASE)
    nb_parties = 1
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    nb_parties=1

    # Dessiner la grille et les pions
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

    # Placer un pion sur la grille
    def placer_pion(grille, ligne, colonne, couleur):
        grille[ligne][colonne] = couleur

    def tabScore(grille, lenGrille, couleurs):
        score = [0, 0, 0, 0]
        for i in range(lenGrille):
            for j in range(lenGrille):
                if grille[i][j] is not None:  # Si la case n'est pas vide
                    index = couleurs.index(grille[i][j])  # On récupère l'index de la couleur
                    score[index] += 1  # On incrémente le score

        return score

    def affichageScore(score, couleursTab, grille, TAILLE_GRILLE):
        if TAILLE_GRILLE == 6:
            coul = changerCouleur(grille, TAILLE_GRILLE, couleursTab)

            # Zone du titre "Scores"
            rectangle(bordureDroite, 4, LARGEUR_FENETRE - 1, TAILLE_CASE + 4, couleur="black", remplissage=coul[1])
            texte((LARGEUR_FENETRE + bordureDroite) // 2, (TAILLE_CASE + 4) // 2, "Scores", police="Arial", taille=20,
                  ancrage="center")
            # Zone des scores (le reste de l'espace à droite)
            rectangle(bordureDroite, TAILLE_CASE + 4, LARGEUR_FENETRE - 1, HAUTEUR_FENETRE - 22
                      , couleur="black", remplissage=coul[0])

            # Affichage des scores triés
            scoreTrie = []
            for i, (s, c) in enumerate(zip(score, couleursTab)):
                scoreTrie.append((s, c))
            scoreTrie.sort(reverse=True)

            # Centrage vertical des scores
            y_start = (HAUTEUR_FENETRE - (len(scoreTrie) * 60)) // 2  # Calculer le point de départ centré verticalement
            for i in range(len(scoreTrie)):
                image((LARGEUR_FENETRE + bordureDroite) // 2 - 60, y_start + i * 60, scoreTrie[i][1], largeur=50,
                      hauteur=50,
                      ancrage="nw")
                texte((LARGEUR_FENETRE + bordureDroite) // 2 + 20, y_start + i * 60 + 10, str(scoreTrie[i][0]),
                      police="Arial",
                      taille=20, ancrage="nw")


        elif TAILLE_GRILLE == 8:
            coul = changerCouleur(grille, TAILLE_GRILLE, couleursTab)
            rectangle(bordureDroite, 4, LARGEUR_FENETRE - 1, TAILLE_CASE + 4, couleur="black", remplissage=coul[1])
            rectangle(bordureDroite, TAILLE_CASE + 4, LARGEUR_FENETRE - 1, HAUTEUR_FENETRE - 4, couleur="black",
                      remplissage=coul[0])
            texte((LARGEUR_FENETRE + bordureDroite) // 2, 32, "Scores", police="Arial", taille=20, ancrage="center")
            scoreTrie = []

            for i, (s, c) in enumerate(zip(score, couleursTab)):
                scoreTrie.append((s, c))

            scoreTrie.sort(reverse=True)

            for  i in range(len(scoreTrie)):
                image((LARGEUR_FENETRE + bordureDroite) // 2 - 60, 70 + i * 60, scoreTrie[i][1], largeur=50, hauteur=50,
                      ancrage="nw")
                texte((LARGEUR_FENETRE + bordureDroite) // 2 + 20, 80 + i * 60, str(scoreTrie[i][0]), police="Arial", taille=20,
                      ancrage="nw")

        elif TAILLE_GRILLE == 9:
            coul = changerCouleur(grille, TAILLE_GRILLE, couleursTab)
            rectangle(bordureDroite, 4, LARGEUR_FENETRE - 1, TAILLE_CASE + 4, couleur="black", remplissage=coul[1])
            rectangle(bordureDroite, TAILLE_CASE + 4, LARGEUR_FENETRE - 1, HAUTEUR_FENETRE - 8, couleur="black",
                      remplissage=coul[0])
            texte((LARGEUR_FENETRE + bordureDroite) // 2, 32, "Scores", police="Arial", taille=20, ancrage="center")
            scoreTrie = []

            for i, (s, c) in enumerate(zip(score, couleursTab)):  # zip crée un tuple avec les éléments de chaque tab
                scoreTrie.append((s, c))

            scoreTrie.sort(reverse=True)  # On trie le tableau par score décroissant

            for i in range(len(scoreTrie)):
                image((LARGEUR_FENETRE + bordureDroite) // 2 - 60, 70 + i * 60, scoreTrie[i][1], largeur=50, hauteur=50,
                      ancrage="nw")
                texte((LARGEUR_FENETRE + bordureDroite) // 2 + 20, 80 + i * 60, str(scoreTrie[i][0]), police="Arial",
                      taille=20,
                      ancrage="nw")

    def affichageGauche(couleurs, nb_joueurs, tour, lenGrille, grille, taille_grille):
        if taille_grille == 6:
            coul = changerCouleur(grille, lenGrille, couleurs)
            # Rectangle en haut à gauche
            rectangle(0, 4, MARGE_GAUCHE_DROITE, TAILLE_CASE + 4, couleur="black", remplissage=coul[1])

            couleur = couleurs[tour % nb_joueurs]

            texte((MARGE_GAUCHE_DROITE // 2) - 20, (TAILLE_CASE + 4) // 2, f"Tour :", police="Arial", taille=20,
                  ancrage="center")
            image(MARGE_GAUCHE_DROITE // 2 + 40, (TAILLE_CASE + 4) // 2, couleur, largeur=50, hauteur=50,
                  ancrage="center")

            # Rectangle en bas à gauche
            rectangle(0, HAUTEUR_FENETRE - TAILLE_CASE - 2, MARGE_GAUCHE_DROITE, HAUTEUR_FENETRE - 2, couleur="black",
                      remplissage=coul[1])

            texte(MARGE_GAUCHE_DROITE // 2, HAUTEUR_FENETRE - (TAILLE_CASE // 2) - 2,
                  f"{tour + nb_joueurs} / {lenGrille ** 2}",
                  police="Arial", taille=20, ancrage="center")

            # Vide
            rectangle(0, TAILLE_CASE + 4, MARGE_GAUCHE_DROITE, HAUTEUR_FENETRE - TAILLE_CASE - 2, couleur="black",
                      remplissage=coul[0])

            # Bouton sauvegarde
            rectangle(15, (HAUTEUR_FENETRE // 2) - 35, MARGE_GAUCHE_DROITE - 15, (HAUTEUR_FENETRE // 2) + 35,
                      couleur="black", remplissage='pink')
            texte(MARGE_GAUCHE_DROITE // 2, (HAUTEUR_FENETRE // 2), "SAUVEGARDER", police="Arial", taille=15,
                  ancrage="center")

        elif taille_grille == 8:
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

            # Bouton sauvegarde
            rectangle(15, (HAUTEUR_FENETRE // 2) - 35, MARGE_GAUCHE_DROITE - 15, (HAUTEUR_FENETRE // 2) + 35,
                      couleur="black",
                      remplissage='pink')
            texte(MARGE_GAUCHE_DROITE // 2, (HAUTEUR_FENETRE // 2), f"SAUVEGARDER", police="Arial", taille=15,
                  ancrage="center")
        elif taille_grille == 9:
            coul = changerCouleur(grille, lenGrille, couleurs)

            # Rectangle en haut à gauche
            rectangle(0, 4, MARGE_GAUCHE_DROITE, TAILLE_CASE + 4, couleur="black", remplissage=coul[1])

            couleur = couleurs[tour % nb_joueurs]

            texte(MARGE_GAUCHE_DROITE // 2 - 30, 32, f"Tour :", police="Arial", taille=20, ancrage="center")
            image(MARGE_GAUCHE_DROITE // 2 + 30, 32, couleur, largeur=50, hauteur=50, ancrage="center")

            # Rectangle en bas à gauche
            rectangle(0, HAUTEUR_FENETRE - TAILLE_CASE - 8, MARGE_GAUCHE_DROITE, HAUTEUR_FENETRE - 8, couleur="black",
                      remplissage=coul[1])

            texte(MARGE_GAUCHE_DROITE // 2, HAUTEUR_FENETRE - 32, f"{tour + nb_joueurs} / {lenGrille ** 2}",
                  police="Arial",
                  taille=20, ancrage="center")

            # Vide
            rectangle(0, TAILLE_CASE + 4, MARGE_GAUCHE_DROITE, HAUTEUR_FENETRE - TAILLE_CASE - 8, couleur="black",
                      remplissage=coul[0])

            # Bouton sauvegarde
            rectangle(15, (HAUTEUR_FENETRE // 2) - 35, MARGE_GAUCHE_DROITE - 15, (HAUTEUR_FENETRE // 2) + 35,
                      couleur="black", remplissage='pink')
            texte(MARGE_GAUCHE_DROITE // 2, (HAUTEUR_FENETRE // 2), "SAUVEGARDER", police="Arial", taille=15,
                  ancrage="center")
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


    def bouleNextTo(grille, ligne, colonne):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # 8 directions possibles
        for d_l, d_c in directions:
            if 0 <= ligne + d_l < TAILLE_GRILLE and 0 <= colonne + d_c < TAILLE_GRILLE:
                if grille[ligne + d_l][colonne + d_c] is not None:
                    return True
        return False

    def fin(tour, grille, lenGrille, couleurs, nb_joueurs):
        if tour == (lenGrille**2) - nb_joueurs:
            score = tabScore(grille, lenGrille, couleurs)
            scoreTrie = []
            for i, (s, c) in enumerate(zip(score, couleurs)):
                scoreTrie.append((s, c))
            scoreTrie.sort(reverse=True)
            return (True, scoreTrie[0],scoreTrie)  # Retourne True et le gagnant
        return (False, None)  # Sinon, continue le jeu

    def changerCouleur(grille, lenGrille, couleurs):
        score = tabScore(grille, lenGrille, couleurs)
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
        
    def affichage_fin(grille,tour,lenGrille,couleurs):
        
        image(427, 240, 'podium.jpg', largeur=854, hauteur=480, ancrage='center')
            
        scoreTrie = fin(tour, grille, lenGrille, couleurs, nb_joueurs)[2]
        
        if nb_joueurs == 2 :
            image(174, 325, scoreTrie[0][1], largeur=100, hauteur=100, ancrage='center')
            image(419, 325, scoreTrie[1][1], largeur=100, hauteur=100, ancrage='center')
            
            image(810, 50, scoreTrie[0][1], largeur=75, hauteur=75, ancrage='center')
            texte(813, 53, scoreTrie[0][0], police="Arial", taille=15,ancrage="center")
            
            image(810, 150, scoreTrie[1][1], largeur=75, hauteur=75, ancrage='center')
            texte(813, 153, scoreTrie[1][0], police="Arial", taille=15,ancrage="center")
            
        elif nb_joueurs > 2 :
            image(174, 325, scoreTrie[0][1], largeur=100, hauteur=100, ancrage='center')
            image(419, 325, scoreTrie[1][1], largeur=100, hauteur=100, ancrage='center')
            image(663, 325, scoreTrie[2][1], largeur=100, hauteur=100, ancrage='center')
            
            if nb_joueurs == 3 :
                image(810, 50, scoreTrie[0][1], largeur=75, hauteur=75, ancrage='center')
                texte(813, 53, scoreTrie[0][0], police="Arial", taille=15,ancrage="center")
                
                image(810, 150, scoreTrie[1][1], largeur=75, hauteur=75, ancrage='center')
                texte(813, 153, scoreTrie[1][0], police="Arial", taille=15,ancrage="center")
                
                image(810, 250, scoreTrie[2][1], largeur=75, hauteur=75, ancrage='center')
                texte(813, 253, scoreTrie[2][0], police="Arial", taille=15,ancrage="center")
                
            elif nb_joueurs == 4 :
                image(810, 50, scoreTrie[0][1], largeur=75, hauteur=75, ancrage='center')
                texte(813, 53, scoreTrie[0][0], police="Arial", taille=15,ancrage="center")
                
                image(810, 150, scoreTrie[1][1], largeur=75, hauteur=75, ancrage='center')
                texte(813, 153, scoreTrie[1][0], police="Arial", taille=15,ancrage="center")
                
                image(810, 250, scoreTrie[2][1], largeur=75, hauteur=75, ancrage='center')
                texte(813, 253, scoreTrie[2][0], police="Arial", taille=15,ancrage="center")
                
                image(810, 350, scoreTrie[3][1], largeur=75, hauteur=75, ancrage='center')
                texte(813, 353, scoreTrie[3][0], police="Arial", taille=15,ancrage="center")
        


    def sauv(tour, grille, tev, ev, nb_parties):
        """
        Fonction qui permet de réaliser la sauvegarde d'une partie
        :param tour: Tour actuel de la partie
        :param grille: État de la grille
        :param tev: Type d'événement
        :param ev: Événement
        :param nb_parties: Numéro de la partie
        """
        if tev == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)
            # Si le joueur clique sur le bouton sauvegarder
            if 15 <= x <= MARGE_GAUCHE_DROITE - 15 and (HAUTEUR_FENETRE // 2) - 35 <= y <= (HAUTEUR_FENETRE // 2) + 35:
                # Déterminer le chemin du dossier de sauvegarde
                save_folder_path = os.path.expanduser("~/sauvegarde")

                # S'assurer que le dossier existe
                os.makedirs(save_folder_path, exist_ok=True)

                # Construire le chemin complet du fichier de sauvegarde
                save_file_path = os.path.join(save_folder_path, f"sauvegarde_partie{nb_parties}.txt")

                # Les informations de la partie sont enregistrées dans un fichier texte
                with open(save_file_path, 'w', encoding='utf8') as sauvegarde:
                    nb_parties += 1
                    sauvegarde.write(str(grille) + '\n')
                    sauvegarde.write(str(tour) + '\n')
                    sauvegarde.write(str(nb_joueurs) + '\n')
                    sauvegarde.write(str(taille_grille) + '\n')
                    sauvegarde.write(str(couleurs))
                    ferme_fenetre()

    def jouer(tour):  # Passer tour en paramètre ici
        while fin(tour, grille, TAILLE_GRILLE, COULEURS, nb_joueurs)[0] is not True:
            ev = donne_ev()
            tev = type_ev(ev)

            if tev == "Quitte":
                break
            elif tev == "ClicGauche":
                x, y = abscisse(ev), ordonnee(ev)
                ligne, colonne = (y - 4) // TAILLE_CASE, (x - MARGE_GAUCHE_DROITE) // TAILLE_CASE
                if 0 <= ligne < TAILLE_GRILLE and 0 <= colonne < TAILLE_GRILLE:
                    if grille[ligne][colonne] is None:  # Si la case est vide
                        couleur = COULEURS[tour % nb_joueurs]
                        if bouleNextTo(grille, ligne, colonne):
                            placer_pion(grille, ligne, colonne, couleur)
                            encadrer_pions(grille, ligne, colonne, couleur)
                            tour += 1
            efface_tout()
            dessiner_grille(grille, TAILLE_GRILLE, COULEURS)
            affichageScore(tabScore(grille, TAILLE_GRILLE, COULEURS), COULEURS, grille, TAILLE_GRILLE)
            affichageGauche(COULEURS, nb_joueurs, tour, TAILLE_GRILLE, grille, TAILLE_GRILLE)
            sauv(tour, grille, tev, ev, nb_parties)
            mise_a_jour()

        ferme_fenetre()

        cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
        affichage_fin(grille,tour,TAILLE_GRILLE,COULEURS)
        
        while True:
            tev = type_ev(ev)
            
            if tev == "Quitte":
                break
            mise_a_jour()
            
        ferme_fenetre()
        attend_ev()

    # Lancer la partie en cours
    jouer(tour)


