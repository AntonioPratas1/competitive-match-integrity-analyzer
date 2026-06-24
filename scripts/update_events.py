# Downloads and updates Fortnite event data from CITO API into data/events.csv
# Fields saved : 
# - event_id
# - event_name
# - region
# - start_time
# - end_time
# - status
#-----------------------------------------------------------------------------

import requests
import pandas as pd

print("Starting test...")

API_KEY = "cito_055d026cf2df290726b104a8414cefe5f4e84d28996f517801cbdb965c343029"

url = "https://api.citoapi.com/api/v1/fortnite/tournaments/upcoming"

headers = {
    "x-api-key": API_KEY
  }

response = requests.get(url, headers=headers)

data = response.json()

print(type(data))

events = data["data"]

events_list = events["epic"]

rows = []

for event in events_list:
    rows.append({
        "event_id": event["eventId"],
        "event_name": event["name"],
        "region": event["eventId"].split("_")[-1],
        "start_time": event["startTime"],
        "end_time": event["endTime"],
        "status": event["status"]
    })
events_df = pd.DataFrame(rows)
events_df.to_csv("data/events.csv", index=False)
print("Events CSV updated!")
print(events_df.head())
