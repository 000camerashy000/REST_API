response=$(curl -X POST \
  http://localhost:80/rest/ng/sessions \
  -H 'Content-Type: application/json' \
  -d '{
    "loginName": "av",
    "password": "ashishOpen1",
    "domainName": "openspecimen"
  }')


token=$(echo $response | jq -r '.token')


curl -X GET \
  http://localhost:80/rest/ng/collection-protocols/4 \
  -H 'Content-Type: application/json' \
  -H "X-OS-API-TOKEN: $token"
