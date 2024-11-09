import requests

url = "http://127.0.0.1:8080/generate"
data = {"text": "Test input for embedding"}

try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except ValueError:
    print("Response was not JSON:", response.text)
