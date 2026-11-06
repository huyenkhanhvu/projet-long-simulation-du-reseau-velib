from network import Network
from router import Router
from algorithms.distance_vector import DistanceVector

def run():
    net = Network()

    for name in ["A","B","C","D","E","F","G","H","I"]:
        net.add_router(Router(name, DistanceVector()))

    # Liens initiaux
    net.add_link(net.routers["A"], net.routers["B"], 1)
    net.add_link(net.routers["B"], net.routers["C"], 1)
    net.add_link(net.routers["B"], net.routers["D"], 1)
    net.add_link(net.routers["C"], net.routers["E"], 1)
    net.add_link(net.routers["D"], net.routers["F"], 1)
    net.add_link(net.routers["E"], net.routers["F"], 1)
    net.add_link(net.routers["E"], net.routers["G"], 2)
    net.add_link(net.routers["F"], net.routers["G"], 2)
    net.add_link(net.routers["G"], net.routers["H"], 1)
    net.add_link(net.routers["H"], net.routers["I"], 1)

    for r in net.routers.values():
        r.algorithm.initialize()
    return net

def dynamic_event(net, tick):
    
    if tick == 5:
        print("\n Panne du lien E-F")
        net.remove_link(net.routers["E"], net.routers["F"])
        
    elif tick == 12:
        print("\n Augementation entre B et D ! Le coût passe de 1 à 5")
        net.update_link_cost(net.routers["B"], net.routers["D"], 5)