from network import Network
from router import Router
from algorithms.distance_vector import DistanceVector
from user import User

def run():
    net = Network()

    for name in ["A", "B", "C", "D"]:
        net.add_router(Router(name, DistanceVector()))

    net.add_link(net.routers["A"], net.routers["B"], 1)
    net.add_link(net.routers["B"], net.routers["C"], 2)
    net.add_link(net.routers["C"], net.routers["D"], 1)

    for r in net.routers.values():
        r.algorithm.initialize()

    u1 = User("Alice", source=net.routers["A"], destination=net.routers["D"])
    net.add_user(u1)
    
    u2 = User("Bob", source=net.routers["C"], destination=net.routers["A"])
    net.add_user(u2)

    return net

def dynamic_event(net, tick):
    if tick == 5:
        print("\n Charlie commence son trajet de B vers D")
        u3 = User("Charlie", source=net.routers["B"], destination=net.routers["D"])
        net.add_user(u3)