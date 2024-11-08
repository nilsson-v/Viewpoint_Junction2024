import requests

url = "http://127.0.0.1:8080/generate"
data = {"text": "Test input for embedding"}

response = requests.post(url, json=data)

print(response.json())
