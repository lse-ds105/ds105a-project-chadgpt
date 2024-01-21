import json
import requests as r
import sys
import spacy

# AUTHENTICATE WITH CREDENTIALS TO GET ACCESS TOKEN AND HEADERS
def authenticate_and_get_headers(filepath="../credentials.json"):
    '''
    Authenticate with the Reddit API using a credentials.json file, and gets a header dict for use in subsequent GET requests.

    Args:
        filepath (str): path specifying the location of the credentials.json file

    Returns:
        dict: a dictionary of headers, including Reddit access token, ready to be used in subsequent GET requests
    '''

    # From Reddit's API documentation, this is the endpoint I need
    ACCESS_TOKEN_ENDPOINT = "https://www.reddit.com/api/v1/access_token"

    # Open the file and load the data into a variable
    with open(filepath, "r") as f:
        credentials = json.load(f)

    # Set up authentication parameters 
    client_auth = r.auth.HTTPBasicAuth(credentials["app_client_id"], credentials["app_client_secret"])
    
    # Send, via HTTP POST, your Reddit username and password
    post_data = {"grant_type": "password",
                "username": credentials["reddit_username"],
                "password": credentials["reddit_password"]}

    # Reddit API requests that we identify ourselves in the User-Agent
    headers = {"User-Agent": f"LSE DS105A Recipe Scraping Project by {credentials['reddit_username']}"}

    # Send a HTTP POST 
    response = r.post(ACCESS_TOKEN_ENDPOINT, auth=client_auth, data=post_data, headers=headers)

    my_token = response.json()['access_token']

    headers = {"Authorization": f"bearer {my_token}",
               "User-Agent": f"LSE DS105A Recipe Scraping Project by {credentials['reddit_username']}"}
    
    return headers

def is_english(text, model):
    '''
    Checks if text is in English

    Args:
        text (str): the text to be parsed.
        model (Language): the NLP model to be loaded. Note that the model must be downloaded using pip and loaded to be used.
    
    Returns:
        (bool): True if the text is in English; False otherwise.    
    '''
    # Process the text using spaCy
    doc = model(text)
    
    # return True if the text is in English, False otherwise
    return doc.lang_ == 'en'