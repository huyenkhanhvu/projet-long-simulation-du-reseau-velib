from network import Network
from router import Router
from algorithms.distance_vector import DistanceVector


def run():
    net = Network()

    A = Router("A", DistanceVector())
    B = Router("B", DistanceVector())
    C = Router("C", DistanceVector())

    net.add_router(A)
    net.add_router(B)
    net.add_router(C)

    net.add_link(A, B, cost=1)
    net.add_link(B, C, cost=1)

    for r in net.routers.values():
        r.algorithm.initialize()
    return net
