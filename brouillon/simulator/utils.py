import time

def draw_network(network):
    print("\nNetwork topology")
    for router in network.routers.values():
        neighbors = []
        for neigh, cost in router.neighbors.items():
            neighbors.append(f"{neigh.id}({cost})")
        print(f"{router.id} -- " + ", ".join(neighbors))


def display_routing_tables(network, highlight_changes=False):
    print("\nRouting tables")
    for router in network.routers.values():
        print(f"Router {router.id}")
        for dest, (cost, next_hop) in router.algorithm.table.items():
            marker = "*" if highlight_changes else " "
            print(f"{marker} -> {dest} : cost={cost}, via={next_hop.id}")


def animate_tick(network, delay=1.0):
    print(f"\nTICK {network.time}")
    draw_network(network)
    updated = network.tick()
    display_routing_tables(network, highlight_changes=updated)
    time.sleep(delay)
    return updated
