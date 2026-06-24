# Competitive Match Integrity Analyzer 

A Python-based application that analyzes competitive gaming data, player reports, and performance metrics to identify suspicious behavior patterns and assist with
tournament integrity reviews.

## Tech Stack

- Python
- Pandas
- Streamlit
- Requests
- CSV Data Storage

## Features

- Submit player reports
- Search Epic usernames
- Store reports in CSV format
- Fetch player statistics
- Generate player summaries
- Calculate triage scores
- Flag accounts for manual review

## Project Structure

data/          Raw project data
outputs/       Generated analysis files
scripts/       Maintenance Scripts        
utils/         Shared utility functions

## Run Application

streamlit run streamlit_app.py

## Run Analysis Pipeline

python run_triage.py

## Version

Current Release: v1.0

This project is under active development and new features will be added in future releases.

## Future improvement
1. Move generated CSVs into outputs/, stats and triage.
2. Players stats from events endpoint.
3. Player Profile Pages.
4. Ranking system between this players.