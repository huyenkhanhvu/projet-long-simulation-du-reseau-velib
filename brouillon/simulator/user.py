import random

class User:
    def __init__(self, user_id, source, destination):
        self.id = user_id
        self.source = source
        self.destination = destination
        
        self.current_router = source
        self.next_router = None
        self.ticks_remaining = 0
        self.arrived = False
        
        self.has_bike = False 

    def step(self):
        if self.arrived:
            return

        if self.ticks_remaining > 0:
            self.ticks_remaining -= 1
            if self.ticks_remaining == 0:
                self.current_router = self.next_router
                self.next_router = None
                
                if self.current_router == self.destination:
                    
                    if hasattr(self.destination, 'bikes') and hasattr(self.destination, 'capacity'):
                        if self.destination.bikes < self.destination.capacity:
                            self.arrived = True
                            self.destination.bikes += 1 
                            self.has_bike = False
                        else:
                            voisins = list(self.destination.neighbors.keys())
                            if voisins:
                                self.destination = random.choice(voisins)
                    else:
                        # (ancienne version pour garder les autre test)
                        self.arrived = True
                        self.has_bike = False
                        
            return

        if self.ticks_remaining == 0 and not self.arrived:
            
            if not self.has_bike and self.current_router == self.source:
                
                if hasattr(self.current_router, 'bikes'):
                    if self.current_router.bikes > 0:
                        self.current_router.bikes -= 1 
                        self.has_bike = True
                    else:
                        # Aucun velo disponible, il attend au prochain tick
                        return
                else:
                    # (same)
                    self.has_bike = True

            if self.has_bike:
                table = self.current_router.algorithm.table
                
                if self.destination.id in table:
                    cost_to_dest, next_hop_router = table[self.destination.id]
                    
                    if cost_to_dest > 0:
                        link_cost = self.current_router.neighbors.get(next_hop_router)
                        
                        if link_cost is not None:
                            self.next_router = next_hop_router
                            self.ticks_remaining = link_cost