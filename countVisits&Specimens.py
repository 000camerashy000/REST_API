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
loginData = {
    "loginName": "av",
    "password": "ashishOpen1@",
    "domainName": "openspecimen"
}

# CP Id to extract Participants
getCprs = {
    "cpId": 4,
    "maxResults": 10
}

# Resources
baseUrl = "http://localhost:80/rest/ng/"
loginUrl = baseUrl + "sessions"
participantUrl = baseUrl + "collection-protocol-registrations/list"
visitsUrl = baseUrl + "visits"

# Get Participant ID and Visits data
with requests.Session() as session:
    loginResponse = session.post(loginUrl, json=loginData, headers={"Content-Type": "application/json"})
    token = loginResponse.json()["token"]

    # Get Participant ID
    participantResponse = session.post(participantUrl, json=getCprs, headers={"Content-Type": "application/json", "X-OS-API-TOKEN": token})
    participantIds = [participant["participant"]["id"] for participant in participantResponse.json()]

    # Get Visits data and count visits and total specimens for each PPID
    visitsCount = defaultdict(int)
    totalSpecimenCount = defaultdict(int)

    for participantId in participantIds:
        visitsResponse = session.get(visitsUrl + f"?cprId={participantId}&includeStats=true", headers={"Content-Type": "application/json", "X-OS-API-TOKEN": token})
        visitsData = visitsResponse.json()

        for visit in visitsData:
            if "id" in visit:
                ppid = visit.get("ppid")
                storedSpecimens = visit.get("storedSpecimens")
                notStoredSpecimens = visit.get("notStoredSpecimens")
                visitsCount[ppid] += 1
                totalSpecimenCount[ppid] += storedSpecimens + notStoredSpecimens

# Write data to CSV
with open("specimenCount_python.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    csvwriter.writerow(["ppid", "total_visits", "total_specimens_all_visit"])
    for ppid in visitsCount.keys():
        csvwriter.writerow([ppid, visitsCount[ppid], totalSpecimenCount[ppid]])
