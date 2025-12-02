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

TOUR = 1

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
    ll_copie = list(ll)
    while len(ll_copie) != 0:
        if ll[0] not in main:
            return False
        ll_copie.pop(0)
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

def select_mot_initial(mots_fr, let):
    """
    Q13)
    """
    return [mot for mot in mots_fr if mot[0] == let]

def select_mot_longueur(mots_fr, lgr):
    """
    Q14)
    """
    return [mot for mot in mots_fr if len(mot) == lgr]

def mot_jouable(mot, main):
    """
    Q15) 
    """
    main_copie = list(main)
    mot_copie = list(mot)
    
    i = 0
    while i < len(main_copie):
        if main_copie[i] in mot_copie:
            mot_copie.remove(main_copie.pop(i))
        else:
            i += 1

    n_jokers = 0
    for let in main_copie:
        if let == '?':
            n_jokers += 1

    besoin_jokers = len(mot_copie)
    return besoin_jokers - n_jokers <= 0

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
        case "gauche":
            return x - 1, y
        case "bas":
            return x, y + 1
        case "haut":
            return x, y - 1
        case "droit":
            return x + 1, y
    return x, y

def case_finale(x, y, mot_len, dir):
    match dir:
        case "gauche":
            return x - (mot_len - 1), y
        case "bas":
            return x, y + (mot_len - 1)
        case "haut":
            return x, y - (mot_len - 1)
        case "droit":
            return x + (mot_len - 1), y
    return x, y

def voisin_orthogonal(plateau, x, y, let_cour, dir):
    ort_directions = []
    match dir:
        case "droit":
            ort_directions += ["haut", "bas"]
        case "bas":
            ort_directions += ["gauche", "droit"]

    segments = {}
    for ort_dir in ort_directions:
        segment = ''
        nx, ny = case_suiv(x, y, ort_dir)
        while 0 <= nx <= TAILLE_PLATEAU - 1 and 0 <= ny <= TAILLE_PLATEAU - 1:
            jeton_cour = plateau[ny][nx]
            if jeton_cour == '':
                break
            segment += jeton_cour
            nx, ny = case_suiv(nx, ny, ort_dir)
        if ort_dir in ["gauche", "haut"]: segment = segment[::-1]
        segments[ort_dir] = segment

    voisin = segments.get("gauche", "") + segments.get("haut", "") + let_cour + segments.get("droit", "") + segments.get("bas", "")
    
    if voisin == let_cour:
        return ''
    return voisin

def a_voisins(plateau, x, y, dir):
    """
    renvoie si la case a des voisin non-vides
    """
    if TOUR == 1: return True # cas special
    
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
            if plateau[ny][nx] != '':
                return True

    return False

def tester_placement(plateau, x, y, dir, mot):
    """
    Q29)
    """
    print(f"DEBUG: tester_placement(): trying to place {mot} at {x+1}, {y+1} to the {dir}")
    mot_len = len(mot)

    x_fin, y_fin = case_finale(x, y, mot_len, dir)
    
    if case_hors_limites(x, y) or case_hors_limites(x_fin, y_fin):
        print("DEBUG: tester_placement(): case hors limites")
        return []
    elif dir not in ["bas", "droit"]:
        print(f"DEBUG: tester_placement(): dir {dir} is incorrect")
        return []

    voisins = False # RENAME THIS TO a_voisins or something
    lettres_manq = []
    for i in range(mot_len):
        let_cour = plateau[y][x]
        if not (let_cour == '' or let_cour == mot[i]):
            # le cas ou on essaye de recouvrir une case avec une autre lettre
            print(f"DEBUG: tester_placement(): trying to overwrite a letter at {x} {y}")
            return []
        elif let_cour == '':
            lettres_manq.append(mot[i])

        if a_voisins(plateau, x, y, dir):
            voisins = True
        x, y = case_suiv(x, y, dir)

    print(voisins)
    print(lettres_manq)
    if not voisins:
        return []
    return lettres_manq

