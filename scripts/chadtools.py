import json
import requests as r
import spacy
import langid
from openai import OpenAI
import re

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

def is_english(text, threshold_rank=5):
    '''
    Checks if text is in English

    Args:
        text (str): the text to be parsed.
        threshold_rank (int): the threshold rank to be specified. A higher threshold means a looser requirement for English.
    
    Returns:
        (bool): True if the text is in English; False otherwise.    
    '''
    ranklist = langid.rank(text)
    langlist = [ranklist[x][0] for x in range(len(ranklist))]
    if 'en' not in langlist[:threshold_rank]: # if English is not in the top 5 languages
        return False
    else:
        return True
    
def extract_ingredients_text(comment):
    '''
    Truncates the recipe post to only include the ingredients, and not the instructions.

    Args:
        comment (str): the comment containing the recipe

    Returns:
        ingredients_text (str): the portion of the recipe containing the ingredients.

    Note: This function uses "INSTRUCTIONS", "DIRECTIONS", and "STEPS" as keywords to identify the start of the instructions, which are common delimiter words in the recipe comment. While it is not perfect, it is a good heuristic for most recipes as the main objective is to reduce the number of tokens to be processed by GPT-3.
    '''
    match = re.search(r'INSTRUCTIONS|DIRECTIONS|STEPS', comment, re.IGNORECASE)
    if match:
        ingredients_text = comment[:match.start()].strip()
        return ingredients_text
    else:
        return comment
    
def setup_gpt_client(credentials_path="../credentials.json"):
    '''
    Set up the OpenAI client using the credentials.json file. REQUIRES OPENAI API KEY. \n
    To include the OpenAI API key, the credentials.json file should have the following structure:
    {"openai_api_key: <your_api_key_here>"}
    '''
    # Open the file and load the data into a variable
    with open(credentials_path, "r") as f:
        credentials = json.load(f)

    client = OpenAI(api_key=credentials["openai_api_key"])
    return client

def get_ingredient_list(comment:str, client:OpenAI):
    '''
    Extracts the ingredients from a recipe using GPT-3.5-turbo
    
    Args: 
        comment (str): the comment containing the recipe
        client (OpenAI): the OpenAI client
        
    Returns:
        ingredient_list (list): a list of ingredients
    '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        seed=69,
        messages=[
            {
                "role": "system", "content": "You are a professional chef and food scientist.",
                "role": "user", "content": "In the following recipe, disregard the cooking instructions, identify the food items without the quantities and list them in a string with semicolon as the delimiter:\n" + comment
            },
        ],
    )
    ingredient_list = response.choices[0].message.content.split(";")

    # normalise all text to lower case
    ingredient_list = [ingredient.lower().strip() for ingredient in ingredient_list if ingredient != '']
    return ingredient_list

def get_cuisine(comment:str, client:OpenAI):
    '''
    Identifies the most likely cuisine from a recipe using GPT-3.5-turbo
    
    Args: 
        comment (str): the comment containing the recipe
        client (OpenAI): the OpenAI client
        
    Returns:
        cuisine (str): the most likely cuisine according to GPT
    '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        seed=69,
        messages=[
            {
                "role": "system", "content": "You are a professional chef and food reviewer.",
                "role": "user", "content": "Identify the 5 most likely cuisines that the following recipe belongs to. List your answers in a string with semicolon as the delimiter:\n" + comment
            },
        ]
    )
    cuisine_list = response.choices[0].message.content.split(";")

    # normalise all text to lower case
    cuisine_list = [cuisine.lower().strip() for cuisine in cuisine_list if cuisine != '']
    return cuisine_list[0]