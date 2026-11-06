from network import Network
from router import Router
from algorithms.distance_vector import DistanceVector


def run():
    net = Network()

    A = Router("A", DistanceVector())
    B = Router("B", DistanceVector())
    C = Router("C", DistanceVector())

    for r in [A, B, C]:
        net.add_router(r)

    net.add_link(A, B, 1)
    net.add_link(B, C, 1)
    net.add_link(A, C, 5)

    for r in net.routers.values():
        r.algorithm.initialize()
    return net
