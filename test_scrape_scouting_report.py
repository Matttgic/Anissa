# test_scrape_scouting_report.py

import requests
from bs4 import BeautifulSoup

def get_scouting_report(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"❌ Erreur HTTP {r.status_code} pour {url}")
        return {}

    soup = BeautifulSoup(r.text, "html.parser")
    report = {}

    scouting_table = soup.find("table", {"id": "scout_summary"})
    if not scouting_table:
        print("❌ Scouting Report introuvable.")
        return report

    for row in scouting_table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 2:
            stat_name = cells[0].text.strip()
            percentile = cells[1].text.strip()
            if percentile.isdigit():
                report[stat_name] = int(percentile)

    return report

if __name__ == "__main__":
    url = "https://fbref.com/en/players/e342ad68/Mohamed-Salah"
    print(f"➡️ URL utilisée : {url}")
    print(f"📊 Récupération du scouting report...")

    report = get_scouting_report(url)

    if report:
        print(f"✅ Scouting Report récupéré :\n")
        for stat, pct in report.items():
            print(f"{stat:35s} : {pct}")
    else:
        print("⚠️ Aucun scouting report extrait.")
