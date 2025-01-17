from flask import Flask, send_from_directory, request, jsonify, render_template
import json
import os

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


# Function to save the current transcript to a file
def save_transcript(user_info):
    filename = f"{TRANSCRIPT_DIR}/{user_info['date']}_{user_info['name']}.json"
    with open(filename, 'w') as f:
        json.dump({"user_info": user_info, "transcript": current_transcript}, f, indent=4)
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
    transcripts = [filename for filename in os.listdir(TRANSCRIPT_DIR) if filename.endswith('.json')]
    return jsonify({'transcripts': transcripts})

# API to list all saved enquiries
@app.route('/api/list_enquiries', methods=['GET'])
def list_enquiries():
    enquiries = [filename for filename in os.listdir(ENQUIRIES_DIR) if filename.endswith('.json')]
    return jsonify({'enquiries': enquiries})


# API to load a specific enquiry
@app.route('/api/load_enquiry/<filename>', methods=['GET'])
def load_enquiry(filename):
    filepath = os.path.join(ENQUIRIES_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            enquiry_data = json.load(f)
        return jsonify({'enquiry': enquiry_data})
    return jsonify({'error': 'Enquiry not found'}), 404

# API to load a specific transcript
@app.route('/api/load_transcript/<filename>', methods=['GET'])
def load_transcript(filename):
    filepath = os.path.join(TRANSCRIPT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            transcript_data = json.load(f)
        return jsonify({'transcript': transcript_data})
    return jsonify({'error': 'Transcript not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
