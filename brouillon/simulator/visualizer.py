import matplotlib.pyplot as plt
import networkx as nx

class NetworkVisualizer:
    def __init__(self, network):
        self.network = network
        self.tick = 0
        self.display_page = 0 
        
        if hasattr(self.network, 'arrondissement_label'):
            if self.network.arrondissement_label == "Tout Paris":
                self.mode = "tout_paris"
                self.max_pages = 20
            else:
                self.mode = "single_arr"
                self.max_pages = 1
        else:
            self.mode = "standard"
            self.max_pages = 1
        
        self.fig, (self.ax_graph, self.ax_text) = plt.subplots(
            1, 2, figsize=(18, 9), gridspec_kw={'width_ratios': [3, 2]}
        )
        self.fig.canvas.manager.set_window_title("Simulateur de Trafic Cycliste")
        
        self.base_G = nx.Graph()
        if self.network.history:
            initial_snapshot = self.network.history[0]
            for (u, v), cost in initial_snapshot.get("links", {}).items():
                self.base_G.add_edge(u, v)
            for node in initial_snapshot["tables"].keys():
                self.base_G.add_node(node)

        self.pos = {}
        self.has_gps = True  
        
        for node in self.base_G.nodes():
            router = self.network.routers.get(node)
            if router and hasattr(router, 'lon') and hasattr(router, 'lat'):
                self.pos[node] = (router.lon, router.lat) 
            else:
                self.has_gps = False
                break
                
        if not self.has_gps:
            self.pos = nx.spring_layout(self.base_G, seed=42)
            
        xs = [coord[0] for coord in self.pos.values()]
        ys = [coord[1] for coord in self.pos.values()]
        if xs and ys:
            dx = max(xs) - min(xs)
            dy = max(ys) - min(ys)
            dx = dx if dx > 0 else 0.1
            dy = dy if dy > 0 else 0.1
            self.xlim = (min(xs) - dx * 0.1, max(xs) + dx * 0.1)
            self.ylim = (min(ys) - dy * 0.1, max(ys) + dy * 0.1)
        else:
            self.xlim, self.ylim = None, None
            
        self.node_to_num = {node: str(i+1) for i, node in enumerate(sorted(self.base_G.nodes()))}

        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.draw()
        plt.show()

    def on_key(self, event):
        if not self.network.history:
            return
            
        max_tick = len(self.network.history) - 1
        if event.key == 'right' and self.tick < max_tick:
            self.tick += 1
            self.draw()
        elif event.key == 'left' and self.tick > 0:
            self.tick -= 1
            self.draw()
        elif event.key == 'up':
            self.display_page = min(self.max_pages, self.display_page + 1)
            self.draw()
        elif event.key == 'down':
            self.display_page = max(0, self.display_page - 1)
            self.draw()

    def draw(self):
        self.ax_graph.clear()
        self.ax_text.clear()
        self.ax_text.axis('off')

        if not self.network.history:
            return

        snapshot = self.network.history[self.tick]
        tables = snapshot["tables"]
        links = snapshot.get("links", {})
        users_at_nodes = snapshot.get("users_at_nodes", {})

        G = nx.Graph()
        for node in self.base_G.nodes():
            G.add_node(node)
        for (u, v), cost in links.items():
            G.add_edge(u, v, weight=cost)

        node_colors = []
        labels = {}
        
        if self.tick == 0:
            node_colors = ["lightblue"] * len(G.nodes())
        else:
            prev_tables = self.network.history[self.tick - 1]["tables"]
            for node in G.nodes():
                node_colors.append("orange" if tables[node] != prev_tables[node] else "lightblue")

        is_massive = len(G.nodes()) > 150

        if is_massive:
            nx.draw(G, self.pos, node_color=node_colors, node_size=15, 
                    ax=self.ax_graph, edge_color="lightgray", width=0.5)
        else:
            for node in G.nodes():
                num = self.node_to_num[node]
                count = users_at_nodes.get(node, 0)
                if count > 0:
                    labels[node] = f"{num}\n({count})" 
                else:
                    labels[node] = num
                    
            nx.draw(G, self.pos, labels=labels, node_color=node_colors, 
                    node_size=250, font_weight="bold", ax=self.ax_graph, edge_color="gray", font_size=7)
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, self.pos, edge_labels=edge_labels, ax=self.ax_graph, font_size=7)

        if self.xlim and self.ylim:
            self.ax_graph.set_xlim(self.xlim)
            self.ax_graph.set_ylim(self.ylim)

        if self.mode == "tout_paris":
            title = f"Topologie : Tout Paris (Carte GPS) - Tick {self.tick}"
        elif self.mode == "single_arr":
            title = f"Topologie : Arrondissement {self.network.arrondissement_label} (Carte GPS) - Tick {self.tick}"
        else:
            gps_text = " (Carte GPS)" if self.has_gps else ""
            title = f"Topologie{gps_text} - Tick {self.tick}"
            
        self.ax_graph.set_title(title, fontsize=14, pad=15)
        
        nodes_list = sorted(G.nodes())
        all_users = snapshot.get("users", [])
        
        if self.mode in ["standard", "single_arr"]:
            if self.display_page == 0:
                self.ax_text.set_title(f"Infos Stations (Page 1/2) - Tick {self.tick}", fontsize=12, pad=10)
                text_info = "LEGENDE DES STATIONS :\n"
                
                for i in range(0, len(nodes_list), 2):
                    parts = []
                    for j in range(2):
                        if i + j < len(nodes_list):
                            n = nodes_list[i+j]
                            clean_name = n.strip()[:35]
                            parts.append(f"[{self.node_to_num[n]}] {clean_name}".ljust(45))
                    text_info += " | ".join(parts) + "\n"
                    
                text_info += "\nTABLES DE ROUTAGE (Abregees) :\n"
                
                table_lines = []
                for node in nodes_list:
                    routes = [f"Vers.{self.node_to_num[dest]}:{cost}" 
                              for dest, (cost, nh_id) in tables[node].items() if dest != node]
                    if routes:
                        routes_str = " | ".join(routes[:2])
                        if len(routes) > 2:
                            routes_str += "..."
                        table_lines.append(f"[{self.node_to_num[node]}]-> {routes_str}")
                    else:
                        table_lines.append(f"[{self.node_to_num[node]}]-> Isole")

                for i in range(0, len(table_lines), 2):
                    str1 = table_lines[i].ljust(45)
                    if i + 1 < len(table_lines):
                        str2 = table_lines[i+1]
                        text_info += f"{str1} | {str2}\n"
                    else:
                        text_info += f"{str1}\n"
                
                text_info += "\nAppuyez sur 'HAUT' ou 'BAS' pour voir les cyclistes."

            else:
                self.ax_text.set_title(f"Liste des Cyclistes (Page 2/2) - Tick {self.tick}", fontsize=12, pad=10)
                text_info = "CYCLISTES EN TRANSIT (Tous):\n"
                
                user_lines = []
                if all_users:
                    for u in all_users:
                        if u["arrived"]:
                            user_lines.append(f"[Arrive] {u['id']} a st.{self.node_to_num[u['dest']]}")
                        elif u["next"]:
                            user_lines.append(f"[Route] {u['id']} vers st.{self.node_to_num[u['next']]} ({u['ticks_left']}t)")
                        else:
                            user_lines.append(f"[Attend] {u['id']} a st.{self.node_to_num[u['current']]}")
                            
                    for i in range(0, len(user_lines), 3):
                        parts = []
                        for j in range(3):
                            if i + j < len(user_lines):
                                parts.append(user_lines[i+j].ljust(30))
                        text_info += " | ".join(parts) + "\n"
                else:
                    text_info += "Aucun cycliste sur le reseau.\n"
                    
                text_info += "\nAppuyez sur 'HAUT' ou 'BAS' pour revenir aux stations."

        elif self.mode == "tout_paris":
            if self.display_page == 0:
                self.ax_text.set_title(f"VUE GLOBALE (Page 0/20) - Tick {self.tick}", fontsize=12, pad=10)
                text_info = "STATISTIQUES GLOBALES :\n\n"
                text_info += f"Nombre total de stations : {len(G.nodes())}\n"
                text_info += f"Nombre total de connexions (rues) : {len(G.edges())}\n"
                text_info += f"Cyclistes en circulation : {len(all_users)}\n\n"
                
                arrived_count = sum(1 for u in all_users if u["arrived"])
                text_info += f"Cyclistes arrives a destination : {arrived_count}\n"
                text_info += f"Cyclistes en cours de trajet : {len(all_users) - arrived_count}\n\n"
                text_info += "-" * 40 + "\n"
                text_info += "Utilisez la fleche 'HAUT' pour voir les details\n"
                text_info += "specifiques de l'arrondissement 1, puis 2, 3...\n"
                text_info += "Utilisez 'GAUCHE / DROITE' pour avancer dans le temps."
                
            else:
                arr_cible = self.display_page
                self.ax_text.set_title(f"Focus Arrondissement {arr_cible} (Page {arr_cible}/20) - Tick {self.tick}", fontsize=12, pad=10)
                
                arr_nodes = [n for n in G.nodes() if hasattr(self.network.routers[n], 'arrondissement') and self.network.routers[n].arrondissement == arr_cible]
                text_info = f"STATIONS DU {arr_cible}e ARRONDISSEMENT :\n"
                
                if not arr_nodes:
                    text_info += "\nAucune station dans cet arrondissement.\n"
                else:
                    for i in range(0, len(arr_nodes), 2):
                        parts = []
                        for j in range(2):
                            if i + j < len(arr_nodes):
                                n = arr_nodes[i+j]
                                clean_name = n.strip()[:35]
                                parts.append(f"[{self.node_to_num[n]}] {clean_name}".ljust(45))
                        text_info += " | ".join(parts) + "\n"
                        
                text_info += f"\nCYCLISTES LIES AU {arr_cible}e :\n"
                
                arr_users = []
                for u in all_users:
                    if (u["current"] in arr_nodes) or (u["dest"] in arr_nodes) or (u["next"] and u["next"] in arr_nodes):
                        arr_users.append(u)
                        
                if not arr_users:
                    text_info += "\nAucun cycliste dans ce secteur pour le moment.\n"
                else:
                    user_lines = []
                    for u in arr_users:
                        if u["arrived"]:
                            user_lines.append(f"[Arrive] {u['id']} a st.{self.node_to_num[u['dest']]}")
                        elif u["next"]:
                            user_lines.append(f"[Route] {u['id']} vers st.{self.node_to_num[u['next']]} ({u['ticks_left']}t)")
                        else:
                            user_lines.append(f"[Attend] {u['id']} a st.{self.node_to_num[u['current']]}")
                            
                    for i in range(0, len(user_lines), 2):
                        parts = []
                        for j in range(2):
                            if i + j < len(user_lines):
                                parts.append(user_lines[i+j].ljust(45))
                        text_info += " | ".join(parts) + "\n"

        self.ax_text.text(0.0, 1.0, text_info, transform=self.ax_text.transAxes, 
                          fontsize=8, verticalalignment='top', family='monospace')
        
        self.fig.tight_layout()
        plt.draw()