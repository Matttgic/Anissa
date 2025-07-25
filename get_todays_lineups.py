# get_todays_lineups.py

import requests
import datetime

API_KEY = "1df93a4239msh5776d5f2c3b3a91p147a3ejsnea4c93adaca3"
API_HOST = "api-football-v1.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

LEAGUES = {
    "Premier League": 39,
    "Bundesliga": 78,
    "Serie A": 135,
    "Ligue 1": 61,
    "La Liga": 140
}

def get_fixtures_today(league_id, date_str):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params = {
        "league": league_id,
        "date": date_str,
        "season": 2025,
        "status": "NS"  # Not Started = match à venir
    }

    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"❌ Erreur {response.status_code} pour league {league_id}")
        return []

    return response.json().get("response", [])

def get_lineups(fixture_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/lineups"
    params = { "fixture": fixture_id }

    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"❌ Erreur lineups pour match {fixture_id}")
        return []

    return response.json().get("response", [])

def run():
    today = datetime.date.today().isoformat()
    print(f"📅 Date du jour : {today}")

    for league_name, league_id in LEAGUES.items():
        print(f"\n🏆 {league_name}")
        fixtures = get_fixtures_today(league_id, today)

        if not fixtures:
            print("  Aucun match aujourd’hui.")
            continue

        for match in fixtures:
            fixture_id = match["fixture"]["id"]
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            print(f"\n➡️  {home} vs {away} | ID: {fixture_id}")

            lineups = get_lineups(fixture_id)
            if not lineups:
                print("  ❌ Aucune composition disponible pour ce match.")
                continue

            for team in lineups:
                print(f"  📋 {team['team']['name']}")
                for player in team.get("startXI", []):
                    p = player["player"]
                    print(f"    - {p['name']} | Poste: {p['pos']} | Numéro: {p['number']} | ID: {p['id']}")

if __name__ == "__main__":
    run()
