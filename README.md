# Simulation d'un réseau de vélos en libre-service

Projet universitaire de simulation de réseau et de trafic cycliste, inspiré des problématiques d'un système de vélos en libre-service comme Vélib'.

## Présentation

Ce projet propose un simulateur permettant de tester et visualiser des algorithmes de routage sur un réseau, tout en intégrant des cyclistes et des scénarios de trafic. Il sert à observer l'évolution des itinéraires et des comportements du réseau au fil de la simulation.

Le simulateur comprend actuellement une implémentation de l'algorithme "Distance Vector", plusieurs scénarios de test et un outil de visualisation.

**Périmètre :** la gestion des stocks de vélos en station et l'adaptation des coûts à l'heure de la journée font partie des évolutions envisagées, et non des fonctionnalités annoncées comme terminées.

## Fonctionnalités

- Simulation d'un réseau de routage.
- Implémentation de l'algorithme "Distance Vector".
- Intégration d'utilisateurs / cyclistes dans les simulations.
- Scénarios de test portant notamment sur la topologie, les changements dynamiques et le trafic.
- Visualisation de l'évolution de la simulation, tick par tick.
- Paramétrage du nombre maximal de ticks et possibilité de désactiver l'affichage graphique.

## Technologies

- **Langage :** Python (projet testé avec Python 3.12)
- **Bibliothèques :** NetworkX, Matplotlib

## Installation

### 1. Récupérer le dépôt

```
git clone https://github.com/huyenkhanhvu/projet-long-simulation-du-reseau-velib.git

cd projet-long-simulation-du-reseau-velib
```

### 2. Préparer l'environnement Python

```
python3 -m venv .venv

source .venv/bin/activate

python3 -m pip install networkx matplotlib
```


Sous Windows, l'activation s'effectue avec `.venv\Scripts\activate` dans l'invite de commandes.

### 3. Se placer dans le dossier du simulateur

Repérez le fichier `main.py` dans les sources du dépôt et ouvrez un terminal dans son dossier. Les commandes suivantes supposent que vous vous trouvez à cet emplacement.

## Utilisation

### Lancer la simulation par défaut


`python3 main.py`


Cette commande lance le scénario de trafic urbain par défaut.

### Choisir un scénario


`python3 main.py --test large`


Scénarios indiqués dans le projet :

| Scénario | Commande |
| --- | --- |
| Grand réseau | `python3 main.py --test large` |
| Réseau dynamique | `python3 main.py --test dynamic` |
| Topologie en ligne | `python3 main.py --test line` |
| Coûts des liens | `python3 main.py --test link_costs` |
| Topologie en anneau | `python3 main.py --test ring` |
| Utilisateurs | `python3 main.py --test users` |
| Trafic | `python3 main.py --test traffic` |

### Options disponibles

- `--ticks` : limite le nombre de ticks de la simulation.
- `--no-visual` : exécute la simulation sans ouvrir le visualiseur.
- `--random` : active une variante aléatoire du scénario de trafic.

Exemple :


`python3 main.py --test traffic --no-visual`


### Navigation dans la visualisation

Utilisez les flèches gauche et droite du clavier pour reculer ou avancer d'un tick.

## Organisation du code

Le README initial du projet décrit les modules suivants pour le simulateur :

```text
simulator/
├── algorithms/
│   ├── base.py
│   └── distance_vector.py
├── main.py
├── message.py
├── network.py
├── router.py
├── user.py
├── utils.py
├── visualizer.py
└── tests/
    ├── test_dynamic_large_network.py
    ├── test_dynamic.py
    ├── test_line.py
    ├── test_link_costs.py
    ├── test_ring.py
    ├── test_traffic.py
    └── test_users.py
```


## Perspectives d'amélioration

- [ ] Exploiter des jeux de données ouverts pour produire des scénarios plus réalistes.
- [ ] Modéliser les stocks de vélos dans les stations, avec emprunts et restitutions.
- [ ] Faire varier les coûts de déplacement en fonction de l'heure et de la saturation du trafic.

## Auteurs

Projet universitaire développé par **Vu Khanh Huyen** et **Goddet Lucas**.

## Référence

[Dépôt GitHub du projet](https://github.com/huyenkhanhvu/projet-long-simulation-du-reseau-velib)
