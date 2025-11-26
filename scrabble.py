#!/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_shirkunov_barlubayeva_projet.py : CR projet « Scrabble », groupe IMA04

Aleksandr SHIRKUNOV <aleksandr.shirkunov@etu-univ-grenoble-alpes.fr>
Arna BARLUBAYEVA <arna.barlubayeva@etu-univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from pathlib import Path
import random
import tkinter

# CONSTANTES ###################################################################

TAILLE_PLATEAU = 15

TAILLE_MARGE = 4

TAILLE_SAC = 102

JOKER = '?'

BONUS_SYMBOLS = {
    "MT": '!',
    "MD": '@',
    "LT": '#',
    "LD": '$'
}

# PARTIE 1 : LE PLATEAU ########################################################

def symetrise_liste(lst) :
    """
    Auxilliaire pour Q1 : symétrise en place la liste lst.
    EB : modification de lst.

    >>> essai = [1,2] ; symetrise_liste(essai) ; essai
    [1, 2, 1]
    >>> essai = [1,2,3] ; symetrise_liste(essai) ; essai
    [1, 2, 3, 2, 1]
    """
    copie_lst = list(lst)
    for i in range(2, len(copie_lst)+1): lst.append(copie_lst[-i])

def init_bonus():
    """
    Q1) Initialise le plateau des bonus.
    """
    # Compte-tenu  de  la  double   symétrie  axiale  du  plateau,  on
    # a  7  demi-lignes  dans  le  quart  supérieur  gauche,  puis  la
    # (demi-)ligne centrale,  et finalement  le centre. Tout  le reste
    # s'en déduit par symétrie.
    plt_bonus = [  # quart-supérieur gauche + ligne et colonne centrales
        ['MT', ''  , ''  , 'LD', ''  , ''  , ''  , 'MT'],
        [''  , 'MD', ''  , ''  , ''  , 'LT', ''  , ''],
        [''  , ''  , 'MD', ''  , ''  , ''  , 'LD', ''],
        ['LD', ''  , ''  , 'MD', ''  , ''  , ''  , 'LD'],
        [''  , ''  , ''  , ''  , 'MD', ''  , ''  , ''],
        [''  , 'LT', ''  , ''  , ''  , 'LT', ''  , ''],
        [''  , ''  , 'LD', ''  , ''  , ''  , 'LD', ''],
        ['MT', ''  , ''  , 'LD', ''  , ''  , ''  , 'MD']
    ]
    # On transforme les demi-lignes du plateau en lignes :
    for ligne in plt_bonus: symetrise_liste(ligne)
    # On transforme le demi-plateau en plateau :
    symetrise_liste(plt_bonus)

    return plt_bonus

def init_jetons():
    """
    Q2) Initialise le plateau des jetons.
    """
    plt_jetons = [['' for j in range(TAILLE_PLATEAU)] for i in range(TAILLE_PLATEAU)]
    return plt_jetons

def ind_prefix(ind):
    s_ind = str(ind)
    if len(s_ind) == 1:
        s_ind = '0' + s_ind
    return s_ind

def affiche_jetons(jetons, bonus):
    """
    Q3) Affiche le plateau des jetons.
    """
    print(' ' * TAILLE_MARGE + ' ', end='')
    for i in range(1, TAILLE_PLATEAU + 1):
        print(ind_prefix(i) + "  ", end = '')
    print()
    
    for i in range(TAILLE_PLATEAU):
        ligne = i + 1
        print(' ' * TAILLE_MARGE + "|---" * TAILLE_PLATEAU + '|')
        print(' ' + ind_prefix(ligne) + ' ', end = '')
        for j in range(TAILLE_PLATEAU):
            col = j
            jeton_act = jetons[i][j] or ' '
            if jeton_act == "START": jeton_act = '_'
            bonus_act = BONUS_SYMBOLS.get(bonus[i][j], ' ')
            print(f"| {jeton_act}{bonus_act}", end = '')
        print('|')
    print(' ' * TAILLE_MARGE + "|---" * TAILLE_PLATEAU + '|')
    
