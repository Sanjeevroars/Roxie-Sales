import json
from random import choice, randint
from datetime import datetime, timedelta

# Function to generate random time
def random_time(base_time):
    random_seconds = randint(1, 3600)  # random offset in seconds
    return base_time + timedelta(seconds=random_seconds)

# List of locations and models to vary
locations = ["Mumbai, India", "Kolkata, India", "Hyderabad, India"]
models = ["Toyota Prius", "Toyota Corolla", "Toyota Camry"]
names = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Peyton", "Sydney", "Cameron", "Quinn"]

# Generate files
files = []
base_time = datetime.strptime("24-01-2025_21-00-00", "%d-%m-%Y_%H-%M-%S")

for i in range(20):
    name = choice(names)
    location = choice(locations)
    model = choice(models)
    time = random_time(base_time).strftime("%d-%m-%Y_%H-%M-%S")
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

    # Append to list
    files.append(file_content)

# Save as individual files
for idx, file_content in enumerate(files, start=1):
    filename = f"./transcripts/user_data_{idx}.json"
    with open(filename, "w") as f:
        json.dump(file_content, f, indent=4)

# Output the filenames created
[f"user_data_{i}.json" for i in range(1, 21)]
