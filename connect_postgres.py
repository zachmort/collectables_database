import psycopg2
from psycopg2 import sql
from psycopg2 import extras
from dotenv import load_dotenv
import os
from parse_api_data import transverse_json_data
from parse_api_data import data_by_item_id
from typing import Any


load_dotenv()
dbname: str | None = os.getenv("dbname")
user: str | None = os.getenv("user")
password: str | None = os.getenv("password")
host: str | None = os.getenv("host")
port: str | None = os.getenv("port")
connection_params: dict[str, str | None] = {
                  'dbname': dbname 
                , 'user': user 
                , 'password': password 
                , 'host': host 
                , 'port': port}

# Connect to the PostgreSQL database
connection: psycopg2.connection = psycopg2.connect(**connection_params)
print("cursor connection", connection.closed)
cursor = connection.cursor()

# Define the table and columns
# catalog_name = 'Cards'
schema_name: str = 'cards_schema'
table_name: str = 'example_table'
project_name: str = 'Cards'

test: dict[str, Any] = {"href": "https://api.ebay.com/buy/browse/v1/item_summary/search?q=laptop&limit=1&filter=buyingOptions%3A%7BFIXED_PRICE%7D&offset=0", "total": 1933831, "next": "https://api.ebay.com/buy/browse/v1/item_summary/search?q=laptop&limit=1&filter=buyingOptions%3A%7BFIXED_PRICE%7D&offset=1", "limit": 1, "offset": 0, "itemSummaries": [{"itemId": "v1|326160310582|0", "title": "Samsung Chromebook XE350XBA-K05US 15.6' 1080p FHD Laptop Intel 4GB RAM 128GB SSD", "leafCategoryIds": ["177"], "categories": [{"categoryId": "177", "categoryName": "PC Laptops & Netbooks"}, {"categoryId": "58058", "categoryName": "Computers/Tablets & Networking"}, {"categoryId": "175672", "categoryName": "Laptops & Netbooks"}], "image": {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/GBsAAOSwAXVmaIaV/s-l225.jpg"}, "price": {"value": "349.00", "currency": "USD"}, "itemHref": "https://api.ebay.com/buy/browse/v1/item/v1%7C326160310582%7C0", "seller": {"username": "jcs_computer_store", "feedbackPercentage": "96.5", "feedbackScore": 45754}, "condition": "Used", "conditionId": "3000", "thumbnailImages": [{"imageUrl": "https://i.ebayimg.com/images/g/GBsAAOSwAXVmaIaV/s-l1600.jpg"}], "shippingOptions": [{"shippingCostType": "FIXED", "shippingCost": {"value": "0.00", "currency": "USD"}, "minEstimatedDeliveryDate": "2024-06-25T07:00:00.000Z", "maxEstimatedDeliveryDate": "2024-06-25T07:00:00.000Z", "guaranteedDelivery": True}], "buyingOptions": ["FIXED_PRICE"], "epid": "14043912572", "itemWebUrl": "https://www.ebay.com/itm/326160310582?hash=item4bf0ab6136:g:GBsAAOSwAXVmaIaV&amdata=enc%3AAQAJAAAA0CmKvRLb%2BDtiMhaIFIPA5WsqknBx3ouaDDMK%2BzBnVBgxAuKi8aFTBJ34kmfoejIJcVff0MDS8wio%2FylvQCZpxCo4XE6%2FIRoCFevHc8s87RnIKVT%2FXrpmM02itxAwEuYOf%2FFws3VH%2BBdbRTP%2FEFIk5UwFdg4bpit%2BvPhjrEQdZfdthVqtbwZOCeR4VB99xDrufDzW5T%2F9rzah2wQO3rD%2FKIzmogPFLb93CFn9Ba1gXQKlXClJxryHv4QgeiabOLNhgY31xXf8ZcYdqMrwnywLxlA%3D", "itemLocation": {"postalCode": "146**", "country": "US"}, "additionalImages": [{"imageUrl": "https://i.ebayimg.com/thumbs/images/g/V48AAOSw3epmaIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/C1UAAOSwSFRmaIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/b8MAAOSwMFxmaIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/NOUAAOSwDTJmaIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/UwUAAOSwtO5maIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/OC0AAOSwUGpmaIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/Hf4AAOSwJ-5maIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/cj0AAOSwYD5maIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/6~oAAOSwJAdmaIaV/s-l225.jpg"}], "adultOnly": False, "legacyItemId": "326160310582", "availableCoupons": False, "itemCreationDate": "2024-06-12T09:21:31.000Z", "topRatedBuyingExperience": False, "priorityListing": True, "listingMarketplaceId": "EBAY_US"}]}


def check_table_exits() -> bool:
    table_check = sql.SQL(f"""SELECT EXISTS (SELECT * FROM information_schema.tables WHERE table_schema = '{schema_name}' AND table_name = '{table_name}')""")
    cursor.execute(table_check)
    table_exists: bool = cursor.fetchone()[0]
    return table_exists



def table_exist_schema_validation():
    #####this will proabbly be slow chekcing in SQL try a shema validation package
    ### Check if table exists
    if check_table_exits() == True:
        schema_check: sql.SQL = sql.SQL(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns
                WHERE table_schema = '{schema_name}'
                AND table_name = '{table_name}'
                                    """)
        
        cursor.execute(schema_check)
        table_schema: list[tuple] = cursor.fetchall()
        
        table_schema_validation_column_name: bool = table_schema[0][0] == 'itemId'
        table_schema_validation_column_type: bool = table_schema[0][1] == "character varying"
        print(table_schema)
        print(f"name_check: {table_schema_validation_column_name}", table_schema_validation_column_type)
        print(test := not table_schema_validation_column_name and not table_schema_validation_column_type)
        
        if not table_schema_validation_column_name or not table_schema_validation_column_type:
            try:
                print("Table had incorrect schema type attempting to recreate")
                drop_table: sql.SQL = sql.SQL(f"""DROP TABLE {schema_name}.{table_name}""")
                cursor.execute(drop_table)
                print("table dropped checking schema again")
                table_exist_schema_validation()
                return True
            except Exception as e:
                print("table could not be dropped")
                print(e)
                return False
        else:
            return True

    else:
        try:
            create_table: sql.SQL = sql.SQL(f"""
                    CREATE TABLE {schema_name}.{table_name} (
                            itemId VARCHAR PRIMARY KEY
                            , jsonString VARCHAR
                            )               """)
            cursor.execute(create_table)
            print("Table did not exist, created table")
            return True
        except Exception as e:
            print(e)
            return False

def get_api_data():
    pass

def insert_data_to_db(connection_params, *input_string):
    """
    Inserts a string into the 'example_table' table in the PostgreSQL database.

    Parameters:
    - connection_params (dict): A dictionary containing the connection parameters.
                                Example: {
                                    'dbname': 'your_db',
                                    'user': 'your_user',
                                    'password': 'your_password',
                                    'host': 'localhost',
                                    'port': '5432'
                                }
    - input_string (str): The string data to be inserted into the database.
    """

    columns: list[str] = ['itemId', 'jsonData']
    temp: list[Any | None] = []
    items: dict[Any, Any] = transverse_json_data(test)
    temp.append(items)
    items_pairs = data_by_item_id(items)
    
    data_list: list[Any] = []
    for i in items_pairs:
        for key, value in data_by_item_id(items_pairs).items():
            record: dict[str, str] = {'itemId': f'{key}','jsonData': f'{value}',}
            data_list.append(record)

    # Convert the list of dictionaries into a list of tuples (corresponding to each row)
    values: list[tuple[Any, ...]] = [tuple(item[col] for col in columns) for item in data_list]


    # Prepare the SQL query
    insert_data_query = sql.SQL("INSERT INTO {} ({}) VALUES %s").format(
                                    sql.SQL('.').join([
                                        sql.Identifier(schema_name),
                                        sql.Identifier(table_name)
                                        ]),
                                    sql.SQL(',').join(map(sql.Identifier, columns))
                                    )

    try:
        data: None = None
        ### create temp table and insert the data of the new rows here
        ## Temp table created for data pulled in by API call
        create_temp_table = sql.SQL(f"""
                                            CREATE TEMP TABLE temp_{table_name} AS
                                            SELECT 
                                        """)
        ### take tmp table and merge it into base table
        ### join on product id
        ### check that the recieved/updated time is greater than the base updated time 
        merge_temp_table = None


        if table_exist_schema_validation() == True:
        # if table_check and table_schema_validation:
            try:
                # Execute the batch insert
                # extras.execute_values(cursor, insert_data_query, values)
                # Commit the transaction
                connection.commit()
            except Exception as error:
                print(f"table check error {error}")
        else:
            # cursor.execute(drop_table_query)
            # cursor.execute(create_table_query)
            # Commit the transaction
            connection.commit()

        # Define the SQL query with placeholders
        # query = sql.SQL("INSERT INTO cards_schema.example_table (data_column) VALUES (%s)")

        # Execute the query with the provided string
        # cursor.execute(query, (data_list,))

        # Commit the transaction
        connection.commit()
        print("Data successfully inserted")

    except Exception as error:
        print(f"Error inserting data: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            # print(f"data {example_string} inserted")

# print(connection_params)
insert_data_to_db(connection_params=connection_params)
# Fetch data from the API
# data = fetch_api_data(api_url)


# Insert the fetched data into the PostgreSQL database
# if data:
    # insert_data_to_db(connection_params, data)


table_exist_schema_validation()
# print(test)
