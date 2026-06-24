# Contains the triage scoring system used to rank reported players for manual review.
#
# Factors considered:
# - Report Counts
# - Match history
# - Performance metrics
# - Risk indicators
#------------------------------------------------------------------------------------

def triage_score(row):
    score = 0

    # Account Risk ---> need to add it later when i have access to events stats endpoint.
    #if row["total_tracked_events"] == 0:
    #    score += 35
    #elif row["total_tracked_events"] <= 2:
    #    score += 20

    # Smurf account? (Very Important) (Most cheaters use new accounts)
    if row["playtime_hours"] < 150:
        score += 10

    elif row["playtime_hours"] < 250:
        score += 5 

    # Lifetime performance risk from FNRank
    if row ["kd"] >= 5:
        score += 25
    elif row["kd"] >= 3:
        score += 12

    if row["avg_kills_history"] >= 5:
        score += 20
    elif row["avg_kills_history"] >= 3:
        score += 12     

    if row["win_rate"] >= 20:
        score += 15
    elif row["win_rate"] >= 10:
        score += 7

    if row["total_tracked_matches"] < 50:
        score += 35
    elif row["total_tracked_matches"] < 200:
        score += 5              
  
    # Kills = strongest current signal, softaim. ---> need to add it later when i have access to events stats endpoint.
    """if row["event_avg_kills"] >= row["avg_kills_history"] * 2:
        score += 45
        kill_flag = 2
    elif row["event_avg_kills"] >= row["avg_kills_history"] * 1.5:
        score += 30
        kill_flag = 1"""

    # Placement matters, ESP signal. ---> need to add it later when i have access to events stats endpoint.
    """if row["event_avg_placement"] < row["avg_placement_history"] * 0.6:
        score += 25
        placement_flag = 2
    elif row["event_avg_placement"] < row["avg_placement_history"] * 0.8:
        score += 18
        placement_flag = 1
    elif row["event_avg_placement"] < row["avg_placement_history"]:
        score += 10"""

    # Reports (still low weight) ----> too many rage reports.
    if row["total_reports_this_event"] >= 3:
        score += 5

    return score                    