def placer_mot(plateau, joueur, x, y, dir, mot, mots_fr, dico):
    """
    Q30)
    """
    main = joueur["main"]
    mot_score = 0

    if mot not in mots_fr:
        print(f"DEBUG: placer_mot(): {mot} n'est pas un mot francais")
        return False
    
    lettres_manq = tester_placement(plateau, x, y, dir, mot)
    if lettres_manq == []:
        print(f"DEBUG: placer_mot(): tester_placement(): impossible de placer le mot '{mot}' a {x+1} {y+1}")
        return False
    
    if not mot_jouable(lettres_manq, main):
        print("DEBUG: placer_mot(): mot_jouable() returned False")
        return False

    nx, ny = x, y
    mot_len = len(mot)
    for i in range(mot_len):
        voisin_ort = voisin_orthogonal(plateau, nx, ny, mot[i], dir)
        print(f"DEBUG: placer_mot(): voisin {voisin_ort} at {nx + 1}, {ny + 1}")

        if voisin_ort != '':
            if voisin_ort not in mots_fr:
                print(f"DEBUG: pas possible de jouer {mot}: {voisin_ort} n'est pas un mot francais")
                return False
            if plateau[ny][nx] == '':
                mot_score += valeur_mot(voisin_ort, dico)
            
        nx, ny = case_suiv(nx, ny, dir)

    nx, ny = x, y
    for i in range(mot_len):
        if plateau[ny][nx] == '':
            plateau[ny][nx] = mot[i]
            if mot[i] not in main:
                main.remove('?')
            else:
                main.remove(mot[i])
        nx, ny = case_suiv(nx, ny, dir)
        
    mot_score += valeur_mot(mot, dico)
    if len(joueur["main"]) == 0: mot_score += 50
    joueur["score"] += mot_score
    return True

# PARTIE 5 : PREMIER PROGRAMME PRINCIPAL #######################################

def tour_joueur(plateau, joueur, sac, dico, mots_fr):
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
                    jetons_echanges = input("echanger ('!RET' pour retourner): ").upper()
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
                    
                    if not placer_mot(plateau, joueur, x - 1, y - 1, dir, mot_propose, mots_fr, dico):
                        print("Impossible de placer ce mot.")
                        continue
                    else:
                        break
                if (mot_propose != "!RET"):
                    completer_main(joueur["main"], sac)
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
    bonus = init_bonus()
    global TOUR
    
    dico = generer_dico() # combien vaut chaque lettre
    sac = init_pioche(dico)
    mots_fr = generer_dictfr("littre.txt")

    joueur_suiv = 0
    for joueur in joueurs:
        completer_main(joueur["main"], sac)

    # DELETE THIS
    joueurs[0]["main"] = ['O', 'N']
    joueurs[1]["main"] = ['G', 'O']

    joueurs[0]["main"] = ['G', 'O', 'U', 'R', 'M', 'E', 'T']
    joueurs[1]["main"] = ['C', 'H', 'A', 'T', 'O', 'N', '?']
    
    while True:
        affiche_jetons(jetons, bonus)
        cur_joueur = joueurs[joueur_suiv]
        print(f"Joueur {cur_joueur['nom']},\nil reste {len(sac)} jetons dans le sac,\nvotre score est {cur_joueur['score']}\nvotre main est {cur_joueur['main']}")
        tour_joueur(jetons, cur_joueur, sac, dico, mots_fr)
        TOUR += 1
        
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

DONE!

2) account for placing the same word in the same way, e.g:

DONE!

3) account for continuing the word in the same direction, e.g:

 B 
BANANE
 N
 A
 N
 E

and writing ANANE from (2, 2) to the right or down
DONE!

3.5)

FIX CONNECTING WORDS IN THE SAME DIRECTION

__ON -> GOON shouldn't be valid

4) correctly count score points
DONE!

5) remove jokers from hand
DONE!
"""
