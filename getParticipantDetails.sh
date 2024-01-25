#!/bin/bash
getToken=$(curl -X POST \
  http://localhost:80/rest/ng/sessions \
  -H 'Content-Type: application/json' \
  -d '{
    "loginName": "av",
    "password": "ashishOpen1",
    "domainName": "openspecimen"
  }')


token=$(echo $getToken | jq -r '.token')

my_token=$token

# Retrieve the JSON response from the API
response=$(curl -X POST \
  http://localhost:80/rest/ng/collection-protocol-registrations/list \
  -H 'Content-Type: application/json' \
  -H "X-OS-API-TOKEN: $my_token" \
  -d '{
    "cpId": 4,
    "name": "AV",
    "maxResults": 25
  }')

# Extract data and convert it into a csv file.

jq -r '.[] | [.cpTitle, .ppid, .participant.firstName, .activityStatus, (.participant.races | join(",")), (.participant.ethnicities | join(","))] | @csv' <<< "$response" >> cp_registration_data.csv



