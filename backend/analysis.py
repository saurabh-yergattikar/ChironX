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
    """Process video upload or live burst. Sample frames, call Gemini, return metrics JSON with flaw details, drill context, and progress history."""
    if input_type == 'upload':
        video_path = data.get('video_path')
        frames = sample_frames(video_path)
        pil_images = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in frames]
        # Enhanced prompt for Gemini
        prompt = (
            "You are a world-class guitar technique analyzer. Given a sequence of video frames, "
            "analyze the player's chord, detect flaws, and estimate accuracy (0-100). "
            "For each flaw, provide: (1) a description, (2) reasoning for why it happened, (3) a specific tip to fix it, (4) an estimated timestamp in seconds (if possible), and (5) a reference image or GIF URL showing the correct technique. "
            "For the drill, provide a one-sentence context of what it helps improve. "
            "Also, return a progress_history array (last 5 sessions, simulated if needed) with accuracy values. "
            "Return a JSON object with keys: chord (string), flaws (list of objects with description, reason, tip, timestamp, image_url), accuracy (int), drill (string), drill_context (string), progress_history (list of ints). "
            "If you can't tell, make your best guess."
        )
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content([prompt, *pil_images])
            import json
            import re
            text = response.text
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                result = json.loads(match.group(0))
                return result
            else:
                return {"error": "Could not parse Gemini response", "raw": text}
        except Exception as e:
            return {"error": str(e)}
    elif input_type == 'live_burst':
        # Simulate a rich response for live burst
        return {
            "chord": "C",
            "flaws": [
                {
                    "description": "Muted G string",
                    "reason": "Your ring finger may be brushing the string.",
                    "tip": "Try arching your ring finger more.",
                    "timestamp": 2,
                    "image_url": "https://www.justinguitar.com/sites/default/files/styles/scale_width_800/public/2021-06/Chord-C-Major.jpg"
                }
            ],
            "accuracy": 60,
            "drill": "E|-----0-----|",
            "drill_context": "Practice this open E string exercise to improve clarity.",
            "progress_history": [40, 50, 55, 60, 60]
        }
    else:
        return {"error": "Unknown input type"} 