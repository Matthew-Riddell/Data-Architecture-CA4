#!/usr/bin/env python3
# XML report generation
# Matthew Riddell D00245674

from pymongo import MongoClient
import configparser
import xml.etree.ElementTree as ET

# Load MongoDB config
config = configparser.ConfigParser()
config.read("mongodb.conf")

dbconfig = config["mongodb"]

client = MongoClient(
    dbconfig["host"],
    username=dbconfig["username"],
    password=dbconfig["password"]
)

db = client[dbconfig["database"]]
products = db["products"]

# Aggregation product count
pipeline = [
    {
        "$group": {
            "_id": "$store",
            "count": {"$sum": 1},
            "avg_price": {
                "$avg": {
                    "$toDouble": "$variants.price"
                }
            }
        }
    }
]

results = list(products.aggregate([
    {
        "$unwind": "$variants"
    },
    {
        "$group": {
            "_id": "$store",
            "count": {"$sum": 1},
            "avg_price": {
                "$avg": {
                    "$toDouble": "$variants.price"
                }
            }
        }
    }
]))

# Build XML
root = ET.Element("stores")

for r in results:

    store = ET.SubElement(root, "store")
    store.set("name", r["_id"])

    count = ET.SubElement(store, "product_count")
    count.text = str(r["count"])

    avg = ET.SubElement(store, "average_price")
    avg.text = str(round(r["avg_price"], 2))

# Write XML file
tree = ET.ElementTree(root)
tree.write("store_report.xml", encoding="utf-8", xml_declaration=True)

print("XML report generated successfully.")