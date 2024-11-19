from connect_postgres import insert_data_to_db
# from ebay_api_calls import get_sold_item_data
# from ebay_api_calls import get_ebay_api_call

def main():
    """
    Main function to fetch data from eBay API and insert it into the PostgreSQL database.
    """
    # Database connection parameters
    connection_params = {
        'dbname': 'Cards',
        'user': 'zachmortenson',
        'password': 'xxxx',
        'host': 'localhost',
        'port': '5432'
    }

    # Fetch data from the eBay API
    # api_data = get_ebay_api_call()
    api_data = True

    # If data is successfully fetched, insert it into the database
    if api_data:
        insert_data_to_db(connection_params, api_data)
    else:
        print("No data fetched from the API.")

if __name__ == "__main__":
    main()
