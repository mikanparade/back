import requests, json

url = "http://127.0.0.1:8000/api/users/example@example.com"

data = { "email": "akira@example.com", "password": "password" }

data = json.dumps(data)

response = requests.put(url, data=data)

print(response)