import requests
from collections import deque
import time

BASE_URL = "https://hire-game-maze.pertimm.dev/"

def start_game(player):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'player': player}
    r = requests.post(BASE_URL + "start-game/", data=data, headers=headers)
    return r.json()

def discover(url):
    return requests.get(url).json()

def move(url, x, y):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'position_x': str(x), 'position_y': str(y)}
    return requests.post(url, data=data, headers=headers).json()

def main():
    player = ""
    while not player.strip():
        player = input("Nom du joueur : ").strip()

    state = start_game(player)
    if not state or not state.get("player"):
        print("Erreur d'initialisation :", state.get("message") if state else "Pas de réponse JSON")
        return

    print(f"Départ : ({state['position_x']}, {state['position_y']})")
    start_pos = (state["position_x"], state["position_y"])
    url_move = state["url_move"]
    url_discover = state["url_discover"]

    queue = deque()
    queue.append((start_pos, [start_pos], url_move, url_discover))
    visited = set()
    step = 0

    while queue:
        pos, path, url_move, url_discover = queue.popleft()
        if pos in visited:
            continue
        visited.add(pos)
        print(f"\nÉtape {step}: À la position {pos}, chemin parcouru : {path}")
        voisins = discover(url_discover)
        for cell in voisins:
            print(f"  - Voisin ({cell['x']}, {cell['y']}) | value: {cell['value']} | move: {cell['move']}")
        for cell in voisins:
            next_pos = (cell["x"], cell["y"])
            if not cell["move"]:
                continue
            if cell["value"] in ("wall", "trap"):
                print(f"    Case ({next_pos}) ignorée (mur ou piège)")
                continue
            if next_pos in path:
                print(f"    Case ({next_pos}) déjà visitée sur ce chemin")
                continue
            print(f"    On tente d'avancer vers {next_pos} ...")
            nstate = move(url_move, cell["x"], cell["y"])
            time.sleep(0.05)
            if nstate["dead"]:
                print(f"    Perdu : tombé dans un piège au {next_pos} !")
                return
            chemin = path + [next_pos]
            if nstate["win"]:
                print(f"\nVictoire ! Arrivée atteinte en {len(chemin)-1} déplacements.")
                print("Chemin :", chemin)
                return
            queue.append(((nstate["position_x"], nstate["position_y"]), chemin, nstate["url_move"], nstate["url_discover"]))
        step += 1

    print("\nAucune sortie trouvée dans ce labyrinthe.")

if __name__ == "__main__":
    main()
