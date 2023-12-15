import requests
import json

data = {"email": "akira@icloud.com", "password": "password"}

response = requests.post("http://127.0.0.1:8000/api/users/me/delete", json=data)

print(response.status_code)
print(response.json())