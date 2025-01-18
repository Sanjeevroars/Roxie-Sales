from flask import Flask, send_from_directory, request, jsonify, render_template
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

app = Flask(__name__, static_folder='build', static_url_path='')

# In-memory storage for the current conversation transcript
current_transcript = []

# Directory to save transcripts
TRANSCRIPT_DIR = os.path.abspath('transcripts')

# Directory to save enquiries
ENQUIRIES_DIR = os.path.abspath('enquiries')

# Ensure the transcript directory exists
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(ENQUIRIES_DIR, exist_ok=True)

load_dotenv()
MONGO_URI = os.getenv("mongoDB.uri")
client = MongoClient(MONGO_URI)
db = client["client_info"]
enquiry_collection = db["enquiry_details"]
transcript_collection = db["transcript_details"]

# Function to save the current transcript to a file
def save_transcript(user_info):
    transcript_data = {
        "user_info": user_info,
        "transcript": current_transcript.copy()  # Ensure we don't clear before saving
    }

    # Insert the transcript into MongoDB
    transcript_collection.insert_one(transcript_data)
    current_transcript.clear()

def save_enquiry(user_info, model, location):
    enquiry_data = {
        "name": user_info.get("name"),
        "contact": user_info.get("contact"),
        "date": user_info.get("date"),
        "interested_model": user_info.get("interested_model"),
        "location": user_info.get("location")
    }
    filename = f"{ENQUIRIES_DIR}/{user_info['date']}_{user_info['name']}_enquiry.json"
    with open(filename, 'w') as f:
        json.dump(enquiry_data, f, indent=4)

    enquiry_collection.insert_one(enquiry_data)

# Route to serve the React app's static files
@app.route('/')
@app.route('/<path:path>')
def serve_static(path='index.html'):
    return send_from_directory(app.static_folder, path)

# API to update the transcript
@app.route('/api/update_transcript', methods=['POST'])
def update_transcript():
    data = request.json
    line = data.get('line')
    if line:
        current_transcript.append(line)
    return jsonify({'success': True, 'transcript': current_transcript})

# API to get the current transcript
@app.route('/api/get_transcript', methods=['GET'])
def get_transcript():
    return jsonify({'transcript': current_transcript})

# API to end the conversation and save the transcript
@app.route('/api/end_conversation', methods=['POST'])
def end_conversation():
    user_info = request.json.get('user_info')
    interested_model = request.json.get('interested_model')
    location = request.json.get('location', "Unknown")
    if user_info:
        save_transcript(user_info)
        save_enquiry(user_info, interested_model, location)
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

# API to list all saved transcripts
@app.route('/api/list_transcripts', methods=['GET'])
def list_transcripts():
    transcripts = transcript_collection.find()
    response = [{"_id": str(t["_id"]), "user_info": t["user_info"]} for t in transcripts]
    return jsonify({'transcripts': response})

# API to list all saved enquiries
@app.route('/api/list_enquiries', methods=['GET'])
def list_enquiries():
    enquiries = enquiry_collection.find()
    response = [{"_id": str(e["_id"]), "name": e["name"], "date": e["date"]} for e in enquiries]
    return jsonify({'enquiries': response})


@app.route('/api/load_transcript/<transcript_id>', methods=['GET'])
def load_transcript(transcript_id):
    transcript = transcript_collection.find_one({"_id": ObjectId(transcript_id)})
    if transcript:
        transcript["_id"] = str(transcript["_id"])  # Convert ObjectId to string
        return jsonify({'transcript': transcript})
    return jsonify({'error': 'Transcript not found'}), 404

@app.route('/api/load_enquiry/<enquiry_id>', methods=['GET'])
def load_enquiry(enquiry_id):
    enquiry = enquiry_collection.find_one({"_id": ObjectId(enquiry_id)})
    if enquiry:
        enquiry["_id"] = str(enquiry["_id"])  # Convert ObjectId to string
        return jsonify({'enquiry': enquiry})
    return jsonify({'error': 'Enquiry not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
