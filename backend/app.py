from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import agents
import analysis
import skills_studio

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure API keys from environment variables
def configure_api_keys():
    """Configure API keys from environment variables."""
    gemini_key = os.environ.get('GEMINI_API_KEY')
    gcp_project = os.environ.get('GCP_PROJECT_ID')
    gcp_credentials = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    
    if gemini_key or gcp_project:
        agents.set_api_keys(
            gemini_key=gemini_key,
            gcp_project_id=gcp_project,
            gcp_credentials=gcp_credentials
        )
        print("✅ API keys configured from environment variables")
    else:
        print("ℹ️  Running in demo mode - no API keys configured")

@app.route('/skills')
def get_available_skills():
    """Get list of available skills."""
    return jsonify({
        'skills': skills_studio.skills_studio.get_available_skills(),
        'categories': {
            'music': ['guitar', 'piano'],
            'sports': ['tennis'],
            'arts': ['drawing']
        }
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    video = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)
    
    # Use the original analysis flow for compatibility with the frontend
    result = agents.handle_input({'input_type': 'upload', 'data': {'video_path': video_path}})
    
    return jsonify(result)

@app.route('/setup', methods=['POST'])
def setup_api_keys():
    """Set up API keys via API call."""
    data = request.get_json()
    gemini_key = data.get('gemini_key')
    gcp_project = data.get('gcp_project_id')
    gcp_credentials = data.get('gcp_credentials')
    
    agents.set_api_keys(
        gemini_key=gemini_key,
        gcp_project_id=gcp_project,
        gcp_credentials=gcp_credentials
    )
    
    return jsonify({
        'status': 'success',
        'message': 'API keys configured successfully'
    })

@app.route('/status')
def get_status():
    """Get the current status of the application."""
    gemini_key = os.environ.get('GEMINI_API_KEY')
    gcp_project = os.environ.get('GCP_PROJECT_ID')
    
    return jsonify({
        'gemini_configured': bool(gemini_key),
        'gcp_configured': bool(gcp_project),
        'demo_mode': not (gemini_key or gcp_project),
        'available_skills': skills_studio.skills_studio.get_available_skills()
    })

@app.route('/feedback.mp3')
def serve_audio():
    # Serve the generated audio file for demo
    return send_from_directory('.', 'feedback.mp3')

@app.route('/feedback/<filename>')
def serve_dynamic_audio(filename):
    # Get the project root directory (parent of backend directory)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Serving audio file: {filename} from directory: {project_root}")
    return send_from_directory(project_root, filename)

if __name__ == '__main__':
    # Configure API keys on startup
    configure_api_keys()
    
    print("🚀 Starting ChironX Skills Studio...")
    print("📍 Backend will be available at: http://localhost:5001")
    print("🌐 Frontend: Open frontend/index.html in your browser")
    print(f"🎯 Available skills: {skills_studio.skills_studio.get_available_skills()}")
    
    app.run(host='0.0.0.0', port=5001, debug=True) 