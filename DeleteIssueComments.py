import requests
import json
import re
from getpass import getpass

# READ ME: Before running this script, please input the JSON response from Chrome Dev Tools into 'text' to Extract the Comment UIDs for deletion

# Define the text (use Chrome Dev tools to get JSON response for comment details - See below example for reference)

text = """
  {
    "response": {
        "code": "SUCCESS",
        "data": {
            "totalCount": 3,
            "items": [
                {
                    "issueCommentUid": "4de3ce7fae64",
                    "commentText": "test\n",
                    "createdDate": "2024-04-06T22:49:18Z",
                    "commentTextModifiedDate": null,
                    "createdByUserUid": "22a26bafd1bc",
                    "createdByWatcherUid": null,
                    "taggedUsers": []
                },
                {
                    "issueCommentUid": "cafd37932fc5",
                    "commentText": "test4\n",
                    "createdDate": "2024-04-06T22:49:22Z",
                    "commentTextModifiedDate": null,
                    "createdByUserUid": "22a26bafd1bc",
                    "createdByWatcherUid": null,
                    "taggedUsers": []
                },
                {
                    "issueCommentUid": "56b82ffd44e4",
                    "commentText": "test7",
                    "createdDate": "2024-04-06T22:49:27Z",
                    "commentTextModifiedDate": null,
                    "createdByUserUid": "22a26bafd1bc",
                    "createdByWatcherUid": null,
                    "taggedUsers": []
                }
            ]
        }
    }
}
"""

print('To bulk delete comments from an issue, please follow the below prompts: \n\n');

# Define username(Admin), password(Admin) + Project and Job Uid for the Job you want to download here
username = input('Enter Smartling Admin Email Address: ')
password = getpass('Enter Smartling Dashboard Password: ')
projectUid = input('Enter Project Uid: ')
issueUid = input('Enter Issue Uid: ')

# 1 -------------------------------- AUTHENTICATE --------------------------------

# Authenticate (Use your Admin Email Address as userIdentified and Dashboard Password as userSecret)
api_parameters = {
    'userIdentifier': username,
    'userSecret': password
}

# Define the request URL
api_url = "https://api.smartling.com/auth-api/v2/authenticate/user"

# Make post request
api_response = requests.post(api_url, json=api_parameters)

# Check if authentication was successful
if api_response.status_code == 200 and 'accessToken' in api_response.json()['response']['data']:
    # Store access token for use in subsequent API calls
    access_token = api_response.json()['response']['data']['accessToken']
    print("Authentication successful\n")
else:
    print("Authentication failed. Response:", api_response.json())

# -------------------------------- Get Comment Uids --------------------------------

# Regular expression to find issueCommentUid values
pattern = r'"issueCommentUid": "([^"]+)"'

# Find all matches
matches = re.findall(pattern, text)

# Join the matches into a comma-separated string
result = ','.join(matches)

# 2 -------------------------------- Delete Issue Comments --------------------------------


count = 0

for match in matches:
    # Define the request URL
    url = "https://api.smartling.com/issues-api/v2/projects/" + projectUid + "/issues/" + issueUid + "/comments/" + match

    # Add the access token to the headers
    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    # Make get request
    response = requests.delete(url, headers=headers)

    # Check if list files call was successful
    if response.status_code == 200:
        print("Comment deleted for Comment Uid: " + match)
        count+=1
    else:
        print("Error, could not delete Comment Uid: " + match)


print("Bulk action complete. " + str(count) + " comments deleted.")