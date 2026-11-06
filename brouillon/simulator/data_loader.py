import csv
import math
from router import Router
from algorithms.distance_vector import DistanceVector

PARIS_CENTERS = { # Centre des arrondissement (malheuresement paris a toujours pour code 75056 dans le csv)
    1: (48.8626, 2.3363), 2: (48.8683, 2.3429), 3: (48.8628, 2.3600),
    4: (48.8543, 2.3576), 5: (48.8444, 2.3486), 6: (48.8491, 2.3324),
    7: (48.8562, 2.3127), 8: (48.8727, 2.3125), 9: (48.8770, 2.3375),
    10: (48.8761, 2.3607), 11: (48.8591, 2.3782), 12: (48.8412, 2.3956),
    13: (48.8284, 2.3623), 14: (48.8292, 2.3265), 15: (48.8411, 2.2967),
    16: (48.8637, 2.2769), 17: (48.8835, 2.3219), 18: (48.8925, 2.3444),
    19: (48.8818, 2.3822), 20: (48.8635, 2.3984)
}

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000 # Rayon de la terre a peu près
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return int(R * c) # la distance en mètre qui les sépare

def get_closest_arrondissement(lat, lon):
    min_dist = float('inf')
    best_arr = -1
    for arr, (c_lat, c_lon) in PARIS_CENTERS.items():
        dist = haversine_distance(lat, lon, c_lat, c_lon)
        if dist < min_dist:
            min_dist = dist
            best_arr = arr
    return best_arr

def load_velib_network(network, csv_path, arrondissement=None, max_stations=100):
    print(f"Chargement des donnees de {csv_path}")
    stations_data = []
    
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        
        for row in reader:
            if row.get('Nom communes équipées') == 'Paris' and row.get('Station en fonctionnement') == 'OUI':
                
                coords = row['Coordonnées géographiques'].split(',')
                lat, lon = float(coords[0]), float(coords[1])
                
                station_arr = get_closest_arrondissement(lat, lon)
                
                if arrondissement is None or station_arr == arrondissement:
                    name = row['Nom station']
                    stations_data.append({
                        'id': name,
                        'name': name,
                        'lat': lat,
                        'lon': lon,
                        'capacity': int(row['Capacité de la station'] or 0),
                        'bikes': int(row['Nombre total vélos disponibles'] or 0),
                        'arrondissement': station_arr
                    })
                    
            if len(stations_data) >= max_stations:
                break

    print(f"{len(stations_data)} stations chargees. Creation du reseau.")

    routers_dict = {}
    for data in stations_data:
        full_name = data['name'].strip()
        r = Router(full_name, DistanceVector())
        
        r.capacity = data['capacity']
        r.bikes = data['bikes']
        r.lat = data['lat']
        r.lon = data['lon']
        r.arrondissement = data['arrondissement']
        
        routers_dict[full_name] = r
        network.add_router(r)

    routers_list = list(routers_dict.values())
    for r1 in routers_list:
        distances = []
        for r2 in routers_list:
            if r1 != r2:
                dist = haversine_distance(r1.lat, r1.lon, r2.lat, r2.lon)
                distances.append((dist, r2))
        
        distances.sort(key=lambda x: x[0])
        
        # On relie à 4 voisins (ou 3 pour un reseau geant afin d'alleger les calculs)
        max_voisins = 3 if arrondissement is None else 4
        for dist, r2 in distances[:max_voisins]:
            link_id = tuple(sorted([r1.id, r2.id]))
            if link_id not in network.links:
                cost = max(1, dist // 100) 
                network.add_link(r1, r2, cost)

    for r in network.routers.values():
        r.algorithm.initialize()

    return network