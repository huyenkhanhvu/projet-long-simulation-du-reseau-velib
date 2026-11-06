import random
from network import Network
from router import Router
from algorithms.distance_vector import DistanceVector
from user import User

def run(random_mode=False):
    net = Network()

    # Création d'une grille 3x3
    nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    for name in nodes:
        net.add_router(Router(name, DistanceVector()))
    # Liens horizontaux
    net.add_link(net.routers["A"], net.routers["B"], 2)
    net.add_link(net.routers["B"], net.routers["C"], 2)
    net.add_link(net.routers["D"], net.routers["E"], 2)
    net.add_link(net.routers["E"], net.routers["F"], 2)
    net.add_link(net.routers["G"], net.routers["H"], 2)
    net.add_link(net.routers["H"], net.routers["I"], 2)
    # Liens verticaux
    net.add_link(net.routers["A"], net.routers["D"], 2)
    net.add_link(net.routers["D"], net.routers["G"], 2)
    net.add_link(net.routers["B"], net.routers["E"], 2)
    net.add_link(net.routers["E"], net.routers["H"], 2)
    net.add_link(net.routers["C"], net.routers["F"], 2)
    net.add_link(net.routers["F"], net.routers["I"], 2)

    for r in net.routers.values():
        r.algorithm.initialize()

    if random_mode:
        print("\n Génération de 10 cyclistes !")
        for i in range(1, 11):
            src = net.routers[random.choice(nodes)]
            dst = net.routers[random.choice(nodes)]
            while dst == src: 
                dst = net.routers[random.choice(nodes)]
            net.add_user(User(f"Velo_{i}", src, dst))
    else:
        print("\n Engorgement planifié !")
        
        net.add_user(User("U1", net.routers["A"], net.routers["I"]))
        net.add_user(User("U2", net.routers["A"], net.routers["H"]))
        net.add_user(User("U3", net.routers["B"], net.routers["I"]))
        net.add_user(User("U4", net.routers["B"], net.routers["G"]))
        net.add_user(User("U5", net.routers["C"], net.routers["G"]))
        net.add_user(User("U6", net.routers["I"], net.routers["A"]))
    return net