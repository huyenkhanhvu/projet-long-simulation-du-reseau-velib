class Router:
    def __init__(self, router_id, algorithm):
        self.id = router_id
        self.algorithm = algorithm
        self.algorithm.router = self

        self.neighbors = {}  
        self.inbox = []
        self.network = None

    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost

    def receive(self, message):
        self.inbox.append(message)

    def process_messages(self):
        updated = self.algorithm.process_messages(self.inbox)
        self.inbox = []
        return updated

    def send_updates(self):
        messages = self.algorithm.create_messages()
        for neighbor, msg in messages:
            neighbor.receive(msg)

    def display_routing_tables(network):
        print("\nRouting tables")
        for router in network.routers.values():
            print(f"Router {router.id}")
            for dest, (cost, next_hop) in router.algorithm.table.items():
                print(f"  -> {dest} : cost={cost}, via={next_hop.id}")
