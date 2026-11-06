import copy

class Network:
    def __init__(self):
        self.routers = {}
        self.base_links = {}
        self.links = {}
        self.time = 0
        self.history = []
        self.users = []

    def add_router(self, router):
        self.routers[router.id] = router
        router.network = self

    def add_link(self, r1, r2, cost=1):
        link_id = tuple(sorted([r1.id, r2.id]))
        self.base_links[link_id] = cost
        self.links[link_id] = cost
        r1.add_neighbor(r2, cost)
        r2.add_neighbor(r1, cost)

    def update_link_cost(self, r1, r2, new_cost):
        link_id = tuple(sorted([r1.id, r2.id]))
        if link_id in self.links:
            self.links[link_id] = new_cost
            r1.neighbors[r2] = new_cost
            r2.neighbors[r1] = new_cost

    def remove_link(self, r1, r2):
        link_id = tuple(sorted([r1.id, r2.id]))
        if link_id in self.links:
            del self.links[link_id]
            del self.base_links[link_id]
            r1.neighbors.pop(r2, None)
            r2.neighbors.pop(r1, None)

    def add_user(self, user):
        self.users.append(user)
        user.current_router.network = self

    def save_state(self):
        clean_tables = {}
        for r in self.routers.values():
            clean_tables[r.id] = {}
            for dest, (cost, next_hop) in r.algorithm.table.items():
                clean_tables[r.id][dest] = (cost, next_hop.id)

        user_states = []
        users_at_nodes = {r_id: 0 for r_id in self.routers}

        for u in self.users:
            user_states.append({
                "id": u.id, "dest": u.destination.id,
                "current": u.current_router.id,
                "next": u.next_router.id if u.next_router else None,
                "ticks_left": u.ticks_remaining, "arrived": u.arrived
            })
            
            if u.ticks_remaining == 0:
                users_at_nodes[u.current_router.id] += 1

        snapshot = {
            "tick": self.time,
            "tables": clean_tables,
            "links": self.links.copy(),
            "users": user_states,
            "users_at_nodes": users_at_nodes 
        }
        self.history.append(snapshot)

    def tick(self):
       
        link_traffic = {link_id: 0 for link_id in self.base_links.keys()}
        
        for u in self.users:
            if u.ticks_remaining > 0 and u.next_router:
                link_id = tuple(sorted([u.current_router.id, u.next_router.id]))
                if link_id in link_traffic:
                    link_traffic[link_id] += 1
                    
        for link_id, base_cost in self.base_links.items():
            new_cost = base_cost + link_traffic[link_id]
            if self.links.get(link_id) != new_cost:
                r1_id, r2_id = link_id
                self.update_link_cost(self.routers[r1_id], self.routers[r2_id], new_cost)
                
        updated = False
        for router in self.routers.values():
            if router.process_messages():
                updated = True

        for router in self.routers.values():
            router.send_updates()

        for user in self.users:
            user.step()

        self.save_state()
        self.time += 1
        return updated