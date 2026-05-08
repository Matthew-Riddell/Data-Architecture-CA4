#!/usr/bin/env python3
# transfer MongoDB products into PostgreSQL
# Matthew Riddell D00245674

from pymongo import MongoClient
import psycopg2
import configparser

# Load MongoDB config
config = configparser.ConfigParser()
config.read('mongodb.conf')

dbconfig = config['mongodb']

# Connect to MongoDB
mongo_client = MongoClient(
    dbconfig['host'],
    username=dbconfig['username'],
    password=dbconfig['password']
)

mongo_db = mongo_client[dbconfig['database']]
products_collection = mongo_db['products']


# Connect to PostgreSQL
pg_conn = psycopg2.connect(
    dbname='riddellm',
    user='riddellm'
)

pg_cur = pg_conn.cursor()

# Relational schema

pg_cur.execute("""

CREATE TABLE IF NOT EXISTS stores (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

""")

pg_cur.execute("""

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    product_id BIGINT,
    title TEXT,
    vendor TEXT,
    product_type TEXT,
    price NUMERIC
);

""")

pg_conn.commit()

# Transaction 

try:

    pg_conn.autocommit = False

    products = products_collection.find({})

    for product in products:

        store_name = product.get('store')

        # Insert store if not exists

        pg_cur.execute("""
            INSERT INTO stores (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        """, (store_name,))

        # Get store ID

        pg_cur.execute("""
            SELECT id FROM stores
            WHERE name = %s
        """, (store_name,))

        store_id = pg_cur.fetchone()[0]

        # Extract price

        price = None

        try:
            if product.get('variants'):
                price = float(
                    product['variants'][0]['price']
                )
        except:
            pass

        # Insert product

        pg_cur.execute("""

            INSERT INTO products (
                store_id,
                product_id,
                title,
                vendor,
                product_type,
                price
            )
            VALUES (%s, %s, %s, %s, %s, %s)

        """, (
            store_id,
            product.get('id'),
            product.get('title'),
            product.get('vendor'),
            product.get('product_type'),
            price
        ))

    # Commit transaction

    pg_conn.commit()

    print('Transfer completed successfully.')

except Exception as e:

    pg_conn.rollback()

    print('Transaction failed.')
    print(e)

finally:

    pg_cur.close()
    pg_conn.close()