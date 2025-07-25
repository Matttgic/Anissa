# update_player_cache.py

import os
import json
from datetime import datetime, timedelta

CACHE_DIR = "cache_players"
os.makedirs(CACHE_DIR, exist_ok=True)

def normalize_filename(name):
    return name.lower().replace(" ", "_").replace(".", "").replace("-", "_")

def is_cache_fresh(player_file):
    with open(player_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    last = datetime.fromisoformat(data.get("last_update", "2000-01-01"))
    return (datetime.now() - last) < timedelta(days=7)

def update_cache_for_players(players):
    for p in players:
        name = p["name"]
        player_id = p["id"]
        pos = p["pos"]

        filename = f"{CACHE_DIR}/{normalize_filename(name)}.json"
        if os.path.exists(filename):
            if is_cache_fresh(filename):
                print(f"✅ {name} déjà en cache (à jour)")
                continue
            else:
                print(f"♻️ {name} en cache mais trop vieux → à mettre à jour")
        else:
            print(f"🆕 {name} non présent en cache → création")

        data = {
            "player_id": player_id,
            "name": name,
            "position": pos,
            "last_update": datetime.now().isoformat(),
            "scouting_report": {}  # sera rempli plus tard par scraping FBref
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    # 🧪 Exemple avec 2 joueurs extraits des compos
    players = [
        {"id": 789, "name": "Mohamed Salah", "pos": "F"},
        {"id": 456, "name": "Martin Ø
