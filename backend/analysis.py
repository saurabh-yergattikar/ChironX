import cv2
import numpy as np
import google.generativeai as genai
import os
import base64
import io
from PIL import Image

# --- Helper: Sample Frames from Video ---
def sample_frames(video_path, every_n=5, max_frames=20):
    """Sample every_n-th frame from video, up to max_frames."""
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    while cap.isOpened() and len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if count % every_n == 0:
            # Resize for efficiency
            frame_small = cv2.resize(frame, (224, 224))
            frames.append(frame_small)
        count += 1
    cap.release()
    return frames

# --- Helper: Encode frames as base64 PNGs ---
def encode_frames_to_base64(frames):
    """Convert list of np.array frames to list of base64-encoded PNG strings."""
    encoded = []
    for frame in frames:
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        encoded.append(base64.b64encode(buf.read()).decode('utf-8'))
    return encoded

# --- Main Processing Function ---
def process_input(input_type, data):
    """Process video upload or live burst. Sample frames, call Gemini, return metrics JSON."""
    if input_type == 'upload':
        video_path = data.get('video_path')
        frames = sample_frames(video_path)
        # Convert OpenCV frames to PIL Images
        pil_images = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in frames]
        # Compose prompt for Gemini
        prompt = (
            "You are a guitar technique analyzer. Given a sequence of video frames, "
            "analyze the player's chord, detect flaws, and estimate accuracy (0-100). "
            "Return a JSON object with keys: chord (string), flaws (list of strings), accuracy (int). "
            "If you can't tell, make your best guess."
        )
        # Call Gemini (Vision model)
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Pass prompt and PIL Images directly
            response = model.generate_content([prompt, *pil_images])
            # Try to extract JSON from response
            import json
            import re
            text = response.text
            # Extract JSON object from text
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                result = json.loads(match.group(0))
                return result
            else:
                # Fallback: return raw text
                return {"error": "Could not parse Gemini response", "raw": text}
        except Exception as e:
            return {"error": str(e)}
    elif input_type == 'live_burst':
        # TODO: Handle live burst input (simulate webcam burst)
        return {"chord": "C", "flaws": ["timing off"], "accuracy": 60}
    else:
        return {"error": "Unknown input type"} 