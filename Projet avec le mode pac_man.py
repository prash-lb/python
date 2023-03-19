from upemtk import *
from time import sleep
from random import randint

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases


def case_vers_pixel(case):
    """
	Fonction recevant les coordonnées d'une case du plateau sous la 
	forme d'un couple d'entiers (ligne, colonne) et renvoyant les 
	coordonnées du pixel se trouvant au centre de cette case. Ce calcul 
	prend en compte la taille de chaque case, donnée par la variable 
	globale taille_case.
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes():
    """
    :param:pommes
    :param: serpent
    fonction permmetant d'afficher la pomme et de verifier
    si la pomme est apparait sur le serpent alors
    elle renvoie une nouvelle coordonné à la pomme
    """
    nb_pomme = len(pommes)
    if nb_pomme < 1:  # pomme maximal sur le terrain
        pos_pomme = randint(0, 39), randint(0, 29)  # pomme aleatoire
        # verification que la pomme ne se crée pas sur les coordonner du serpent
        if pos_pomme in serpent:
            pos_pomme = randint(0, 39), randint(0, 29)

        pommes.append(pos_pomme)
        # affichage de tous les pommes
    for i in range(nb_pomme):
        x, y = case_vers_pixel(pommes[i])
        cercle(x, y, taille_case / 2,
               couleur='darkred', remplissage='red')
        rectangle(x - 2, y - taille_case * .4, x + 2, y - taille_case * .7,
                  couleur='darkgreen', remplissage='darkgreen')


def position_serpent(coordonne_serpent, coordonne_corps_serpent):
    """
    :param coordonne_serpent
    :param serpent:
    :param coordonne_corps_serpent:
    :return:
    fonction recevant les coordonnes de la tete du serpent ainsi que celle du corps
    et aura pour but de donner au corps du serpent les coordones de sont adjacents
    """
    longeueur = len(serpent)
    alternatif = True
    tete = serpent[0]
    test = [tete, coordonne_corps_serpent]
    serpent[0] = coordonne_serpent
    for i in range(0, longeueur):
        if i == 0:
            test[1] = serpent[i + 1]
            serpent[i + 1] = test[0]
        elif alternatif:
            if i < longeueur - 1:
                test[0] = serpent[i + 1]
                serpent[i + 1] = test[1]
            alternatif = not alternatif
        elif not alternatif:
            if i < longeueur - 1:
                test[1] = serpent[i + 1]
                serpent[i + 1] = test[0]
                alternatif = not alternatif
        else:
            test[1] = serpent[i]


def affiche_serpent():
    """
    affiche le corps du serpent aini que la tete du serpent d'une different couleur
    :param :serpent
    """
    longueur = len(serpent)
    x, y = case_vers_pixel(serpent[0])
    cercle(x, y, taille_case / 2 + 1,
           couleur='darkgreen', remplissage='blue')
    for i in range(1, longueur):
        x, y = case_vers_pixel(serpent[i])
        cercle(x, y, taille_case / 2 + 1,
               couleur='darkgreen', remplissage='#E104FF')


def change_direction(direction, touche):
    """
    :param direction:
    :param touche:
    :return:
    fonction recevant un direction ainsi qu'une touche et renvoyant une nouvelle direction
    """
    if "z" == touche:  # flèche haut pressée
        if (serpent[0][0], serpent[0][1] - 1) in serpent:
            return direction
        else:
            return (0, -1)
    elif "s" == touche:  # flèche bas pressée
        if (serpent[0][0], serpent[0][1] + 1) in serpent:
            return direction
        else:
            return (0, 1)
    elif "d" == touche:  # flèche droite pressée
        if (serpent[0][0] + 1, serpent[0][1]) in serpent:
            return direction
        else:
            return (1, 0)
    elif "q" == touche:  # flèche gauche pressée
        if (serpent[0][0] - 1, serpent[0][1]) in serpent:
            return direction
        else:
            return (-1, 0)
    else:
        return direction


def collision(direction, score):
    """
    :param direction:
    :return:
    Fonction recevant une direction.Elle aura
    pour but de verifier la collision du serpent
    avec la pomme ainsi avec lui meme
    """
    longeueur = len(serpent)
    if serpent[0] == pommes[0]:
        dernier_corps_serpent = longeueur - 1
        serpent.append(serpent[dernier_corps_serpent] + direction)
        pommes.remove(pommes[0])
        score[0] = score[0] + 1
        return False
    if serpent[0] in mur:
        del serpent[:]
        return True
    if serpent[0] in serpent[1:longeueur]:
        del serpent[:]
        return True


def affichage_mur():
    nb_mur = len(mur)
    if nb_mur < 15:  # pomme maximal sur le terrain
        pos_mur = randint(0, 39), randint(0, 29)  # pomme aleatoire
        # verification que la pomme ne se crée pas sur les coordonner du serpent
        if pos_mur in serpent or pos_mur in pommes:
            pos_mur = randint(0, 39), randint(0, 29)

        mur.append(pos_mur)
        # affichage de tous les pommes
    for i in range(nb_mur):
        x, y = case_vers_pixel(mur[i])
        cercle(x, y, taille_case / 2 + 1,
               couleur='darkgreen', remplissage='grey')


# variable
corps = 0
score = [0]
framerate = 20  # taux de rafraîchissement du jeu en images/s
direction = (1, 0)  # direction initiale du serpent
mur = []  # liste des coordonnées des cases contenant des murs
pommes = []  # liste des coordonnées des cases contenant des pommes
serpent = [(20, 20), (19, 20), (18, 20)]  # liste des coordonnées de cases adjacentes décrivant le serpent
main = True
jouer = rejouer = mode_mur = pac_man = False
# affichage texte
cree_fenetre(taille_case * largeur_plateau,
             taille_case * hauteur_plateau)
rectangle(0, 0, taille_case * largeur_plateau, taille_case * hauteur_plateau, remplissage="#133337")

texte(190, 50, "MODES DE JEU", "blue")
rectangle(200, 100, 400, 150, 'black', '#E51944')
texte(240, 110, "NORMAL")
rectangle(200, 200, 400, 250, 'black', '#C1D955')
texte(230, 210, "PAC-MUR")
rectangle(200, 300, 400, 350, 'black', '#E51944')
texte(260, 310, "MUR")
rectangle(450, 380, 590, 420, 'black', '#E00D0D')
texte(450, 380, "QUITTER")

# main

x_souris, y_souris = attend_clic_gauche()
if x_souris < 400 and x_souris > 200 and y_souris > 100 and y_souris < 150:
    jouer = True
    mode_mur = pac_man = False
elif x_souris < 400 and x_souris > 200 and y_souris > 200 and y_souris < 250:
    pac_man = mode_mur = jouer = True
elif x_souris < 400 and x_souris > 200 and y_souris > 300 and y_souris < 350:
    mode_mur = jouer = True
elif x_souris < 590 and x_souris > 450 and y_souris > 380 and y_souris < 420:
    main = False

# fonction principale:
while main:
    while jouer:
        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)
        if ty == 'Quitte':
            jouer = False
        elif ty == 'Touche':
            direction = change_direction(direction, touche(ev))

        # affichage des objets
        efface_tout()
        rectangle(0, 0, taille_case * largeur_plateau, taille_case * hauteur_plateau, remplissage="#0FA471")
        if mode_mur:
            affichage_mur()
        affiche_pommes()
        affiche_serpent()
        texte(38 * taille_case, 0 * taille_case, score)
        if collision(direction, score):
            jouer = False
        mise_a_jour()

        if len(serpent) == 0:
            jouer = False
            rejouer = True
        else:
            position_serpent(serpent[0], corps)
            # deplacement du serpent
            serpent[0] = serpent[0][0] + direction[0], serpent[0][1] + direction[1]
            if pac_man:#J AI AJOUTER SA 
                if serpent[0][0] == 40:
                    l=serpent[0][1]
                    serpent[0]=0,l
                    jouer = True
                elif serpent[0][0] == -1:
                    l=serpent[0][1]
                    serpent[0]=40,l
                    jouer = True
                elif serpent[0][1] == -1:
                    l=serpent[0][0]
                    serpent[0]=l,30
                    jouer = True
                elif serpent[0][1] == 30:
                    l=serpent[0][0]
                    serpent[0]=l,0
                    jouer = True
            elif serpent[0][0] < 0 or serpent[0][0] >= 40 or serpent[0][1] < 0 or serpent[0][1] >= 30:
                jouer = False
                rejouer = True
                


        # attente avant rafraîchissement
        sleep(1 / framerate)
    if rejouer is True:
        #afficage de fin de jue
        efface_tout()
        rectangle(0, 0, taille_case * largeur_plateau, taille_case * hauteur_plateau, remplissage="#043276")
        texte(240, 210, "PERDU",)
        rectangle(200, 100, 400, 150, 'black', 'green')
        texte(225, 110, "REJOUER")
        rectangle(200, 300, 400, 350, 'black', '#E00D0D')
        texte(230, 310, "QUITTER")

        x_souris, y_souris = attend_clic_gauche()
        if x_souris < 400 and x_souris > 200 and y_souris > 100 and y_souris < 150:
            jouer = True
            serpent = [(20, 20), (19, 20), (18, 20)]
            score = [0]
            pommes = []
            mur = []
            direction = (1, 0)


        elif x_souris < 400 and x_souris > 200 and y_souris > 300 and y_souris < 350:
            main = False
# fermeture et sortie
ferme_fenetre()
