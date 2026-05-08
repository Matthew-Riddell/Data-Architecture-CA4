#!/usr/bin/env python3
# Load shopify product JSON to MongoDB
# Matthew Riddell D00245674

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import requests
import configparser

print('Loading information from stores...')

# Load config from mongodb.conf
config = configparser.ConfigParser()
config.read('mongodb.conf')
dbconfig = config['mongodb']

# Connect to MongoDB
client = MongoClient(
    dbconfig['host'],
    username=dbconfig['username'],
    password=dbconfig['password']
)

db = client[dbconfig['database']]

stores_collection = db['stores']
products_collection = db['products']

# Create UNIQUE compound index
# Prevent duplicates
products_collection.create_index(
    [('store', 1), ('handle', 1)],
    unique=True
)

# Loop through stores
stores = stores_collection.find({})

for store in stores:

    print(f"\nFetching products from: {store['name']}")

    page = 1

    while True:

        url = store['url'] + '/products.json'

        params = {
            'limit': 250,
            'page': page
        }

        try:

            response = requests.get(url, params=params)

            # stop if request failed
            if response.status_code != 200:
                print(f"Failed request: {response.status_code}")
                break

            data = response.json()

            products = data.get('products', [])

            # no more products
            if not products:
                break

            # Process each product
            for product in products:

                # inject store name
                product['store'] = store['name']

                # generate reference
                product['ref'] = f"{store['name']}/{product['id']}"

                print(product['title'])

                # insert into MongoDB
                try:
                    products_collection.insert_one(product)
                    print('Inserted')

                except DuplicateKeyError:
                    print('Duplicate item ignored')

            page += 1

        except Exception as e:
            print(f"Error: {e}")
            break

print('\nFinished loading products.')