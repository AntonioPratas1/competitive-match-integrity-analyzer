# Handles Epic Games player lookups.

# Actions : 
# - Search for players by username
# - Retrieve Epic Account information
# - Return data used by the reporting system
# -----------------------------------------------

import requests

def search_epic_players(query):
    url = "https://epicgames.tools/api/search/suggestions"

    payload = {
        "query": query,
        "searchType": "epic_display_name"
    }

    response = requests.post(url, json=payload)

    data = response.json()

    return data["suggestions"]
