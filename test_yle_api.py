import requests
from config_private import APP_ID, APP_KEY
import re


def call_yle_api(url, params):
    try:
        # Make the request to the API and parse JSON response
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        subpage = data.get("teletext", {}).get("page", {}).get("subpage", [])[0]

        return subpage
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def get_pages(url, params):
    subpage = call_yle_api(url, params)
    numbers = []
    for content in subpage.get("content", []):
        for line in content.get("line", []):
            text = line.get("Text")
            if text:
                match = re.match(r" \d+", text)  # Match digits at the beginning of the text
                if match:
                    numbers.append(match.group().strip())  # Append the matched number
    return numbers


def get_news_text(pages, params):

    data = {}
    # Compile regex pattern once for efficiency
    formatting_pattern = re.compile(r"{[^}]*}")

    for page in pages: 
        url = "https://external.api.yle.fi/v1/teletext/pages/" + page + ".json"

        # Extract text content from the first subpage
        text_lines = []
        seen_lines = set()  # Set to track unique lines and avoid duplicates

        subpage = call_yle_api(url, params)
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

        full_text = " ".join(text_lines)
        data[int(page)] = full_text
    
    return data


# Define the API endpoint and parameters
url = "https://external.api.yle.fi/v1/teletext/pages/102.json"
params = {
    "app_id": APP_ID,
    "app_key": APP_KEY
}

# Get all pages for KOTIMAA
pages = get_pages(url, params)
print(pages)

# Get the news for these pages
data = get_news_text(pages, params)
print(data)