# testing
from jsonschema import validate

test = {"href": "https://api.ebay.com/buy/browse/v1/item_summary/search?q=laptop&limit=1&filter=buyingOptions%3A%7BFIXED_PRICE%7D&offset=0", "total": 1933831, "next": "https://api.ebay.com/buy/browse/v1/item_summary/search?q=laptop&limit=1&filter=buyingOptions%3A%7BFIXED_PRICE%7D&offset=1", "limit": 1, "offset": 0, "itemSummaries": [{"itemId": "v1|326160310582|0", "title": "Samsung Chromebook XE350XBA-K05US 15.6' 1080p FHD Laptop Intel 4GB RAM 128GB SSD", "leafCategoryIds": ["177"], "categories": [{"categoryId": "177", "categoryName": "PC Laptops & Netbooks"}, {"categoryId": "58058", "categoryName": "Computers/Tablets & Networking"}, {"categoryId": "175672", "categoryName": "Laptops & Netbooks"}], "image": {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/GBsAAOSwAXVmaIaV/s-l225.jpg"}, "price": {"value": "349.00", "currency": "USD"}, "itemHref": "https://api.ebay.com/buy/browse/v1/item/v1%7C326160310582%7C0", "seller": {"username": "jcs_computer_store", "feedbackPercentage": "96.5", "feedbackScore": 45754}, "condition": "Used", "conditionId": "3000", "thumbnailImages": [{"imageUrl": "https://i.ebayimg.com/images/g/GBsAAOSwAXVmaIaV/s-l1600.jpg"}], "shippingOptions": [{"shippingCostType": "FIXED", "shippingCost": {"value": "0.00", "currency": "USD"}, "minEstimatedDeliveryDate": "2024-06-25T07:00:00.000Z", "maxEstimatedDeliveryDate": "2024-06-25T07:00:00.000Z", "guaranteedDelivery": True}], "buyingOptions": ["FIXED_PRICE"], "epid": "14043912572", "itemWebUrl": "https://www.ebay.com/itm/326160310582?hash=item4bf0ab6136:g:GBsAAOSwAXVmaIaV&amdata=enc%3AAQAJAAAA0CmKvRLb%2BDtiMhaIFIPA5WsqknBx3ouaDDMK%2BzBnVBgxAuKi8aFTBJ34kmfoejIJcVff0MDS8wio%2FylvQCZpxCo4XE6%2FIRoCFevHc8s87RnIKVT%2FXrpmM02itxAwEuYOf%2FFws3VH%2BBdbRTP%2FEFIk5UwFdg4bpit%2BvPhjrEQdZfdthVqtbwZOCeR4VB99xDrufDzW5T%2F9rzah2wQO3rD%2FKIzmogPFLb93CFn9Ba1gXQKlXClJxryHv4QgeiabOLNhgY31xXf8ZcYdqMrwnywLxlA%3D", "itemLocation": {"postalCode": "146**", "country": "US"}, "additionalImages": [{"imageUrl": "https://i.ebayimg.com/thumbs/images/g/V48AAOSw3epmaIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/C1UAAOSwSFRmaIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/b8MAAOSwMFxmaIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/NOUAAOSwDTJmaIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/UwUAAOSwtO5maIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/OC0AAOSwUGpmaIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/Hf4AAOSwJ-5maIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/cj0AAOSwYD5maIaV/s-l225.jpg"}, {"imageUrl": "https://i.ebayimg.com/thumbs/images/g/6~oAAOSwJAdmaIaV/s-l225.jpg"}], "adultOnly": False, "legacyItemId": "326160310582", "availableCoupons": False, "itemCreationDate": "2024-06-12T09:21:31.000Z", "topRatedBuyingExperience": False, "priorityListing": True, "listingMarketplaceId": "EBAY_US"}]}



def transverse_json_data(data, result=None, parent_key =""):
    items_dict = {}
    if result is None:
        result = {}
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            transverse_json_data(value, result, parent_key=full_key)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            full_key = f"{parent_key}[{index}]"
            transverse_json_data(item, result, parent_key=full_key)
    else:
        result[parent_key] = data
    return result

item_list = []
item_list.append(transverse_json_data(test))

# for each item retuened add it to the list then loop through all items which each item should be a dict

def data_by_item_id(data):
    items_by_id ={}
    i = 0
    for item in item_list:
        # print(type(item))
        item_id = item.get(f"itemSummaries[{i}].itemId")
        items_by_id[item_id] = item
        i += 1
    return items_by_id

# temp = transverse_json_data(item_list)

# temp2 = data_by_item_id(item_list)
# print(temp2)