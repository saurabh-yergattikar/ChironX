from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import agents

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    video = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)
    # Call agent chain
    result = agents.handle_input({'input_type': 'upload', 'data': {'video_path': video_path}})
    return jsonify(result)

@app.route('/feedback.mp3')
def serve_audio():
    # Serve the generated audio file for demo
    return send_from_directory('.', 'feedback.mp3')

@app.route('/feedback/<filename>')
def serve_dynamic_audio(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 