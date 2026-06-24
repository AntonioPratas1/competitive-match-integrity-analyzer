# Frontend interface for submitting player reports.
# 
# Actions:
# - Display report form
# - Search Epic usernames
# - Select live Fortnite events 
# - Save reports to reports.csv
# - Add new players to players.csv
# ---------------------------------------------------

import streamlit as st
import pandas as pd
from datetime import date
from utils.player_lookup import search_epic_players



# App Header
st.title("Competitive Integrity Analyzer")
st.write("Submit a player report")

# Report form Inputs
reporter_username = st.text_input("Reporter Username:")
reported_player_search = st.text_input("Reported Player:")
suggestions = []

# Search Epic usernames
if reported_player_search:
    suggestions = search_epic_players(reported_player_search)

if suggestions:
    player_options = [
        f'{player["value"]} | {player["platform"]}'
        for player in suggestions
    ]   
    selected_player_display = st.selectbox(
        "Select player:",
        player_options
    )
    selected_player_index = player_options.index(selected_player_display)
    selected_player = suggestions[selected_player_index]

# Load available events
events_df = pd.read_csv("data/events.csv")
live_events_df = events_df[events_df["status"] == "live"]
st.success("🟢 Live tournaments only")
event_name = st.selectbox(
    "Event Name",
    live_events_df["event_name"].unique()
)
selected_event = events_df[events_df["event_name"] == event_name].iloc[0]
match_number = st.text_input("Match Number:")
reason = st.text_input("Reason :")

reports_path = "data/reports.csv"
reports_df = pd.read_csv(reports_path)
if reports_df.empty or reports_df["report_id"].isna().all():
    new_report_id = 1
else:
    new_report_id = int(reports_df["report_id"].max() + 1)

players_path = "data/players.csv"
players_df = pd.read_csv(players_path)

# Save report
if st.button("Submit Report"):

    new_player = {
        "player_name": selected_player["value"],
        "epic_account_id": selected_player["accountId"],
        "platform": selected_player["platform"]
    }
    
    player_exists = (
        players_df["epic_account_id"]
        .astype(str)
        .eq(str(selected_player["accountId"]))
        .any()
        )
    if not player_exists:
        new_player_df = pd.DataFrame([new_player])

        updated_players = pd.concat(
            [players_df, new_player_df],
            ignore_index=True
        )

        updated_players.to_csv(
            players_path,
            index=False
        )


    new_report = {
        "report_id": new_report_id,
        "event_id": selected_event["event_id"],
        "reported_player_name": selected_player["value"],
        "reported_player_id": selected_player["accountId"],
        "match_number": match_number,
        "reporter_id": reporter_username,
        "report_reason": reason,
        "timestamp": str(date.today())
    }

    reports_df = pd.read_csv(reports_path)
    new_report_df = pd.DataFrame([new_report])
    updated_reports = pd.concat([reports_df, new_report_df], ignore_index=True)
    updated_reports.to_csv(reports_path, index=False)

    st.success("Report submitted sucessfully!")
    st.write(new_report)
