import os
import json
from pymongo import MongoClient
from random import choice
from dotenv import load_dotenv
import requests

# Load environment variables (for MongoDB URI)
load_dotenv()

# Get MongoDB URI from environment variable
mongodb_uri = os.getenv('mongoDB.uri')

if not mongodb_uri:
    raise ValueError("MongoDB URI is not set in the environment variable")

# Connect to MongoDB
client = MongoClient(mongodb_uri)
db = client['client_info']  # Database name
collection = db['enquiry_details']  # Collection name for enquiries

status = ["Active", "Not Active", "Converted"]

# Define the folder paths
input_folder = "./transcripts"
output_folder = "./transcripts_enquiry"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Iterate through all files in the input folder
for filename in os.listdir(input_folder):
    input_path = os.path.join(input_folder, filename)
    
    # Check if the file is a JSON file
    if os.path.isfile(input_path) and filename.endswith(".json"):
        with open(input_path, "r") as file:
            try:
                # Load the file data as a dictionary
                file_data = json.load(file)
                
                stat = choice(status)

                # Extract the required fields for enquiry
                user_info_payload= {
                "user_info" :{
                    "name": file_data["user_info"]["name"],
                    "contact": file_data["user_info"]["contact"],
                    "date": file_data["user_info"]["date"],
                    "interested_model": file_data["user_info"]["interested_model"],
                    "location": file_data["user_info"]["location"],
                    "status": stat
                }}

                # Save the enquiry details to a new JSON file in the output folder
                output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_enquiry.json")
                with open(output_file_path, "w") as output_file:
                    json.dump(user_info_payload, output_file, indent=4)
                
                # Insert the enquiry details into MongoDB
                # collection.insert_one(enquiry_details)
                
                url = "http://localhost:3000/api/end_conversation"

                response = requests.post(url, json=user_info_payload)

                if response.status_code == 201:
                    print("Data successfully sent to API.")
                else:
                    print(f"Failed to send data. Status code: {response.status_code}")


                print(f"Processed, saved to file, and added to MongoDB: {filename}")
            except (KeyError, json.JSONDecodeError) as e:
                print(f"Error processing {filename}: {e}")