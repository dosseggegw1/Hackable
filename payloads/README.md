## Syntaxe possible pour les scripts d'injection de frappes

> Basé sur les Ducky Script



#### REM [commentaire]

Les lignes non exécutées et servent de commentaire.



#### DEFAULTDELAY [time] 

(Optionnel) Permet de définir un temps d'attente entre chaque commande (ms * 10). Exemple : si time vaut 10, on obtient un délai de 100ms entre chaque commande.  



#### DELAY [time]

Permet de définir un temps d'attente. Le temps spécifié est en milliseconde et peut prendre une valeur entre 1 à 10000. 



#### WINDOWS

Raccourcis [Windows + r] qui permet sur Windows d'accéder à l'exécuteur de commande.



#### MENU 

Raccourcis [SHIFT F10] qui correspond, sur Windows, à un clic droit. Il affiche un menu ou un contexte menu (copier, coller,...)



#### GUI [Single Char]

Permet d'effectuer un raccourcis [Windows + touche(optionnel)] du clavier. 



#### ALT [END, ESC, F1...F12, Single Char, ESPACE, SPACE, TAB]

Permet d'effectuer un raccourcis [ALT gauche + touche] du clavier.



#### CTRL [BREAK, PAUSE, F1...F12, ESC, Single Char]

Permet d'effectuer un raccourcis [CTRL + touche] du clavier.

#### 

#### SHIFT [DELETE, HOME, INSERT, PAGE_UP, PAGE_DOWN, ARROW_U, ARROW_D, ARROW_L, ARROW_R, TAB, GUI]

Permet d'effectuer un raccourcis [SHIFT + touche] du clavier.



#### STRING [Char, Symbole, Num]

Chaîne de caractère transmise à l'identique. Peut être composée de 1 ou plusieurs caractères. Exemple : String abc déf *@à€ ?´^.:- 



#### Commandes supplémentaires correspondant à une touche précise

APP                 // Touche spéciale (affiche le menu / context menu)
ARROW_R             // Touche flèche droite
ARROW_L             // Touche flèche gauche
ARROW_U             // Touche flèche haut
ARROW_D             // Touche flèche bas
BACKSPACE           // Touche backspace (supprime le dernier caractère)
CAPSLOCK            // Touche caps lock (active/désactive)
DELETE              // Touche delete / del
END                 // Touche end   (retour à la fin de la ligne)
ENTER / RETURN      // Touche enter
ESC                 // Touche esc
ESPACE /SPACE       // Touche espace
GUI                 // Touche windows
HOME                // Touche home  (retour au début de la ligne)
INSERT              // Touche insert / ins
PAGE_UP             // Touche pg up (retour début de la page)
PAGE_DOWN           // Touche pg dn (retour fin de la page)
PRINT               // Touche prt sc
SCROLL_LOCK         // Touche scroll lock
TAB                 // Touche de tabulation 
