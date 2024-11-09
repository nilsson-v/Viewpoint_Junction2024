import requests
from config_private import APP_ID, APP_KEY
import re
import json


def call_yle_api(url, params):
    """
    Calls the YLE API using the specified URL and parameters.

    Args:
        url (str): The URL endpoint for the YLE API.
        params (dict): The query parameters, including app ID and key.

    Returns:
        dict: A dictionary representing the first subpage of the response JSON,
              or None if an error occurs.
    """
    try:
        # Make the GET request to the API with the provided parameters
        response = requests.get(url, params=params)
        # Raise an error if the request was unsuccessful
        response.raise_for_status()
        # Parse the JSON response
        data = response.json()
        # Extract the first subpage data
        subpage = data.get("teletext", {}).get("page", {}).get("subpage", [])[0]
        return subpage
    except requests.exceptions.RequestException as e:
        # Print any request-related errors
        print(f"An error occurred: {e}")


def get_pages(url, params):
    """
    Retrieves page numbers from the YLE API response.

    Args:
        url (str): The API endpoint to retrieve pages from.
        params (dict): The parameters for the API request.

    Returns:
        list: A list of page numbers extracted from the response.
    """
    subpage = call_yle_api(url, params)
    numbers = []
    # Loop through content of the subpage to find lines with page numbers
    for content in subpage.get("content", []):
        for line in content.get("line", []):
            text = line.get("Text")
            if text:
                # Match digits at the beginning of the line text
                match = re.match(r" \d+", text)
                if match:
                    # Append matched numbers to the list after stripping whitespace
                    numbers.append(match.group().strip())
    return numbers


def get_news_text(pages, params):
    """
    Retrieves and formats text content from multiple pages.

    Args:
        pages (list): List of page numbers to retrieve.
        params (dict): The parameters for the API request.

    Returns:
        dict: A dictionary mapping page numbers to their corresponding text content.
    """
    data = {}
    # Compile a regex pattern to remove text formatting patterns
    formatting_pattern = re.compile(r"{[^}]*}")

    # Iterate through each page number to fetch its content
    for page in pages: 
        url = "https://external.api.yle.fi/v1/teletext/pages/" + page + ".json"
        text_lines = []
        seen_lines = set()  # Set to avoid adding duplicate lines

        # Fetch and parse the content of the subpage
        subpage = call_yle_api(url, params)
        for content in subpage.get("content", []):
            for line in content.get("line", []):
                text = line.get("Text")
                if text:
                    # Clean the line by removing formatting markers
                    clean_text = formatting_pattern.sub("", text).strip()
                    # Add cleaned text if it hasn't been seen before
                    if clean_text and clean_text not in seen_lines:
                        text_lines.append(clean_text)
                        seen_lines.add(clean_text)

        # Concatenate lines into a single string and associate with page number
        full_text = " ".join(text_lines)
        data[int(page)] = full_text
    
    return data


# Define the base API endpoint for the starting page and query parameters
url = "https://external.api.yle.fi/v1/teletext/pages/130.json"
params = {
    "app_id": APP_ID,
    "app_key": APP_KEY
}

# Retrieve list of pages for "KOTIMAA" section
pages = get_pages(url, params)
print(pages)

# Retrieve and format text content for each page
data = get_news_text(pages, params)
print(data)

# Define the path to the JSON file where the data will be saved
file_path = './news_data2.json'

# Open the JSON file in write mode
with open(file_path, 'w') as file:
    # Serialize and write the data dictionary to the file with indentation
    json.dump(data, file, indent=4)

# Confirm the JSON data has been written successfully
print(f"JSON data has been written to {file_path}")
