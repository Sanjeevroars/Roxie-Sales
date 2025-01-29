import json
from random import choices, randint
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Function to generate a skewed random base date (biased towards recent dates)
def random_base_date():
    # Use a biased distribution with more preference for recent dates (last 3 months)
    random_days = randint(-400, 0)  # More recent dates, within the last 60 days
    return datetime.now() + timedelta(days=random_days)

# Function to generate a skewed random time (biased towards recent and quicker interactions)
def random_time(base_time):
    # Skew time by adding random seconds (most interactions happen in less than 5 minutes)
    random_seconds = randint(1, 300)  # 5-minute spread, this helps clustering
    return base_time + timedelta(seconds=random_seconds)

# List of locations with biased weights (e.g., Mumbai more likely to be chosen)
locations = [
    "Mumbai, India", 
    "Kolkata, India", 
    "Hyderabad, India", 
    "Delhi, India", 
    "Bangalore, India", 
    "Chennai, India", 
    "Pune, India", 
    "Ahmedabad, India", 
    "Surat, India", 
    "Jaipur, India"
]

# Adjusted weights for locations (Mumbai has the highest weight)
location_weights = [7, 4, 6, 3, 5, 10, 3, 2, 2, 1]  # Mumbai, Delhi, and Bangalore favored

# List of models with biased weights (e.g., Toyota Prius more common)
models = ["Toyota Prius", "Toyota Corolla", "Toyota Camry", "Toyota RAV4"]

# Adjusted weights for models (Toyota Prius is more likely)
model_weights = [5, 3, 8, 2]  # Prius has more selection weight

# List of names with biased weights (more common names favored)
names = [
    "Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Peyton", "Sydney", "Cameron", "Quinn", 
    "Avery", "Dakota", "Emerson", "Finley", "Harper", "Rowan", "Skylar", "Spencer", "Logan", "Sawyer", 
    "Elliot", "Carter", "Charlie", "Parker", "Hunter", "Jesse", "Phoenix", "Kai", "Reagan", "Dakota", 
    "Madison", "Cade", "Jaden", "River", "Maddox", "Zane", "Ellis", "Blake", "Asher", "Cooper", 
    "Blaise", "Kendall", "Aidan", "Nolan", "Remy", "Wren", "Toby", "Tate", "Aubrey", "Everett"
]

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from the environment variables
mongodb_uri = os.getenv('mongoDB.uri')

# Check if MongoDB URI is available
if not mongodb_uri:
    raise ValueError("MongoDB URI is missing from environment variables. Please ensure it's set in your .env file.")

# MongoDB Setup
try:
    client = MongoClient(mongodb_uri)  # Connect to MongoDB using the URI
    db = client["client_info"]
    collection = db["transcript_details"]
    print("Connected to MongoDB successfully.")
except Exception as e:
    raise ConnectionError(f"Failed to connect to MongoDB: {e}")

# Generate files and send to MongoDB
for i in range(2000):
    name = choices(names)
    location = choices(locations, weights=location_weights, k=1)[0]  # Weighted selection for locations
    model = choices(models, weights=model_weights, k=1)[0]  # Weighted selection for models
    
    base_time = random_base_date()  # Skewed random base date
    time = random_time(base_time).strftime("%Y-%m-%dT%H:%M:%S")  # Skewed random time
    contact = f"{randint(6000000000, 9999999999)}"

    # Create the JSON structure
    file_content = {
        "user_info": {
            "name": name,
            "contact": contact,
            "date": time,
            "interested_model": model,
            "location": location
        },
        "transcript": [
            f"User: {name}",
            f"My contact number is {contact}",
            f"Assistant: Great choice! The {model} is available in our collection.",
            f"User is interested in: {model}",
            f"Assistant: You are interested in -> {model}",
            f"Booking appointment for {name} @ {location}.",
            "Assistant: Our Sales team will contact you shortly. Have a great day!"
        ]
    }

    # Save the entry to MongoDB
    result = collection.insert_one(file_content)

    # Remove the _id field for local saving
    file_content_no_id = file_content.copy()
    file_content_no_id.pop("_id", None)  # Remove the _id if it exists

    # Optionally save to a local JSON file (without _id)
    filename = f"./transcripts/user_data_{i + 1}.json"
    with open(filename, "w") as f:
        json.dump(file_content_no_id, f, indent=4)

# Output the filenames created (if you're also saving locally)
filenames = [f"user_data_{i + 1}.json" for i in range(20)]
print(filenames)