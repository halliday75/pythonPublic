import re
import requests
from fake_useragent import UserAgent 

# Array of URLs to extract hashcodes from
localizedUrls = ["url1", "url2"]

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

# Extract hash values for each URL in the array
all_hash_values = []
for url in localizedUrls:
    # Ensure the URL starts with 'http'
    if url[:4] != 'http':
        url = 'https://' + url
    localizedUrlEM3 = url + "?smartling_editmode=3"
    hash_values = extract_hash_values_from_url(localizedUrlEM3)
    all_hash_values.extend(hash_values)

# Print the extracted hash values as a single string with commas
#hash_values_string = ','.join(all_hash_values)
#print("Extracted Hash Values:", hash_values_string)

# Write the extracted hash values to a file
with open("extractedHashcodes.txt", "w") as file:
    hash_values_string = ','.join(all_hash_values)
    file.write(hash_values_string)

print("Hashcodes have been exported to 'extractedHashcodes.txt'")