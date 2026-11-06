from network import Network
from router import Router
from algorithms.distance_vector import DistanceVector

def run():
    net = Network()

    for name in ["A", "B", "C"]:
        net.add_router(Router(name, DistanceVector()))

    net.add_link(net.routers["A"], net.routers["B"], 1)
    net.add_link(net.routers["B"], net.routers["C"], 1)

    for r in net.routers.values():
        r.algorithm.initialize()
    return net

def dynamic_event(net, tick):
    if tick == 3:
        print("\n Suppression du lien B-C")
        net.remove_link(net.routers["B"], net.routers["C"])