import math
from message import Message
from algorithms.base import RoutingAlgorithm

INF = math.inf

class DistanceVector(RoutingAlgorithm):
    def __init__(self):
        super().__init__()
        self.table = {}

    def initialize(self):
        
        r = self.router
        self.table[r.id] = (0, r)
        for neighbor, cost in r.neighbors.items():
            self.table[neighbor.id] = (cost, neighbor)

    def clean_dead_routes(self):
       
        routes_to_delete = []
        for dest, (cost, next_hop) in self.table.items():
            if dest != self.router.id and next_hop not in self.router.neighbors:
                routes_to_delete.append(dest)   
        for dest in routes_to_delete:
            del self.table[dest]
        return len(routes_to_delete) > 0

    def process_messages(self, messages):
        updated = self.clean_dead_routes()
        r = self.router
        for msg in messages:
            sender = msg.sender
            cost_to_sender = r.neighbors.get(sender)
            if cost_to_sender is None:
                continue
            for dest, cost in msg.vector.items():
                new_cost = cost_to_sender + cost
                if dest not in self.table:
                    self.table[dest] = (new_cost, sender)
                    updated = True
                else:
                    current_cost, current_next_hop = self.table[dest]
                    if new_cost < current_cost or (current_next_hop == sender and new_cost != current_cost):
                        self.table[dest] = (new_cost, sender)
                        updated = True
        return updated

    def create_messages(self):

        self.clean_dead_routes()
        r = self.router
        messages = []

        for neighbor in r.neighbors:
            vector = {}
            for dest, (cost, next_hop) in self.table.items():
                if next_hop != neighbor:
                    vector[dest] = cost
            msg = Message(r, vector)
            messages.append((neighbor, msg))
        return messages
