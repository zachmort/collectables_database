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
import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed



# get_ebay_api_call -> returns item id (list of item ids?) -> use item id as arg for bidding to see history of item prices etc (only need aggregate of sales data not how they trnded over time of auction)

##### output from item_summary/search
# TODO:
# Learn how to cache this data in browser/django
# need to grab "next" value 'next': 'https://api.ebay.com/buy/browse/v1/item_summary/search?q=laptop&limit=50&filter=buyingOptions%3A%7BFIXED_PRICE%7D&offset=50'
# what is leafCategoryIds?
# itemsummaries [index#]-> categories/image/price/itemHref/buyingOptions/itemWebUrl/itemLocation/condition/thumbnailImages
# itemsummaries -> condition?
# -> multiple categoryId s

load_dotenv()
SANDBOX_CLIENT_SECRET = os.getenv("sandbox_client_secret")
SANDBOX_CLIENT_ID = os.getenv("sandbox_client_id")
PROD_CLIENT_SECRET = os.getenv("client_secret")
PROD_CLIENT_ID = os.getenv("client_id")

def fetch_results(offset, limit, headers):
    EBAY_API_URL = 'https://api.ebay.com/buy/browse/v1/item_summary/search'
    params = {
        'q': 'NBA Cards',   # Example query, adjust as needed
        'limit': limit,
        'offset': offset
    }
    response = requests.get(EBAY_API_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_ebay_api_call():
    headers = {
        "Authorization": ""
        , "content-Type": ""
        , "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
    }
    # response = requests.get("https://api.ebay.com/buy/browse/v1/item_summary/search?q=drone&limit=3")

    # Replace with your App ID (Client ID) and Cert ID (Client Secret)
    # CLIENT_ID = SANDBOX_CLIENT_ID
    # CLIENT_SECRET = SANDBOX_CLIENT_SECRET
    CLIENT_ID = PROD_CLIENT_ID
    CLIENT_SECRET = PROD_CLIENT_SECRET

    # Endpoint for getting OAuth token
    # OAUTH_URL = 'https://api.sandbox.ebay.com/identity/v1/oauth2/token'
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
    # EBAY_API_URL = 'https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search'
    EBAY_API_URL = 'https://api.ebay.com/buy/browse/v1/item_summary/search'

    # Define headers including the Authorization header
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US'  # Replace with your eBay marketplace
    }

        # Define the different offsets/limits to fetch in parallel
    calls = [
        {'offset': 0, 'limit': 50},
        {'offset': 50, 'limit': 50},
        {'offset': 100, 'limit': 50}
    ]

    results = []
    # Use ThreadPoolExecutor to fetch all results in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_call = {executor.submit(fetch_results, c['offset'], c['limit'], headers): c for c in calls}
        for future in as_completed(future_to_call):
            result_data = future.result()
            results.append(result_data)

    # Print or process all results combined
    for i, result in enumerate(results, start=1):
        print(f"Result set {i}:", result)

if __name__ == "__main__":
    get_ebay_api_call()



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

def get_sold_item_data():
    # Replace with your App ID (Client ID) and Cert ID (Client Secret)
    # CLIENT_ID = SANDBOX_CLIENT_ID
    # CLIENT_SECRET = SANDBOX_CLIENT_SECRET
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
    return print("get sold item data", response.json())

def get_collx_api_call():
    pass

def web_scrape_beckett_wesite():
    pass

def get_item_info():
    pass

def compare_site_info():
    pass