def affiche_jetons_gui(jetons, bonus, taille_cell):
    """
    Q6) Affiche le plateau des jetons dans un interface graphical
    avec Tkinter.
    """
    root = tkinter.Tk()
    root.title("Le Scrabble")
    
    canvas = tkinter.Canvas(root,
                       width = taille_cell*TAILLE_PLATEAU,
                       height = taille_cell*TAILLE_PLATEAU)
    canvas.pack()

    for ligne in range(TAILLE_PLATEAU):
        for col in range(TAILLE_PLATEAU):
            x1 = ligne * taille_cell
            y1 = col * taille_cell
            x2 = ligne * taille_cell + taille_cell
            y2 = col * taille_cell + taille_cell

            bonus_act = bonus[ligne][col]
            couleur = "white"
            match bonus_act:
                case "MT": couleur = "red"
                case "MD": couleur = "yellow"
                case "LT": couleur = "blue"
                case "LD": couleur = "green"
            canvas.create_rectangle(x1, y1,
                                    x2, y2,
                                    fill = couleur,
                                    outline = "black")

            jeton_act = jetons[ligne][col]
            couleur = "black"
            canvas.create_text((x1 + x2) / 2,
                               (y1 + y2) / 2,
                               fill = couleur,
                               font = ("Arial", int(taille_cell / 2)),
                               text = jeton_act)
    root.mainloop()
    
# PARTIE 2 : LA PIOCHE #########################################################

def init_pioche_alea():
    """
    Q7) genere une liste aleatore de jetons.
    """
    pioche = [jeton for jeton in "ABCDEFGHIJKLMNOPQRSTUVWXYZ??"]
    for i in range(80):
        nouv_let = chr(random.randint(ord('A'), ord('Z')))
        pioche.append(nouv_let)
    return pioche

def piocher(x, sac):
    """
    Q8) pioche le sac pour x jetons.
    """
    jetons_pioches = []
    for i in range(x):
        pos_alea = random.randint(0, len(sac)-1)
        jetons_pioches.append(sac.pop(pos_alea))
    return jetons_pioches

def completer_main(main, sac):
    """
    Q9) complete la main a 7 jetons.
    """
    nombre_jetons = min(7 - len(main), len(sac))
    main += piocher(nombre_jetons, sac)

def dans_la_main(main, ll):
    ll_copy = list(ll)
    while len(ll_copy) != 0:
        if ll[0] not in main:
            return False
        ll_copy.pop(0)
    return True
    
def echanger(jetons, main, sac):
    """
    Q10) echange les jetons dans la main avec des nouveaux jetons
    pris dans le sac.
    """
    nombre_remp = len(jetons)
    if len(sac) < nombre_remp or len(sac) == 0:
        return False
    
    if not dans_la_main(main, jetons):
        return False

    remplacer = [] # les positions des jetons qu'on doit remplacer dans la main
    for jeton in jetons:
        ind_remplacer = main.index(jeton)
        remplacer.append(ind_remplacer)
        main[ind_remplacer] = ''

    jetons_pioches = piocher(nombre_remp, sac)
    for i in range(nombre_remp):
        main[remplacer[i]] = jetons_pioches[i]
        
    sac += jetons
    return True

# PARTIE 3 : CONSTRUCTIONS DE MOTS #############################################

def generer_dictfr(nf = "littre.txt"):
    """Liste des mots Français en majuscules sans accent.

    >>> len(generer_dictfr())
    73085
    """
    mots = []
    with Path(nf).open(encoding='utf_8') as fich_mots:
        for line in fich_mots: mots.append(line.strip().upper())
    return mots

def select_mot_initiale(mots_fr, let):
    """
    Q13)
    """
    return [mot for mot in mots_fr if mot[0] == let]

def select_mot_longueur(mots_fr, lgr):
    """
    Q14)
    """
    return [mot for mot in mots_fr if len(mot) == lgr]

