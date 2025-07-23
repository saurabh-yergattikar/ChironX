import cv2
import numpy as np
import google.generativeai as genai
import os

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

def process_input(input_type, data):
    """Process video upload or live burst. Sample frames, extract audio, call Gemini, return metrics JSON."""
    if input_type == 'upload':
        video_path = data.get('video_path')
        frames = sample_frames(video_path)
        # TODO: Extract audio from video (e.g., with ffmpeg or Gemini Audio)
        # TODO: Call Gemini with frames/audio, parse response
        # For now, return mock metrics
        return {"chord": "Am", "flaws": ["sloppy fretting"], "accuracy": 80}
    elif input_type == 'live_burst':
        # TODO: Handle live burst input (simulate webcam burst)
        return {"chord": "C", "flaws": ["timing off"], "accuracy": 60}
    else:
        return {"error": "Unknown input type"} 