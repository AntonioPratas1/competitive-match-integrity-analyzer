# Run the backend analysis pipeline.
#
# Actions :
# - Load reports, players, and events
# - Fetch player stats
# - Build player_summary_stats.csv
# - Calculate triage scores
# - Save player_summary_triage.csv
#-------------------------------------------------


import os
import pandas as pd

from utils.data_loader import load_data
from utils.scoring import triage_score
from utils.player_stats import get_fnrank_stats

# Load Data 

players, events, reports = load_data()

player_stats_rows = []

# Fetch player stats from fnrank

for _, player in players.iterrows():
    stats = get_fnrank_stats(player["player_name"])

    if stats is not None:
        player_stats_rows.append(stats)

player_summary_stats = pd.DataFrame(player_stats_rows)

player_summary_stats.to_csv(
    "outputs/player_summary_stats.csv",
    index=False
)

player_summary_stats = pd.read_csv("outputs/player_summary_stats.csv")

# Count reports per player and event

report_counts = (
    reports.groupby(["event_id", "reported_player_id"])
    .size()
    .reset_index(name="total_reports_this_event")
)

# Combine reports, players, events, and stats

merged = reports.merge(
    players, 
    left_on="reported_player_id",
    right_on="epic_account_id",
    how="left"
)
merged = merged.merge(
    events,
    on="event_id",
    how="left"
)
merged= merged.merge(
    player_summary_stats,
    on="player_name",
    how="left"
)

# print(merged.shape)
# print(merged.head())

if merged.empty:
    print("No reports found yet. Skipping triage.")
    exit()

merged = merged.merge(
    report_counts,
    on=["event_id", "reported_player_id"],
    how="left"
)

# Calculate triage score 
merged["triage_score"] = merged.apply(triage_score, axis=1)

# print(merged[["player_name", "event_name", "triage_score"]])

player_summary =(
    merged.groupby("player_name", as_index=False)
    .agg({
        "triage_score":"mean",
        "total_reports_this_event":"max"
    })
    .sort_values(by="triage_score", ascending=False)    
)

def risk_label(score):
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    else:
        return "LOW"
player_summary["risk_label"] = player_summary["triage_score"].apply(risk_label)

player_summary["manual_review"] = player_summary["total_reports_this_event"] >= 20

# print("\n=== Player Ranking ===")
# print(player_summary)

player_summary.to_csv("outputs/player_summary_triage.csv", index=False)
print("\nSaved to outputs/player_summary_triage.csv")