def mot_jouable(mot, main, lettres_deja_placees):
    """
    Q15) 
    """
    main_copy = list(main)
    mot_copy = list(mot)
    for char in lettres_deja_placees:
        i = 0
        while i < len(mot_copy):
            if mot_copy[i] == char:
                mot_copy.pop(i)
            else:
                i += 1

    i = 0
    while i < len(main_copy):
        if main_copy[i] in mot_copy:
            mot_copy.remove(main_copy.pop(i))
        else:
            i += 1

    num_jokers = 0
    for let in main_copy:
        if let == '?':
            num_jokers += 1

    besoin_jokers = len(mot_copy)
    return besoin_jokers - num_jokers <= 0

def mots_jouables(mots_fr, ll, lettres_deja_places):
    """
    Q16)
    """
    return [mot for mot in mots_fr if mot_jouable(mot, ll, lettres_deja_places)]
    # for mot in mots_fr:
    #     if mot_jouable(mot, ll, ''):
    #         res.append(mot)
    # return res

# PARTIE 4 : VALEUR D'UN MOT ###################################################

def generer_dico():
    """Dictionnaire des jetons.

    >>> jetons = generer_dico()
    >>> jetons['A'] == {'occ': 9, 'val': 1}
    True
    >>> jetons['B'] == jetons['C']
    True
    >>> jetons['?']['val'] == 0
    True
    >>> jetons['!']
    Traceback (most recent call last):
    KeyError: '!'
    """
    jetons = {}
    with Path('lettres.txt').open(encoding='utf_8') as lettres :
        for ligne in lettres:
            l, v, o = ligne.strip().split(';')
            jetons[l] = {'occ': int(o), 'val': int(v)}
    return jetons

def init_pioche(dico):
    """
    Q20)
    """
    res = []
    for let in dico:
        res += [let] * dico[let]['occ']
    return res

def valeur_mot(mot, dico):
    """
    Q22)
    """
    val = 0
    for let in mot:
        val += dico[let]['val']
    if len(mot) == 7: val += 50
    return val

def meilleur_mot(mots_fr, ll, dico):
    """
    Q23)
    """
    mots_j = mots_jouables(mots_fr, ll, '')
    val_max = -1
    meil_mot = ''
    for mot in mots_j:
        val = valeur_mot(mot, dico)
        if val > val_max:
            val_max = val
            meil_mot = mot
    return meil_mot, val_max

def meilleurs_mots(mots_fr, ll, dico):
    """
    Q24)
    """
    meil_mots = []
    meil_mot_val = meilleur_mot(mots_fr, ll, dico)[1]
    mots_j = mots_jouables(mots_fr, ll, '')
    for mot in mots_j:
        val = valeur_mot(mot, dico)
        if val == meil_mot_val:
            meil_mots.append(mot)
    return meil_mots

# PARTIE 6 : PLACEMENT DE MOT ##################################################

def case_hors_limites(x, y):
    if not 0 < x < TAILLE_PLATEAU or not 0 < y < TAILLE_PLATEAU:
        return True
    return False

def case_suiv(x, y, dir):
    match dir:
        case "bas":
            return x, y + 1
        case "droit":
            return x + 1, y
    return x, y

def case_finale(x, y, mot_len, dir):
    match dir:
        case "bas":
            return x, y + (mot_len - 1)
        case "droit":
            return x + mot_len - 1, y
    return x, y

def a_voisins(plateau, x, y, dir):
    # renvoie si la case a des voisin non-vides
    
    # on a besoin de dir_ignore car on ne doit pas compter les lettres
    # qu'on vient de placer ce tour
    match dir:
        case "gauche": dir_ignore = "droit"
        case "bas": dir_ignore = "haut"
        case "haut": dir_ignore = "bas"
        case "droit": dir_ignore = "gauche"
    
    directions = {
        "gauche": (-1, 0),
        "bas": (0, -1),
        "haut": (0, 1),
        "droit": (1, 0)
    }

    for c_dir, (dx, dy) in directions.items():
        if c_dir == dir_ignore: continue
        nx, ny = x + dx, y + dy

        if 0 <= nx <= TAILLE_PLATEAU - 1 and 0 <= ny <= TAILLE_PLATEAU - 1:
            if plateau[ny][nx] != '' and plateau[ny][nx] != "START":
                return True
            if plateau[ny][nx] == "START" and c_dir == dir:
                return True

    return False
    
