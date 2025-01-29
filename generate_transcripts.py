import json
from random import choices, randint, choice
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
import requests
import os

# Function to generate a skewed random base date (biased towards recent dates)
def random_base_date():
    random_days = randint(-400, 0)  # More recent dates, within the last 60 days
    return datetime.now() + timedelta(days=random_days)

# Function to generate a skewed random time (biased towards recent and quicker interactions)
def random_time(base_time):
    random_seconds = randint(1, 300)  # 5-minute spread
    return base_time + timedelta(seconds=random_seconds)

# List of locations with biased weights
locations = [
    "Mumbai, India", "Kolkata, India", "Hyderabad, India", "Delhi, India", "Bangalore, India", 
    "Chennai, India", "Pune, India", "Ahmedabad, India", "Surat, India", "Jaipur, India"
]
location_weights = [7, 4, 6, 3, 5, 10, 3, 2, 2, 1]

# List of models with biased weights
models = ["Toyota Prius", "Toyota Corolla", "Toyota Camry", "Toyota RAV4"]
model_weights = [5, 3, 8, 2]

# List of names with biased weights
names = [
    "Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Peyton", "Sydney", "Cameron", "Quinn", 
    "Avery", "Dakota", "Emerson", "Finley", "Harper", "Rowan", "Skylar", "Spencer", "Logan", "Sawyer", 
    "Elliot", "Carter", "Charlie", "Parker", "Hunter", "Jesse", "Phoenix", "Kai", "Reagan", "Dakota", 
    "Madison", "Cade", "Jaden", "River", "Maddox", "Zane", "Ellis", "Blake", "Asher", "Cooper", 
    "Blaise", "Kendall", "Aidan", "Nolan", "Remy", "Wren", "Toby", "Tate", "Aubrey", "Everett"
]

# Load environment variables
load_dotenv()
mongodb_uri = os.getenv('mongoDB.uri')

if not mongodb_uri:
    raise ValueError("MongoDB URI is missing from environment variables.")

# MongoDB Setup
try:
    client = MongoClient(mongodb_uri)
    db = client["client_info"]
    collection = db["transcript_details"]
    print("Connected to MongoDB successfully.")
except Exception as e:
    raise ConnectionError(f"Failed to connect to MongoDB: {e}")

# List to keep track of timestamps for calculating the moving average
timestamps = []
moving_average_window = 10  # Number of most recent entries to consider in the moving average

# Function to calculate moving average (based on time difference between enquiries)
def calculate_moving_average(timestamps):
    if len(timestamps) < 2:
        return 0  # Not enough data to calculate
    time_differences = []
    for i in range(1, len(timestamps)):
        time_diff = (timestamps[i] - timestamps[i - 1]).total_seconds() / 60  # Difference in minutes
        time_differences.append(time_diff)
    
    average_time_diff = sum(time_differences) / len(time_differences)
    enquiries_per_minute = 1 / average_time_diff if average_time_diff > 0 else 0
    return enquiries_per_minute

status = ["Active", "Not Active", "Converted"]

# Generate files and send to MongoDB
for i in range(1499):
    name = choices(names)[0]
    location = choices(locations, weights=location_weights, k=1)[0]
    model = choices(models, weights=model_weights, k=1)[0]
    
    base_time = random_base_date()
    time = random_time(base_time).strftime("%Y-%m-%dT%H:%M:%S")
    contact = f"{randint(6000000000, 9999999999)}"

    # Update the timestamps list with the current interaction time
    timestamps.append(datetime.strptime(time, "%Y-%m-%dT%H:%M:%S"))
    
    # Keep the list length within the moving average window
    if len(timestamps) > moving_average_window:
        timestamps.pop(0)

    stat = choice(status)


    # Calculate the current moving average of enquiries per minute
    moving_avg = calculate_moving_average(timestamps)
    
    # Create the JSON structure with moving average in the transcript
    user_info_payload = {
        "user_info": {
            "name": name,
            "contact": contact,
            "date": time,
            "interested_model": model,
            "location": location,
            "status": stat
        },
        "transcript": [
            f"User: {name}",
            f"My contact number is {contact}",
            f"Assistant: Great choice! The {model} is available in our collection.",
            f"User is interested in: {model}",
            f"Assistant: You are interested in -> {model}",
            f"Booking appointment for {name} @ {location}.",
            "Assistant: Our Sales team will contact you shortly. Have a great day!",
            f"Assistant: Current moving average of enquiries per minute: {moving_avg:.2f}"  # Added moving average
        ]
    }

    # Save the entry to MongoDB
    url = "http://localhost:3000/api/end_conversation"
    response = requests.post(url, json=user_info_payload)

    if response.status_code == 201:
        print("Data successfully sent to API.")
    else:
        print(f"Failed to send data. Status code: {response.status_code}")

    # Optionally save to a local JSON file (without _id)
    file_content_no_id = user_info_payload.copy()
    file_content_no_id.pop("_id", None)

    filename = f"./transcripts/user_data_{i + 1}.json"
    with open(filename, "w") as f:
        json.dump(file_content_no_id, f, indent=4)

# Output the filenames created (if you're also saving locally)
filenames = [f"user_data_{i + 1}.json" for i in range(20)]
print(filenames)
