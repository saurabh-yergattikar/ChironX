import os
import uuid
import analysis

# Try to import Google Cloud services, but handle gracefully if not available
try:
    import google.cloud.aiplatform as aiplatform
    import google.cloud.texttospeech as tts
    import google.generativeai as genai
    from google.cloud import firestore
    from google.cloud import storage
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False
    print("Google Cloud services not available - running in demo mode")

# Global variables for API keys
GEMINI_API_KEY = None
GCP_PROJECT_ID = None
GCP_CREDENTIALS = None

def set_api_keys(gemini_key=None, gcp_project_id=None, gcp_credentials=None):
    """Set API keys for Google Cloud services."""
    global GEMINI_API_KEY, GCP_PROJECT_ID, GCP_CREDENTIALS, GOOGLE_CLOUD_AVAILABLE
    
    GEMINI_API_KEY = gemini_key
    GCP_PROJECT_ID = gcp_project_id
    GCP_CREDENTIALS = gcp_credentials
    
    if gemini_key and GOOGLE_CLOUD_AVAILABLE:
        try:
            genai.configure(api_key=gemini_key)
            print("Gemini API key configured successfully")
        except Exception as e:
            print(f"Failed to configure Gemini API: {e}")
    
    if gcp_project_id and GOOGLE_CLOUD_AVAILABLE:
        try:
            aiplatform.init(project=gcp_project_id)
            print("GCP project configured successfully")
        except Exception as e:
            print(f"Failed to configure GCP project: {e}")
    
    # Set the API key in analysis module
    analysis.set_gemini_api_key(gemini_key)

# --- Agent Stubs ---
def analyzer(input_data):
    """Analyze input (video/audio), return metrics JSON."""
    # Call analysis.process_input and Gemini for metrics
    return analysis.process_input(input_data.get('input_type'), input_data.get('data'))

def statistician(metrics):
    """Update stats in Firebase, calculate improvement."""
    # Example: db.collection('sessions').add({...})
    errors = len(metrics.get("flaws", []))
    improvement = metrics.get("accuracy", 0)  # Placeholder
    # TODO: Uncomment to update Firestore
    # db.collection('sessions').add({'user_id': 'anon', 'errors': errors, 'improvement': improvement})
    return {"errors": errors, "improvement": improvement}

def coach(analysis_result):
    """Generate personalized coaching feedback based on analysis."""
    try:
        metrics = analysis_result.get('metrics', {})
        chord = metrics.get('chord', 'chord')
        accuracy = metrics.get('accuracy', 75)
        flaws = metrics.get('flaws', [])
        
        # Create detailed, specific feedback
        if accuracy >= 80:
            feedback_text = f"Excellent work on the {chord} chord! Your {accuracy}% accuracy shows solid technique."
        elif accuracy >= 60:
            feedback_text = f"Good progress on the {chord} chord with {accuracy}% accuracy. Let's refine your technique."
        else:
            feedback_text = f"Keep practicing the {chord} chord. Your {accuracy}% accuracy indicates areas for improvement."
        
        # Add specific flaw feedback
        if flaws and len(flaws) > 0:
            flaw = flaws[0]
            feedback_text += f" Focus on: {flaw.get('description', 'technique')}. {flaw.get('tip', 'Practice slowly and deliberately.')}"
        
        # Add practice drill
        drill = f"Practice: {chord} chord transitions for 5 minutes daily"
        
        return {
            "feedback_text": feedback_text,
            "drill": drill,
            "navigate_skills": "Ready to try another skill or continue practicing!"
        }
        
    except Exception as e:
        print(f"Coach error: {e}")
        return {
            "feedback_text": "Great guitar playing! Keep practicing your chord transitions.",
            "drill": "Practice chord transitions for 5 minutes daily",
            "navigate_skills": "Ready to try another skill!"
        }

def automator(input_data):
    """Generate audio feedback using TTS."""
    try:
        # Check if we have GCP credentials
        if not GOOGLE_CLOUD_AVAILABLE:
            print("Google Cloud not available, using demo audio")
            return {
                'audio_url': '/feedback.mp3',
                'feedback_text': 'Demo audio feedback - practice your chord transitions!'
            }
        
        # Get the coach feedback
        coach_feedback = input_data.get('feedback_text', '')
        drill = input_data.get('drill', '')
        
        # Create a comprehensive audio message
        if coach_feedback:
            # Combine coach feedback with drill instruction
            audio_text = f"{coach_feedback} {drill}. Keep up the great work!"
        else:
            audio_text = "Great guitar playing! Practice your chord transitions daily for improvement."
        
        # Generate audio with faster settings
        audio_content = text_to_speech(audio_text, voice_name="en-US-Neural2-D", speaking_rate=1.1)
        
        if audio_content:
            # Generate a shorter filename
            filename = f"feedback_{hash(audio_text) % 1000000}.mp3"
            filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), filename)
            
            with open(filepath, 'wb') as f:
                f.write(audio_content)
            
            print(f"TTS successful: {filename}")
            return {
                'audio_url': f'/feedback/{filename}',
                'feedback_text': audio_text
            }
        else:
            print("TTS failed, using demo audio")
            return {
                'audio_url': '/feedback.mp3',
                'feedback_text': 'Demo audio feedback - practice your chord transitions!'
            }
            
    except Exception as e:
        print(f"Automator error: {e}")
        return {
            'audio_url': '/feedback.mp3',
            'feedback_text': 'Demo audio feedback - practice your chord transitions!'
        }

def text_to_speech(text, voice_name="en-US-Neural2-D", speaking_rate=1.1):
    """Convert text to speech with optimized settings for faster generation."""
    if not GOOGLE_CLOUD_AVAILABLE:
        return None
        
    try:
        client = tts.TextToSpeechClient()
        
        # Truncate text if it's too long for faster processing
        if len(text) > 200:
            text = text[:200] + "..."
        
        # Use simpler synthesis input for faster processing
        synthesis_input = tts.SynthesisInput(text=text)
        
        voice = tts.VoiceSelectionParams(
            language_code="en-US",
            name=voice_name  # Changed to male voice: en-US-Neural2-D
        )
        
        audio_config = tts.AudioConfig(
            audio_encoding=tts.AudioEncoding.MP3,
            speaking_rate=speaking_rate,  # Faster speech
            pitch=0.0,                    # Normal pitch
            effects_profile_id=["headphone-class-device"]  # Optimized for headphones
        )
        
        response = client.synthesize_speech(
            input=synthesis_input, 
            voice=voice, 
            audio_config=audio_config
        )
        
        return response.audio_content
        
    except Exception as e:
        print(f"TTS error: {e}")
        return None

# --- Main Handler: Orchestrate Agent Chain ---
def handle_input(input_data):
    """Full agentic workflow: analyze -> stats -> coach -> TTS/audio."""
    metrics = analyzer(input_data)
    stats = statistician(metrics)
    coach_out = coach(metrics) # Changed to pass metrics to coach
    tts_out = automator(coach_out)
    # Collect agent thoughts/logs for frontend
    logs = [
        f"Analyzer: {metrics}",
        f"Statistician: {stats}",
        f"Coach: {coach_out}",
        f"Automator: {tts_out}"
    ]
    return {
        "metrics": metrics,
        "stats": stats,
        "coach": coach_out,
        "audio_url": tts_out["audio_url"],
        "logs": logs
    } 