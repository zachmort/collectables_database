import requests
import pandas as pd
import pprint
import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from ebaysdk.merchandising import Connection as merchandising
import ebaysdk
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os



# get_ebay_api_call -> returns item id (list of item ids?) -> use item id as arg for bidding to see history of item prices etc (only need aggregate of sales data not how they trnded over time of auction)

##### output from item_summary/search
# TODO:
# Learn how to cache this data in browser/django
# need to grab "next" value 'next': 'https://api.ebay.com/buy/browse/v1/item_summary/search?q=laptop&limit=50&filter=buyingOptions%3A%7BFIXED_PRICE%7D&offset=50'
# what is leafCategoryIds?
# itemsummaries [index#]-> categories/image/price/itemHref/buyingOptions/itemWebUrl/itemLocation/condition/thumbnailImages
# itemsummaries -> condition?
# -> multiple categoryId s



##### output from sold history

SANDBOX_CLIENT_SECRET = os.getenv("sandbox_client_secret")
SANDBOX_CLIENT_ID = os.getenv("sandbox_client_id")






#TODO: use only browse api and store data every hours via postgres DB?
# grouped on the item id? Unique key for each? Check termina output


def get_ebay_api_call():
    session = requests.Session()
    headers = {
        "Authorization": ""
        , "content-Type": ""
        , "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
    }
    # response = requests.get("https://api.ebay.com/buy/browse/v1/item_summary/search?q=drone&limit=3")

    # Replace with your App ID (Client ID) and Cert ID (Client Secret)
    CLIENT_ID = SANDBOX_CLIENT_ID
    CLIENT_SECRET = SANDBOX_CLIENT_SECRET

    # Endpoint for getting OAuth token
    OAUTH_URL = 'https://api.ebay.com/identity/v1/oauth2/token'

    # Define the headers and data for the token request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'client_credentials',
        'scope': 'https://api.ebay.com/oauth/api_scope'
    }

    # Request the token
    response = requests.post(OAUTH_URL, headers=headers, data=data, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
    response.raise_for_status()

    # Extract the access token
    access_token = response.json()['access_token']

    # Base URL for eBay Browse API
    EBAY_API_URL = 'https://api.ebay.com/buy/browse/v1/item_summary/search'

    # Your query parameters (e.g., search keyword)
    params = {
        'q': 'NBA Cards',
        # "filter": "buyingOptions%3A%7BFIXED_PRICE%7D",
        'limit': 1
    }
    # 'condition': 'Graded', "New", "Used", "Ungraded"
    # [{'categoryId': '261328', 'categoryName': 'Trading Card Singles'}, {'categoryId': '64482', 'categoryName': 'Sports Mem, Cards & Fan Shop'}, {'categoryId': '212', 'categoryName': 'Sports Trading Cards'}],
    params2 = {
        'q': 'laptop',
        "filter": "buyingOptions%3A%7BAUCTION%7D",
        'limit': 1
    }



    # Define headers including the Authorization header
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US'  # Replace with your eBay marketplace
    }

    # Make the API request
    response = requests.get(EBAY_API_URL, headers=headers, params=params)
    response.raise_for_status()

    # Print the response
    return print(response.json())
    
# print("get items call")
# get_ebay_api_call()



### TODO: get items bidding history?
def get_item_auction_info(item_id):
    try:
        session = requests.Session()
        headers = {
            "Authorization": ""
            , "content-Type": ""
            , "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
        }
        # response = requests.get("https://api.ebay.com/buy/browse/v1/item_summary/search?q=drone&limit=3")

        # Replace with your App ID (Client ID) and Cert ID (Client Secret)
        CLIENT_ID = keys.client_id
        CLIENT_SECRET = keys.client_secret

        # Endpoint for getting OAuth token
        OAUTH_URL = 'https://api.ebay.com/identity/v1/oauth2/token'

        # Define the headers and data for the token request
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'client_credentials',
            'scope': 'https://api.ebay.com/oauth/api_scope'
        }
            # Request the token
        response = requests.post(OAUTH_URL, headers=headers, data=data, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
        response.raise_for_status()

        # Extract the access token
        access_token = response.json()['access_token']

        # Base URL for eBay Browse API
        EBAY_API_URL = 'https://api.ebay.com/buy/offer/v1_beta/bidding'

        # Your query parameters (e.g., search keyword)
        params = {
            'q': 'Anythony Edwards',
            'limit': 5
        }

        # Define headers including the Authorization header
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US'  # Replace with your eBay marketplace
        }

        # Make the API request
        response = requests.get(EBAY_API_URL, headers=headers, params=params)
        response.raise_for_status()

        # Print the response
        return print(response.json())
    
    except:
        print("this item does not have an auction")

#### TODO: Need to apply for use of item sales API
# https://developer.ebay.com/api-docs/buy/marketplace-insights/resources/item_sales/methods/search#s0-1-22-6-7-7-6-GetItemSalesHistoryusingSearch-0
## Requirements: https://developer.ebay.com/api-docs/buy/static/buy-requirements.html#Applying

def get_sold_item_data():
    # Replace with your App ID (Client ID) and Cert ID (Client Secret)
    CLIENT_ID = SANDBOX_CLIENT_ID
    CLIENT_SECRET = SANDBOX_CLIENT_SECRET

    # Endpoint for getting OAuth token
    OAUTH_URL = 'https://api.sandbox.ebay.com/identity/v1/oauth2/token'  # Use sandbox endpoint

    # Define the headers and data for the token request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'client_credentials',
        'scope': 'https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/buy.marketplace.insights'
    }

    # Request the token
    try:
        response = requests.post(OAUTH_URL, headers=headers, data=data, auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET))
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Error getting access token: {err}")
        print(f"Response content: {response.content}")
        return

    # Extract the access token
    access_token = response.json().get('access_token')
    if not access_token:
        print("Failed to obtain access token")
        return

    # Base URL for eBay Marketplace Insights API
    EBAY_API_URL = 'https://api.sandbox.ebay.com/buy/marketplace_insights/v1_beta/item_sales/search'

    # Your query parameters (e.g., search keyword)
    params = {
        'q': 'NBA Cards',
        # 'condition': ["Graded", "New", "Used", "Ungraded"], 
        # 'leafCategoryIds': ["261328"],
        'limit': 1,
    }

    # Define headers including the Authorization header
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US'  # Use the appropriate marketplace ID
    }

    # Make the API request
    try:
        response = requests.get(EBAY_API_URL, headers=headers, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Error making API request: {err}")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        return

    # Print the response
    return print(response.json())

# Call the function to test it
get_sold_item_data()

    

# def get_collx_api_call():
#     pass

# def web_scrape_beckett_wesite():
#     pass

# def get_item_info():
#     pass

# def compare_site_info():
#     pass
