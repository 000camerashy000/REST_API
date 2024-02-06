#!/bin/bash

createCsv() {
  cat << END_OF_HEADERS > cp_registration_data.csv
  cpTitle,ppid,firstName,activityStatus,races,ethnicities
END_OF_HEADERS

  jq -r '.[] | [.cpTitle, .ppid, .participant.firstName, .activityStatus, (.participant.races | join(",")), (.participant.ethnicities | join(","))] | @csv' <<< "$response" >> cp_registration_data.csv

}

getParticipants() {
  response=$(curl -X POST \
  'http://localhost:80/rest/ng/collection-protocol-registrations/list' \
  -H 'Content-Type: application/json' \
  -H "X-OS-API-TOKEN: $token" \
  -d '{
    "cpId": 4,
    "maxResults": 1
  }')

  echo $response

}

getSessions() {
  getToken=$(curl -X POST \
  'http://localhost:80/rest/ng/sessions' \
  -H 'Content-Type: application/json' \
  -d '{
    "loginName": "av",
    "password": "ashishOpen1@",
    "domainName": "openspecimen"
  }')

  token=$(echo $getToken | jq -r '.token')
  echo $token

}

main () {
  getSessions
  getParticipants
  createCsv

}

main;

