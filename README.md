Introduction
Les robots ne font que ce pour quoi ils sont programmés, ce qui complique leur adaptation à des environnements imprévus. Notre objectif : rendre le robot NSIbot intelligent en lui donnant 9 neurones (bien loin des 85 milliards du cerveau humain !)

Importer les librairies :
Si c'est votre première fois avec Arduino, un dossier Arduino a du être créé de par son installation dans votre dossier 'Documents'. Pour que les librairies Sharp-IR et Wire.h fonctionnent, vous devez créer un dossier 'libraries' dans le dossier Arduino et déplacer le Wire.h puis le SharpIR.zip avant de l'extraire.
Concernant matplotlib et numpy, il faut les installer: via le terminal (Ctrl+Shift+ù sur VS Code) (pip install) ou les extensions VS Code par exemple

Comment ça marche
Le fichier NSIBot_GUI.py lance une interface qui permet de remplir une table de vérité. Celle-ci décrit les réactions des moteurs gauche et droit du robot en fonction des entrées (0: marche arrière, 0.5: arrêt, 1: marche avant, selon la fonction sigmoïde).
Cette table est ensuite transmise au fichier neuronal_network.py, qui entraîne le réseau de neurones. Le programme ajuste automatiquement les poids du réseau pour qu’il réagisse correctement à certaines situations, notamment ici, la détection d’obstacles.
Une fois l’apprentissage terminé, le programme génère un fichier texte contenant les poids du réseau (Weights.h): couche d’entrée (Input Weights), couche cachée (Hidden Weights), couche de sortie (Output Weights)
Ce fichier est inclue dans le fichier NSIBot.ino. Il ne reste plus qu'à compiler le fichier arduino et le téléverser dans le robot.

Conclusion
Bonne chance et amusez vous bien !
