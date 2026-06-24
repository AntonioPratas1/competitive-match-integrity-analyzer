# Calculates player statistics usde by the analyzer.
# Actions:
# - Match statistics
# - Placement statistics
# - Kill statistics
# - Summary metrics for reports and reviews
# ----------------------------------------------------


import requests

def get_fnrank_stats(player_name):
    url = f"https://fnrank.com/api/player/{player_name}"
    response = requests.get(url)

    if response.status_code != 200:
        return None
    
    data = response.json()
    try:
        overall = data["stats"]["detailed"]["all"]["overall"]
    except KeyError:
        return None
    
    return {
        "player_name": data["account"]["name"],
        "playtime_hours": round(overall.get("minutes_played", 0) / 60, 2),
        "total_tracked_events": None,
        "total_tracked_matches": overall.get("matches", 0),
        "avg_placement_history": None,
        "avg_kills_history": overall.get("killsPerMatch", 0),
        "win_rate": overall.get("winRate", 0),
        "total_kills": overall.get("kills", 0),
        "wins": overall.get("wins", 0),
        "kd": overall.get("kd", 0)
    }

if __name__ == "__main__":
    print(get_fnrank_stats('Rafael-ZH'))
    
