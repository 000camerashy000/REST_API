getSessions() {
  getToken=$(curl -X POST \
    http://localhost:80/rest/ng/sessions \
    -H 'Content-Type: application/json' \
    -d '{
      "loginName": "av",
      "password": "ashishOpen1@",
      "domainName": "openspecimen"
    }')


  token=$(echo $getToken | jq -r '.token')

  echo "The token is: $token"
}

main() {
  getSessions
}

main;
