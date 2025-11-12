import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzYzNTc4ODc1fQ.2q1ux8SaPgHRxu9vgkjI3XItppgUE0IEZr2CkzPRk9Y"
}

request = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(request)
print(request.json())
