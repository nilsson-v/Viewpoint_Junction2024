import requests
import json

def create_conversation(topic, description):
    # Base URL for the API
    base_url = "https://polis-api-proxy.onrender.com/api/v3/conversations"
    
    # Simplified payload
    payload = {
        "topic": topic,
        "description": description
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(base_url, data=json.dumps(payload), headers=headers)
        
        # Debugging information
        print("Request URL:", response.request.url)
        print("Request Headers:", response.request.headers)
        print("Request Body:", response.request.body)
        
        # Check the response status
        if response.status_code == 200:
            print("Conversation created successfully!")
            print(response.json())
        else:
            print(f"Failed to create conversation. Status code: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Test the simplified request
if __name__ == "__main__":
    create_conversation("Test Topic", "Testing the API without optional fields.")
