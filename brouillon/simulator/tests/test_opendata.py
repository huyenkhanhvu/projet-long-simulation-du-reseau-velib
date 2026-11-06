from network import Network
from data_loader import load_velib_network
from user import User
import random

def run(arrondissement=1):
    net = Network()
    csv_path = "velib-disponibilite-en-temps-reel.csv"
    
    # Si arrondissement vaut 0, on charge TOUT Paris (limite a 800 stations)
    # Sinon on charge l'arrondissement demande (limite a 70 stations)
    limit = 800 if arrondissement == 0 else 70
    arr_filter = None if arrondissement == 0 else arrondissement
    
    load_velib_network(net, csv_path, arrondissement=arr_filter, max_stations=limit)

    print(f"\nGeneration de cyclistes basee sur l'inventaire des stations...")
    routers = list(net.routers.values())
    
    if not routers:
        print("Erreur : Aucune station trouvee pour cet arrondissement.")
        return net
        
    user_id_counter = 1
    
    # Si on charge tout Paris, on ne fait partir que 5% des velos pour eviter que nos pc meurt
    spawn_rate = 0.05 if arrondissement == 0 else 0.20
    
    for router in routers:
        nb_cyclistes = int(router.bikes * spawn_rate)
        
        for _ in range(nb_cyclistes):
            dst = random.choice(routers)
            while dst == router:
                dst = random.choice(routers)
            
            net.add_user(User(f"V_{user_id_counter}", router, dst))
            user_id_counter += 1

    print(f"{user_id_counter - 1} cyclistes injectes dans le reseau")
    
    net.arrondissement_label = "Tout Paris" if arrondissement == 0 else str(arrondissement)
    
    return net