import re
import requests
from fake_useragent import UserAgent 

# Which localized URL would you like to Extract Hashcodes from?
localizedUrl = ""

# Append EM3 parameter to URL
localizedUrlEM3 = localizedUrl + "?smartling_editmode=3"

def extract_hash_values_from_url(url):
    # Create a fake user-agent to mimic Chrome
    user_agent = UserAgent().chrome

    # Set headers with the fake user-agent
    headers = {'User-Agent': user_agent}

    # Fetch the HTML content of the webpage
    response = requests.get(url, headers=headers)
    html_content = response.text

    # Use regular expression to find all occurrences of the pattern
    pattern = r'STRING TRANSLATE BEGIN HASH:([a-fA-F0-9]+)'
    hash_values = re.findall(pattern, html_content)
    return hash_values

# Call the function:
hash_values = extract_hash_values_from_url(localizedUrlEM3)

# Print the extracted hash values as a single string with commas
hash_values_string = ', '.join(hash_values)
print("Extracted Hash Values:", hash_values_string)