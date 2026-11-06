from network import Network
from router import Router
from algorithms.distance_vector import DistanceVector


def run():
    net = Network()

    A = Router("A", DistanceVector())
    B = Router("B", DistanceVector())
    C = Router("C", DistanceVector())
    D = Router("D", DistanceVector())

    for r in [A, B, C, D]:
        net.add_router(r)

    net.add_link(A, B, 1)
    net.add_link(B, C, 1)
    net.add_link(C, D, 1)
    net.add_link(D, A, 1)

    for r in net.routers.values():
        r.algorithm.initialize()
    return net
