
# Run Parsehub scrapping project and get the token of the run
run_token=$(curl -s -X POST https://www.parsehub.com/api/v2/projects/tKvGjvJ33SZ4/run -d api_key=$API_KEY | jq -r .run_token)
echo "Run token: " $run_token

# Wait until the run is completed
run_status=$(curl -s -X GET "https://www.parsehub.com/api/v2/runs/${run_token}?api_key=$API_KEY" | jq -r .status)
echo "Run status: " $run_status
while [ $run_status != complete ]; do
  echo "Wait..."
  sleep 1
  run_status=$(curl -s -X GET "https://www.parsehub.com/api/v2/runs/${run_token}?api_key=$API_KEY" | jq -r .status)
  echo "Run status: " $run_status
done

sleep 2

echo "Downloading data"
curl -X GET "https://www.parsehub.com/api/v2/runs/${run_token}/data?api_key=$API_KEY" --output b3_companies_scrapped.gz

