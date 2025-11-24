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

def mot_jouable(mot, ll, nombre_manq = 0):
    """
    Q15)
    """
    ll_copy = list(ll)
    lettres_supprimes = 0
    i = 0
    while i < len(ll_copy):
        if ll_copy[i] in mot:
            ll_copy.pop(i)
            lettres_supprimes += 1
        else:
            i += 1

    num_jokers = 0
    for let in ll_copy:
        if let == '?':
            num_jokers += 1

    # len(mot) - lettres_supprimes is the amount of letters we need to cover with jokers
    # nombre_manq is the number of non-covered letters we're allowed to have
    return len(mot) - lettres_supprimes - num_jokers <= nombre_manq

def mots_jouables(mots_fr, ll, nombre_manq):
    """
    Q16)
    """
    return [mot for mot in mots_fr if mot_jouable(mot, ll, nombre_manq)]
    # for mot in mots_fr:
    #     if mot_jouable(mot, ll, nombre_manq):
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
    mots_j = mots_jouables(mots_fr, ll, 0)
    val_max = -1
    meil_mot = ''
    for mot in mots_j:
        val = valeur_mot(mot, dico)
        if val > val_max:
            val_max = val
            meil_mot = mot
    return meil_mot

def meilleurs_mots(mots_fr, ll, dico):
    """
    Q24)
    """
    meil_mots = []
    meil_mot_val = len(meilleur_mot(mots_fr, ll, dico))
    mots_j = mots_jouables(mots_fr, ll, 0)
    for mot in mots_j:
        val = valeur_mot(mot, dico)
        if val == meil_mot_val:
            meil_mots.append(mot)
    return meil_mots

# PARTIE 5 : PREMIER PROGRAMME PRINCIPAL #######################################

def tour_joueur(joueur, sac, dico):
    """
    Q25)
    """
    reessayer = True
    while reessayer:
        joueur["dtour"] = input("passer/echanger/proposer? ")

        match joueur["dtour"]:
            case "echanger":
                jetons_echanges = input("echanger ('!ret' pour retourner): ")
                while not dans_la_main(joueur["main"], jetons_echanges) and jetons_echanges != "!ret":
                    jetons_echanges = input("echanger ('!ret' pour retourner): ")
                    
                if jetons_echanges != "!ret":
                    if echanger(list(jetons_echanges), joueur["main"], sac):
                        reessayer = False
                    else:
                        print("Impossible de piocher.")
            case "proposer":
                mot_propose = input("proposer ('!ret' pour retourner): ")
                while mot_jouable(list(mot_propose), joueur["main"], 0) and mot_propose != "!ret":
                    mot_propose = input("proposer ('!ret' pour retourner): ")
                    
                if (mot_propose != "!ret"):
                    val = valeur_mot(mot_propose, dico)
                    print(f"La valeur de votre mot est {val}")
                    joueur["score"] += val
                    for let in mot_propose:
                        joueur["main"].remove(let)
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

# PARTIE 6 : PLACEMENT DE MOT ##################################################

def lire_coords():
    """
    Q28)
    """
    x, y = map(int, input().split())
    return x, y

def tester_placement(plateau, i, j, dir, mot):
    """
    Q29)
    """
    return True
    
# MAIN PROGRAM  ################################################################

def main():
    """
    Q28)
    """    
    n_joueurs = int(input("Nombre de joueurs ? "))
    joueurs = init_joueurs(n_joueurs)
    jetons = init_jetons()
    bonus = init_bonus()
    
    dico = generer_dico()
    sac = init_pioche(dico)
    mots_ft = generer_dictfr("littre.txt")

    joueur_suiv = 0
    for joueur in joueurs:
        #joueur["main"] = ['B', 'A', 'N', 'A', 'N', 'E', '?']
        completer_main(joueur["main"], sac)
        
    print()
    affiche_jetons(jetons, bonus)
    
    while True:
        #affiche_jetons(jetons, bonus)
        cur_joueur = joueurs[joueur_suiv]
        print(f"Joueur {cur_joueur['nom']},\nil reste {len(sac)} jetons dans le sac,\nvotre score est {cur_joueur['score']}\nvotre main est {cur_joueur['main']}")
        tour_joueur(cur_joueur, sac, dico)
        
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
