# test_scrape_scouting_report.py

import requests
from bs4 import BeautifulSoup
import re

def find_fbref_url(player_name):
    # Recherche via Bing (Google bloque souvent les bots)
    query = f"site:fbref.com {player_name}"
    url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # Cherche le premier lien fbref
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "fbref.com/en/players" in href:
            return href
    return None

def get_scouting_report(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    report = {}

    scouting_table = soup.find("table", {"id": "scout_summary"})
    if not scouting_table:
        print("❌ Scouting Report introuvable sur cette page.")
        return report

    for row in scouting_table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 2:
            stat_name = cells[0].text.strip()
            percentile = cells[1].text.strip()
            # Nettoyage : parfois "99" ou "99th" ou "-"
            if percentile.isdigit():
                report[stat_name] = int(percentile)

    return report

if __name__ == "__main__":
    player_name = "Mohamed Salah"
    print(f"🔍 Recherche de l’URL FBref pour {player_name}...")
    url = find_fbref_url(player_name)

    if url:
        print(f"➡️ URL trouvée : {url}")
        print(f"📊 Récupération du scouting report...")
        report = get_scouting_report(url)

        if report:
            print(f"✅ Scouting Report de {player_name} :\n")
            for stat, pct in report.items():
                print(f"{stat:30s} : {pct}")
        else:
            print("⚠️ Aucun report trouvé.")
    else:
        print("❌ Impossible de trouver la page FBref.")
