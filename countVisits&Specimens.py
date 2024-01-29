"""

------------------- PSEUDO-CODE --------------------

Step 1: Authenticate
Step 2: Using Authentication, retrieve participant IDs
Step 3: Extract participants IDs for a CP and store in variable
Step 4: Iterate over the participant IDs to get Visit Details // (Collected Visits have 'id' in the JSON response) && (total specimen for a visit = 'storedSpecimens' + 'notStoredSpecimens')
Step 5: Check if visit response has 'id' i.e. collected visits
        If yes, extract (PPID/Participant Identifer) and storedSpecimens and notStoredSpecimens (storedSpecimen + notStoredSpecimens = totalSpecimen per Visit)
Step 6: Calculate Visit Count by calculating the ids obtain for a pariticpant, and add the totalSpecimen count per visit to get totalSpecimen count per Pariticipant.
Step 7: Add the data in csv file.

---------------------------------------------------

"""

# Import Libraries
from collections import defaultdict
import requests
import csv

# Credintials
login_data = {
    "loginName": "av",
    "password": "ashishOpen1@",
    "domainName": "openspecimen"
}

# CP Id to extract Participants
getCPRs = {
    "cpId": 4,
    "maxResults": 10
}

# Resources
base_url = "http://localhost:80/rest/ng/"
login_url = base_url + "sessions"
participant_url = base_url + "collection-protocol-registrations/list"
visits_url = base_url + "visits"

# Get Participant ID and Visits data
with requests.Session() as session:
    login_response = session.post(login_url, json=login_data, headers={"Content-Type": "application/json"})
    token = login_response.json()["token"]

    # Get Participant ID
    participant_response = session.post(participant_url, json=getCPRs, headers={"Content-Type": "application/json", "X-OS-API-TOKEN": token})
    participant_ids = [participant["participant"]["id"] for participant in participant_response.json()]

    # Get Visits data and count visits and total specimens for each PPID
    visit_counts = defaultdict(int)
    total_specimens_counts = defaultdict(int)

    for participant_id in participant_ids:
        visits_response = session.get(visits_url + f"?cprId={participant_id}&includeStats=true", headers={"Content-Type": "application/json", "X-OS-API-TOKEN": token})
        visits_data = visits_response.json()

        for visit in visits_data:
            if "id" in visit:
                ppid = visit.get("ppid")
                stored_specimens = visit.get("storedSpecimens")
                not_stored_specimens = visit.get("notStoredSpecimens")
                visit_counts[ppid] += 1
                total_specimens_counts[ppid] += stored_specimens + not_stored_specimens

# Write data to CSV
with open("specimenCount_python.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    csvwriter.writerow(["ppid", "total_visits", "total_specimens_all_visit"])
    for ppid in visit_counts.keys():
        csvwriter.writerow([ppid, visit_counts[ppid], total_specimens_counts[ppid]])