def tester_placement(plateau, c1, c2, dir, mot):
    """
    Q29)
    """
    print(f"DEBUG: tester_placement(): trying to place {mot} at {c1}, {c2} to the {dir}")
    mot_len = len(mot)

    x, y = c1 - 1, c2 - 1
    x_fin, y_fin = case_finale(x, y, mot_len, dir)
    
    if case_hors_limites(x, y) or case_hors_limites(x_fin, y_fin):
        print("DEBUG: tester_placement(): case hors limites")
        return False
    elif dir not in ["bas", "droit"]:
        print(f"DEBUG: tester_placement(): dir {dir} is incorrect")
        return False
    
    possible_de_placer = False
    for i in range(mot_len):
        print(f"DEBUG: tester_placement(): trying to access plateau[{y}][{x}]")
        let_cour = plateau[y][x]
        if not (let_cour == '' or let_cour == mot[i] or let_cour == "START"):
            # le cas ou on essaye de recouvrir une case avec une autre lettre
            print("DEBUG: tester_placement(): trying to overwrite a letter")
            return False
        elif let_cour == mot[i] or let_cour == "START":
            # si on tombe sur une case avec une lettre, c'est garanti que
            # notre mot est connecte aux autres si on peur le placer
            # + le cas exceptionnel pour le tout premier mot sur le tableau
            if not possible_de_placer:
                possible_de_placer = True
        elif let_cour == '':
            if not possible_de_placer:
                # verifie que notre mot est connecte a un autre
                possible_de_placer = a_voisins(plateau, x, y, dir)
        x, y = case_suiv(x, y, dir)

    print(f"DEBUG: tester_placement(): word {mot} to be placed from ({c1}, {c2}) to ({x_fin+1}, {y_fin+1}): {possible_de_placer}")
    return possible_de_placer

def placer_mot(plateau, main, c1, c2, dir, mot):
    """
    Q30)
    """
    if not tester_placement(plateau, c1, c2, dir, mot):
        print("DEBUG: placer_mot(): tester_placement() returned False")
        return False
    
    x, y = c1 - 1, c2 - 1
    mot_len = len(mot)

    lettres_deja_placees = []
    x_temp, y_temp = x, y
    for i in range(mot_len):
        if plateau[y_temp][x_temp] != '':
            lettres_deja_placees.append(plateau[y_temp][x_temp])
        x_temp, y_temp = case_suiv(x_temp, y_temp, dir)
        
    if not mot_jouable(mot, main, lettres_deja_placees):
        print("DEBUG: placer_mot(): mot_jouable() returned False")
        return False
    
    for i in range(mot_len):
        if plateau[y][x] == '' or plateau[y][x] == "START":
            plateau[y][x] = mot[i]
            main.remove(mot[i])
        x, y = case_suiv(x, y, dir)
    return True

# PARTIE 5 : PREMIER PROGRAMME PRINCIPAL #######################################

def tour_joueur(plateau, joueur, sac, dico, mots_fr):
    # TODO: check if the word is allowed via mots_fr.
    # TODO2: check if ALL new words are allowed
    """
    Q25)
    """
    reessayer = True
    while reessayer:
        joueur["dtour"] = input("passer/echanger/proposer? ")
        
        match joueur["dtour"]:
            case "echanger":
                jetons_echanges = ''
                while True:
                    jetons_echanges = input("echanger ('!RET' pour retourner): ")
                    if jetons_echanges == "!RET":
                        break
                    elif not dans_la_main(joueur["main"], jetons_echanges):
                        print("Vous n'avez pas de tels jetons dans la main.")
                        continue
                    else:
                        break
                        
                if jetons_echanges != "!RET":
                    if echanger(list(jetons_echanges), joueur["main"], sac):
                        reessayer = False
                    else:
                        print("Impossible de piocher.")
                    
            case "proposer":
                mot_propose = ''
                while True:
                    mot_propose = input("proposer ('!RET' pour retourner): ").upper()
                    
                    if mot_propose == "!RET":
                        break
                    if mot_propose not in mots_fr:
                        print("Ce mot n'est pas un vrai mot francais.")
                        continue

                    x, y = map(int, input("coordonees (x y): ").split(' '))
                    dir = input("direction (bas/droit): ")
                    
                    if not placer_mot(plateau, joueur["main"], x, y, dir, mot_propose):
                        print("Impossible de placer ce mot.")
                        continue
                    else:
                        break
                if (mot_propose != "!RET"):
                    # val = valeur_mot(mot_propose, dico)
                    # print(f"La valeur de votre mot est {val}")
                    # joueur["score"] += val
                    # for let in mot_propose:
                    #     joueur["main"].remove(let)
                    # completer_main(joueur["main"], sac)
                    print("DEBUG:", plateau[7][7])
                    reessayer = False
                    
            case "passer":
                reessayer = False
                
            case _:
                print("Choix invalid. Reessayez.")
        print()
    
