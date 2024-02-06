#Import Libraries
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
    
    # Check if login is successful
    if loginResponse.status_code != 200:
        print("Login failed. Status code:", loginResponse.status_code)
        exit()
        
    token = loginResponse.json()["token"]

    # Get Participant ID
    participantResponse = session.post(participantUrl, json=getCprs, headers={"Content-Type": "application/json", "X-OS-API-TOKEN": token})
    
    # Check if participant data is retrieved successfully
    if participantResponse.status_code != 200:
        print("Failed to retrieve participant data. Status code:", participantResponse.status_code)
        exit()
        
    participantIds = [participant["participant"]["id"] for participant in participantResponse.json()]

    # Get Visits data and count visits and total specimens for each PPID
    visitsCount = defaultdict(int)
    totalSpecimenCount = defaultdict(int)

    for participantId in participantIds:
        visitsResponse = session.get(visitsUrl + f"?cprId={participantId}&includeStats=true", headers={"Content-Type": "application/json", "X-OS-API-TOKEN": token})
        
        # Check if visit data is retrieved successfully
        if visitsResponse.status_code != 200:
            print(f"Failed to retrieve visit data for participant ID {participantId}. Status code:", visitsResponse.status_code)
            continue
            
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
