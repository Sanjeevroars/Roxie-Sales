import os
import json

# Define the folder path containing input files
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
                
                # Extract the required fields
                enquiry_details = {
                    "name": file_data["user_info"]["name"],
                    "contact": file_data["user_info"]["contact"],
                    "date": file_data["user_info"]["date"],
                    "interested_model": file_data["user_info"]["interested_model"],
                    "location": file_data["user_info"]["location"],
                }
                
                # Save the enquiry details to a new JSON file
                output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_enquiry.json")
                with open(output_file, "w") as output:
                    json.dump(enquiry_details, output, indent=4)
                
                print(f"Processed and saved: {output_file}")
            except (KeyError, json.JSONDecodeError) as e:
                print(f"Error processing {filename}: {e}")
