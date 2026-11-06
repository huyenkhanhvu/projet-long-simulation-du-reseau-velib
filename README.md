Simulateur de réseaux et traffic cycliste:

Ce projet a pour origine un simulateur de réseaux qui a pour objectif final de simuler un parc de vélos connecter et les contraintes qui y sont lier dans la vie de tout les jours.

Description :

Ce projet est un simulateur de réseau permettant d’implémenter, tester et visualiser des algorithmes de routage, pour l'instant il implémente une version de l'algorithme "Distance Vector" avec des l'implémentation de "cycliste" ainsi qu'un moyen de visualiser le tout.
Pour l'utilisation on a besoin d'installer une version de python récente (testé avec Python 3.12), certains bibliothèques python, notamment networkx et matplotlib. 

Le projet s'organise de la sorte pour l'insant :

simulator
├── algorithms
│   ├── base.py
│   ├── distance_vector.py
├── main.py
├── message.py
├── network.py
├── router.py
├── tests
│   ├── test_dynamic_large_network.py
│   ├── test_dynamic.py
│   ├── test_line.py
│   ├── test_link_costs.py
│   ├── test_ring.py
│   ├── test_traffic.py
│   └── test_users.py
├── user.py
├── utils.py
└── visualizer.py

Lancer le scénario de trafic urbain, il suffit de faire la commande (elle lance le scénario par défaut):
python3 main.py

Lancer le scénario spécifique (plusieur possible "large","dynamic","line","link_costs","ring","users","traffic"):
python3 main.py --test large

L'option "--ticks" permet de mettre un nombre maximal de tick pour la simulation
L'option "--no-visual" permet d'éviter l'ouverture du visualiser
L'option "--random" permet d'avoir un version aléatoire du test traffic

Pour le visualizer on peux naviger a traver les ticks a l'aide des flêche "<-" et "->" qui permet d'avancer ou de reculer d'un tick

Objectif Futur :

[] Utilisation de data disponible librement pour des test plus intéressant
[] Mise en place de stock (faire en sorte simuler des dépôt de vélos avec un parc qui a un stock de vélos disponible, chaque user en prend 1 et le libére a l'autre place, si un user veux en prendre 1, un velo doit être dispo la ou il arrive)
[] Mise en place de corrélation avec l'heure (temps réel ou simulation, objectif faire dépendre les coûts initiale selon la saturation des voie selon l'heure)

Auteurs

Projet réalisé dans le cadre d’un projet universitaire.
Développé par : Vu Khanh Huyen & Goddet Lucas