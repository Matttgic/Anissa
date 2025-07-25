# get_fixtures.py

import requests
import datetime

# Clé API personnelle (tu peux aussi la charger depuis un fichier .env si tu préfères)
API_KEY = "1df93a4239msh5776d5f2c3b3a91p147a3ejsnea4c93adaca3"
API_HOST = "api-football-v1.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

# IDs des 5 grandes ligues européennes
LEAGUES = {
    "Premier League": 39,
    "Bundesliga": 78,
    "Serie A": 135,
    "Ligue 1": 61,
    "La Liga": 140
}

def get_fixtures(league_id, start_date, end_date):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params = {
        "league": league_id,
        "from": start_date,
        "to": end_date,
        "season": 2025,
        "status": "NS"  # NS = Not Started
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f"❌ Erreur API {response.status_code}: {response.text}")
        return []

    data = response.json()
    return data.get("response", [])

def print_fixtures():
    today = datetime.date.today()
    seven_days_later = today + datetime.timedelta(days=7)

    start_date = today.isoformat()
    end_date = seven_days_later.isoformat()

    for name, league_id in LEAGUES.items():
        print(f"\n📅 Matchs à venir : {name}")
        fixtures = get_fixtures(league_id, start_date, end_date)

        if not fixtures:
            print("  Aucun match trouvé.")
            continue

        for match in fixtures:
            fixture = match["fixture"]
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            date = fixture["date"]
            match_id = fixture["id"]
            print(f"  - {home} vs {away} | {date} | ID: {match_id}")

if __name__ == "__main__":
    print_fixtures()
