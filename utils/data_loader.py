# Loads projects CSV files used by the analyzer.

# Files loaded:
# - players.csv
# - events.csv
# - reports.csv
# ------------------------------------------------

import pandas as pd

def load_data():
    players = pd.read_csv("data/players.csv")
    events = pd.read_csv("data/events.csv")
    reports = pd.read_csv("data/reports.csv")

    return players, events, reports