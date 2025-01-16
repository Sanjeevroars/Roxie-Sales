from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("mongoDB.uri")

# Ensure the URI is provided
if not uri:
    raise ValueError("MongoDB URI is not set in the environment variables.")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), connectTimeoutMS=60000, socketTimeoutMS=60000)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. Successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)

# Select the database and collection
db = client["client_info"]
model_list = db["client_models"]

# Sample data for car models and their variants
model_data = [
    {
        "model": "Toyota Corolla",
        "aliases": ["Corolla"],
        "category": ["Sedan"],
        "variants": [
            {"name": "L", "price": "1500000"},
            {"name": "LE", "price": "1550000"},
            {"name": "XLE", "price": "1800000"},
        ]
    },
    {
        "model": "Toyota Camry",
        "aliases": ["Camry"],
        "category": ["Sedan"],
        "variants": [
            {"name": "LE", "price": "4525000"},
            {"name": "SE", "price": "4600000"},
            {"name": "XSE", "price": "5000000"},
        ]
    },
    {
        "model": "Toyota RAV4",
        "aliases": ["RAV4"],
        "category": ["SUV"],
        "variants": [
            {"name": "LE", "price": "3000000"},
            {"name": "XLE", "price": "3150000"},
            {"name": "ADVENTURE", "price": "3500000"},
        ]
    },
    {
        "model": "Toyota Prius",
        "aliases": ["Prius"],
        "category": ["Hatchback"],
        "variants": [
            {"name": "L Eco", "price": "2500000"},
            {"name": "LE", "price": "2600000"},
            {"name": "XLE", "price": "2750000"},
        ]
    }
]

# Insert car data into the collection
try:
    result = model_list.insert_many(model_data, ordered=False)  # Prevent halting on duplicate errors
    print(f"Inserted {len(result.inserted_ids)} car models into MongoDB successfully.")
except Exception as e:
    print(f"Error inserting data into MongoDB: {e}")
