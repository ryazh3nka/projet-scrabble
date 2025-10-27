#!/bin/env python23
# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------------
i11_shirkunov_barlubayeva_projet.py : CR projet « Scrabble », groupe IMA04

Aleksandr SHIRKUNOV <aleksandr.shirkunov@etu-univ-grenoble-alpes.fr>
Arna BARLUBAYEVA <arna.barlubayeva@etu-univ-grenoble-alpes.fr>
-----------------------------------------------------------------------------
"""

# IMPORTS ######################################################################

from pathlib import Path  # gestion fichiers
import tkinter as tk

# CONSTANTES ###################################################################

TAILLE_PLATEAU = 15  # taille du plateau de jeu

TAILLE_MARGE = 4  # taille marge gauche (qui contient les numéros de ligne)

JOKER = '?'  # jeton joker

BONUS_SYMBOLS = {
    "MT": '!',
    "MD": '@',
    "LT": '#',
    "LD": '$'
}

# ⚠ pas de variable globales, sauf cas exceptionnel


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


def affiche_jetons(jetons, bonus):
    """
    Q3) Affiche le plateau des jetons.
    """
    for ligne in range(TAILLE_PLATEAU):
        print("|---" * TAILLE_PLATEAU + '|')
        for col in range(TAILLE_PLATEAU):
            cur_char = jetons[ligne][col] or ' '
            cur_bonus = BONUS_SYMBOLS.get(bonus[ligne][col], ' ')
            print(f"| {cur_char}{cur_bonus}", end = '')
        print('|')
    print("|---" * TAILLE_PLATEAU + '|')

    
def affiche_jetons_gui(jetons, bonus, cell_size):
    """
    Q6) Affiche le plateau des jetons dans
    
    """
    root = tk.Tk()
    root.title("Le Scrabble")
    
    canvas = tk.Canvas(root,
                       width = cell_size*TAILLE_PLATEAU,
                       height = cell_size*TAILLE_PLATEAU)
    canvas.pack()

    for ligne in range(TAILLE_PLATEAU):
        for col in range(TAILLE_PLATEAU):
            x1 = ligne * cell_size
            y1 = col * cell_size
            x2 = ligne * cell_size + cell_size
            y2 = col * cell_size + cell_size

            cur_bonus = bonus[ligne][col]
            color = "white"
            match cur_bonus:
                case "MT": color = "red"
                case "MD": color = "yellow"
                case "LT": color = "blue"
                case "LD": color = "green"
            canvas.create_rectangle(x1, y1,
                                    x2, y2,
                                    fill = color,
                                    outline = "black")

            cur_char = jetons[ligne][col]
            color = "black"
            canvas.create_text((x1 + x2) / 2,
                               (y1 + y2) / 2,
                               fill = "black",
                               font = ("Arial", int(cell_size / 2)),
                               text = cur_char)
    root.mainloop()
    
# PARTIE 3 : CONSTRUCTIONS DE MOTS #############################################

def generer_dictfr(nf = 'littre.txt'):
    """Liste des mots Français en majuscules sans accent.

    >>> len(generer_dictfr())
    73085
    """
    mots = []
    with Path(nf).open(encoding='utf_8') as fich_mots:
        for line in fich_mots: mots.append(line.strip().upper())
    return mots


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


# MAIN PROGRAM  ################################################################

if __name__ == "__main__":
    # Q3: genere et affiche le plateau
    jetons = init_jetons()
    jetons[0][0] = 'B'
    jetons[1][1] = 'C'
    jetons[2][3] = 'A'
    jetons[14][14] = 'E'
    bonus = init_bonus()
    affiche_jetons(jetons, bonus)
    affiche_jetons_gui(jetons, bonus, 50)
