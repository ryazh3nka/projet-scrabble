# Le Scrabble
CR projet « Scrabble », groupe IMA04

## fait par :
Aleksandr SHIRKUNOV -- `aleksandr.shirkunov@etu-univ-grenoble-alpes.fr`<br>
Arna BARLUBAYEVA -- `arna.barlubayeva@etu-univ-grenoble-alpes.fr`

## comment utiliser
executez le script `scrabble.py` avec l'interprete de votre choix, preciser le nombre et les noms des joueurs, et voila !<br>
pour placer un mot, saisissez ses coordonees comme ca : `x y`, par exemple `4 9`<br>
pour jouer contre IA, donnez a un joueur un nom commencant par "Bot ...", par exemple "Bot Sacha"<br>

il y a aussi le fichier `SAUVEGARDE.txt` avec la partie entre Nigel Richards et Gueu Mathieu Zingbe.<br>
le coup gagnant, c'est de placer "ULCERES" a la case `9, 14`<br>

## limitations
- IA/indices -- analyse du tableau trop lent. cela peut etre ameliore avec multithreading ou simplification de la fonction `generer_toutes_suggestions()`<br>
- SAVE/LOAD -- les chemins sont tous relatif (i.e. dans le meme dossier); il n'est pas possible de sauvegarder la seance<br>
- gestion des erreurs -- le programme peut crasher si l'entree est d'un type incorrect<br>
- TUI/GUI -- pour le moment, il n’existe aucun moyen de changer entre l’interface TUI et l’interface GUI à l’execution. il faut decommenter les fonctions correspondantes dans main() pour passer de l’une à l’autre.
