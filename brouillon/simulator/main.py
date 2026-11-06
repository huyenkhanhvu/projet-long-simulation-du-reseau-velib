import argparse
from visualizer import NetworkVisualizer

import tests.test_dynamic_large_network as test_large
import tests.test_dynamic as test_dyn
import tests.test_line as test_line
import tests.test_link_costs as test_link_costs
import tests.test_ring as test_ring
import tests.test_users as test_users
import tests.test_traffic as test_traffic
import tests.test_opendata as test_opendata

TESTS = {
    "large": test_large,
    "dynamic": test_dyn,
    "line": test_line,
    "link_costs": test_link_costs,
    "ring": test_ring,
    "users": test_users,
    "traffic": test_traffic,
    "opendata": test_opendata,
}

def display_tables(network):
  
    for r in network.routers.values():
        table = r.algorithm.table
        print(f"Station {r.id}: ", end="")
        routes = [f"Vers {dest}: {cost} (via {nh.id})" for dest, (cost, nh) in table.items()]
        print(" | ".join(routes))
    
 
    if hasattr(network, 'users') and network.users:
        print("\nEtat des cyclistes :")
        for u in network.users:
            if u.arrived:
                print(f"  [OK] {u.id} : Arrive a {u.destination.id}")
            elif u.next_router:
                print(f"  [->] {u.id} : En route vers {u.next_router.id} ({u.ticks_remaining} tick(s) restant)")
            else:
                print(f"  [..] {u.id} : Attend a la station {u.current_router.id} (cherche sa route)")

def run_simulation(net, max_ticks=20, dynamic_event=None, visual=True):
    for t in range(max_ticks):
        print(f"\nTICK {t} : ")

        if dynamic_event:
            dynamic_event(net, t)

        updated = net.tick()

        all_users_arrived = True
        if hasattr(net, 'users') and len(net.users) > 0:
            all_users_arrived = all(u.arrived for u in net.users)

        if not updated and dynamic_event is None and all_users_arrived:
            print("\nConvergence atteinte ET tous les trajets sont termines !")
            break

    if visual:
        print("\nLancement du visualiseur...")
        NetworkVisualizer(net)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", type=str, default="traffic", choices=TESTS.keys())
    parser.add_argument("--ticks", type=int, default=50) 
    parser.add_argument("--no-visual", action="store_true")
    parser.add_argument("--random", action="store_true", help="Active les destinations aleatoires")
    parser.add_argument("--arr", type=int, default=1, help="Arrondissement a simuler (1 a 20). 0 pour Tout Paris.")
    
    args = parser.parse_args()

    print(f"\nLancement du test : {args.test}")
    
    test_module = TESTS[args.test]
    
    if args.test == "traffic":
        net = test_module.run(random_mode=args.random)
    elif args.test == "opendata":
        net = test_module.run(arrondissement=args.arr)
    else:
        net = test_module.run()
        
    event_func = getattr(test_module, "dynamic_event", None)

    run_simulation(net, max_ticks=args.ticks, dynamic_event=event_func, visual=not args.no_visual)

if __name__ == "__main__":
    main()