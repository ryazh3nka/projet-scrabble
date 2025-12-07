# Le Scrabble
CR projet « Scrabble », groupe IMA04

## fait par :
Aleksandr SHIRKUNOV -- `aleksandr.shirkunov@etu-univ-grenoble-alpes.fr`
Arna BARLUBAYEVA -- `arna.barlubayeva@etu-univ-grenoble-alpes.fr`

## comment utiliser
executez le script `scrabble.py` avec l'interprete de votre choix, preciser le nombre et les mots des joueurs, et voila !
pour placer un mot, saisissez ses coordonees comme ca : `x y`, par exemple `4 9`
pour jouer contre IA, donnez a un joueur un nom commencant par "Bot ...", par exemple "Bot Sacha"

il y a aussi le fichier `SAUVEGARDE.txt` avec la partie entre Nigel Richards et Gueu Mathieu Zingbe.
le coup gagnant, c'est de placer "ULCERES" a la case `9, 14`

## limitations
IA/indices -- analyse du tableau trop lent (peut etre ameliore avec multithreading ou simplification de la fonction `generer_toutes_suggestions()`)
SAVE/LOAD -- les chemins sont tous relatif (i.e. dans le meme dossier); il n'est pas possible de sauvegarder la seance
gestion des erreurs -- le programme peut crasher si l'entree est d'un type incorrect
