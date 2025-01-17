from flask import Flask, send_from_directory, request, jsonify, render_template
import json
import os

app = Flask(__name__, static_folder='build', static_url_path='')

# In-memory storage for the current conversation transcript
current_transcript = []

# Directory to save transcripts
TRANSCRIPT_DIR = os.path.abspath('transcripts')

# Ensure the transcript directory exists
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

# Function to save the current transcript to a file
def save_transcript(user_info):
    filename = f"{TRANSCRIPT_DIR}/{user_info['date']}_{user_info['name']}.json"
    with open(filename, 'w') as f:
        json.dump({"user_info": user_info, "transcript": current_transcript}, f, indent=4)
    current_transcript.clear()

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
    if user_info:
        save_transcript(user_info)
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

# API to list all saved transcripts
@app.route('/api/list_transcripts', methods=['GET'])
def list_transcripts():
    transcripts = [filename for filename in os.listdir(TRANSCRIPT_DIR) if filename.endswith('.json')]
    return jsonify({'transcripts': transcripts})

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