def partie_terminee(joueurs, sac):
    """
    Q26)
    """
    tous_passes = True
    for joueur in joueurs:
        if joueur["dtour"] != "passer":
            tous_passes = False
        if joueur["main"] == [] and sac == []:
            print("DEBUG: GAME ENDED BECAUSE ONE OF THE HANDS AND THE SACK ARE EMPTY")
            return True
    if tous_passes:
        print("DEBUG: GAME ENDED BECAUSE ALL PLAYERS PASSED")
    return tous_passes

def joueur_suivant(n, d_joue):
    """
    Q27)
    """
    return (d_joue + 1) % n

def init_joueurs(n):
    joueurs = [{"nom": '', "score": 0, "main": [], "dtour": "" }
               for _ in range(n)]
    for i in range(n):
        nom = input(f"Joueur {i}, tapez votre nom : ")
        joueurs[i]["nom"] = nom
    return joueurs

# MAIN PROGRAM  ################################################################

def main():
    """
    Q28)
    """    
    n_joueurs = int(input("Nombre de joueurs ? "))
    joueurs = init_joueurs(n_joueurs)
    jetons = init_jetons()
    jetons[7][7] = "START"
    bonus = init_bonus()
    
    dico = generer_dico() # combien vaut chaque lettre
    sac = init_pioche(dico)
    mots_fr = generer_dictfr("littre.txt")

    joueur_suiv = 0
    for joueur in joueurs:
        #joueur["main"] = ['B', 'A', 'N', 'A', 'N', 'E', '?']
        completer_main(joueur["main"], sac)

    # DELETE THIS
    # joueurs[0]["main"] = ['B', 'A', 'N', 'A', 'N', 'E', '?']
    # joueurs[1]["main"] = ['B', 'A', 'N', 'A', 'N', 'E', '?']
    print()
    
    while True:
        affiche_jetons(jetons, bonus)
        cur_joueur = joueurs[joueur_suiv]
        print(f"Joueur {cur_joueur['nom']},\nil reste {len(sac)} jetons dans le sac,\nvotre score est {cur_joueur['score']}\nvotre main est {cur_joueur['main']}")
        tour_joueur(jetons, cur_joueur, sac, dico, mots_fr)
        
        if partie_terminee(joueurs, sac):
            max_score = -1
            vainqueur = {"nom": "ERROR"}
            for joueur in joueurs:
                for let in joueur["main"]:
                    joueur["score"] -= dico[let]['val']
                joueur["score"] = max(0, joueur["score"])
                if joueur["score"] > max_score:
                    max_score = joueur["score"]
                    vainqueur = joueur
            print(f"\nLe vainqueur est {vainqueur['nom']} avec {max_score} points")
            break
        joueur_suiv = joueur_suivant(n_joueurs, joueur_suiv)

main()

"""
TODO:
1) account for ALL words creating after placing a word, not only the one the user entered, e.g:

    GOURMET
CHATON

(the user just entered GOURMET and played 3 words at the same time)

2) account for placing the same word in the same way, e.g:
3) account for continuing the word in the same direction, e.g:

 B 
BANANE
 N
 A
 N
 E

and writing ANANE from (2, 2) to the right or down

4) correctly count score points
"""
