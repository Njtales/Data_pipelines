import requests
import json

url = 'http://localhost:9090/browser/server_groups/1/servers'

payload = {
    "name": "default_dev",
    "host": "172.20.0.3",
    "port": 5432,
    "database": "airflow",
    "username": "airflow",
    "password": "airflow"
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.text)