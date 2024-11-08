import requests
from config_private import APP_ID, APP_KEY
import re

# Define the API endpoint and parameters
url = "https://external.api.yle.fi/v1/teletext/pages/103.json"
params = {
    "app_id": APP_ID,
    "app_key": APP_KEY
}

# Define the API endpoint and parameters
url = "https://external.api.yle.fi/v1/teletext/pages/103.json"
params = {
    "app_id": APP_ID,
    "app_key": APP_KEY
}

# Compile regex pattern once for efficiency
formatting_pattern = re.compile(r"{[^}]*}")

try:
    # Make the request to the API and parse JSON response
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Extract text content from the first subpage
    text_lines = []
    seen_lines = set()  # Set to track unique lines and avoid duplicates
    subpage = data.get("teletext", {}).get("page", {}).get("subpage", [])[0]

    for content in subpage.get("content", []):
        for line in content.get("line", []):
            text = line.get("Text")
            if text:
                # Clean formatting markers and strip whitespace
                clean_text = formatting_pattern.sub("", text).strip()
                # Add to list if not seen before
                if clean_text and clean_text not in seen_lines:
                    text_lines.append(clean_text)
                    seen_lines.add(clean_text)  # Mark as seen

    # Join all lines into a single text block
    full_text = " ".join(text_lines)
    print(full_text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")