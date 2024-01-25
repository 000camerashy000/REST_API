response=$(curl -X POST \
  http://localhost:80/rest/ng/sessions \
  -H 'Content-Type: application/json' \
  -d '{
    "loginName": "av",
    "password": "ashishOpen1",
    "domainName": "openspecimen"
  }')


token=$(echo $response | jq -r '.token')


my_token=$token
echo "The token is: $my_token"
