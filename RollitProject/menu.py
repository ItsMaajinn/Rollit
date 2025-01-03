from fltk import *
from PIL import Image
from AI.randomAI import *
from AI.semiRandom import *
from AI.miniMax import *
from jeu import *
from sauvegarde import *

# Step stack to track navigation history
step_stack = []


def navigate_to(step_function, *args):
    step_stack.append(step_function)  # Add current step to stack
    step_function(*args)


def go_back():
    if len(step_stack) > 1:
        step_stack.pop()  # Remove current step
        previous_step = step_stack[-1]  # Get the previous step
        previous_step()  # Navigate to the previous step
    else:
        print("No previous steps to go back to.")


def step1():
    image(427, 240, 'menu/1.png', largeur=854, hauteur=480, ancrage='center', tag='im')
    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        if tev == "Quitte":
            ferme_fenetre()
            break

        if tev == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)

            if 361 <= x <= 490 and 267 <= y <= 325:
                print("Jouer")
                navigate_to(step2)

            if 361 <= x <= 493 and 358 <= y <= 415:
                print("S'entrainer")
                navigate_to(step5)

        mise_a_jour()


def step2():
    image(427, 240, 'menu/2.png', largeur=854, hauteur=480, ancrage='center', tag='im')
    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        if tev == "Quitte":
            ferme_fenetre()
            break

        if tev == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)

            if 327 <= x <= 527 and 276 <= y <= 333:
                print("Nouvelle partie")
                navigate_to(step3)

            if 327 <= x <= 527 and 371 <= y <= 433:
                print("Sauvegarde")
                name = open_save_folder()
                name = load_save(name)
                grille, tour, nb_joueurs, taille_grille, couleurs = name['grille'], name['tour'], name['nb_joueurs'], name[
                    'taille_grille'], name['couleurs']
                ferme_fenetre()
                partie_en_cours(grille, tour, nb_joueurs, taille_grille, couleurs)

            if 724 <= x <= 804 and 371 <= y <= 433:
                print("Retour")
                go_back()

        mise_a_jour()


def step3():
    image(427, 240, 'menu/3.png', largeur=854, hauteur=480, ancrage='center', tag='im')
    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        if tev == "Quitte":
            ferme_fenetre()
            break

        if tev == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)

            if 48 <= x <= 251 and 276 <= y <= 334:
                print("2 joueurs")
                navigate_to(step4, 2)

            if 326 <= x <= 526 and 276 <= y <= 334:
                print("3 joueurs")
                navigate_to(step4, 3)

            if 602 <= x <= 804 and 276 <= y <= 334:
                print("4 joueurs")
                navigate_to(step4, 4)

            if 724 <= x <= 804 and 371 <= y <= 433:
                print("Retour")
                go_back()

        mise_a_jour()


def step4(nb):
    image(427, 240, 'menu/4.png', largeur=854, hauteur=480, ancrage='center', tag='im')
    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        if tev == "Quitte":
            ferme_fenetre()
            break

        if tev == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)

            if 69 <= x <= 183 and 310 <= y <= 348:
                print("4x4")
                ferme_fenetre()
                lancer_jeu(nb, 6)

            if 377 <= x <= 491 and 309 <= y <= 348:
                print("6x6")
                ferme_fenetre()
                lancer_jeu(nb, 8)

            if 687 <= x <= 802 and 309 <= y <= 347:
                print("9x9")
                ferme_fenetre()
                lancer_jeu(nb, 9)

            if 724 <= x <= 804 and 371 <= y <= 433:
                print("Retour")
                go_back()

        mise_a_jour()


def step5():
    image(427, 240, 'menu/5.png', largeur=854, hauteur=480, ancrage='center', tag='im')
    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        if tev == "Quitte":
            ferme_fenetre()
            break

        if tev == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)
            if 48 <= x <= 251 and 276 <= y <= 334:
                ferme_fenetre()
                lvl1()

            if 326 <= x <= 526 and 276 <= y <= 334:
                ferme_fenetre()
                lvl2()

            if 602 <= x <= 804 and 276 <= y <= 334:
                ferme_fenetre()
                lvl3()

            if 724 <= x <= 804 and 371 <= y <= 433:
                print("Retour")
                go_back()

        mise_a_jour()


# Start the application
if __name__ == "__main__":
    cree_fenetre(854, 480)
    step_stack.append(step1)  # Initialize the stack with step1
    step1()
