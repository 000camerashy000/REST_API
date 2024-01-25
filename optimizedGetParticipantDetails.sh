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


API_URL="http://localhost:80/rest/ng/collection-protocol-registrations/list"

# Use variables for data payload and headers
DATA_PAYLOAD='{"cpId": 4, "name": "AV", "maxResults": 25}'
HEADERS=(-H 'Content-Type: application/json' -H "X-OS-API-TOKEN: $my_token")

# Retrieve the JSON response from the API
response=$(curl -sSX POST "$API_URL" "${HEADERS[@]}" -d "$DATA_PAYLOAD")

# Extract data and convert it into a csv file.
jq -r '
  ["cpTitle", "ppid", "firstName", "activityStatus", "races", "ethnicities"] as $headers |
  ($headers | @csv), (.[] | [.cpTitle, .ppid, .participant.firstName, .activityStatus, (.participant.races | join(",")), (.participant.ethnicities | join(","))] | @csv)
' <<< "$response" > cp_registration_data.csv