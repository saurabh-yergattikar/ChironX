"""
Skills Studio - Multi-Skill AI Coaching Platform
Core architecture for handling multiple skills
"""

import os
import cv2
import numpy as np
from PIL import Image
import analysis

# Skill-specific prompts for Gemini
SKILL_PROMPTS = {
    'guitar': """You are a world-class guitar technique analyzer. Given a sequence of video frames, 
analyze the player's chord, detect flaws, and estimate accuracy (0-100). 
For each flaw, provide: (1) a description, (2) reasoning for why it happened, (3) a specific tip to fix it, (4) an estimated timestamp in seconds (if possible), and (5) a reference image or GIF URL showing the correct technique. 
For the drill, provide a one-sentence context of what it helps improve. 
Also, return a progress_history array (last 5 sessions, simulated if needed) with accuracy values. 
Return a JSON object with keys: chord (string), flaws (list of objects with description, reason, tip, timestamp, image_url), accuracy (int), drill (string), drill_context (string), progress_history (list of ints). 
If you can't tell, make your best guess.""",
    
    'piano': """You are a world-class piano technique analyzer. Given a sequence of video frames, 
analyze the player's hand positioning, finger independence, and playing technique. 
For each flaw, provide: (1) a description, (2) reasoning for why it happened, (3) a specific tip to fix it, (4) an estimated timestamp in seconds (if possible), and (5) a reference image or GIF URL showing the correct technique. 
For the drill, provide a one-sentence context of what it helps improve. 
Also, return a progress_history array (last 5 sessions, simulated if needed) with accuracy values. 
Return a JSON object with keys: technique (string), flaws (list of objects with description, reason, tip, timestamp, image_url), accuracy (int), drill (string), drill_context (string), progress_history (list of ints). 
If you can't tell, make your best guess.""",
    
    'tennis': """You are a world-class tennis technique analyzer. Given a sequence of video frames, 
analyze the player's serve motion, grip, footwork, and overall technique. 
For each flaw, provide: (1) a description, (2) reasoning for why it happened, (3) a specific tip to fix it, (4) an estimated timestamp in seconds (if possible), and (5) a reference image or GIF URL showing the correct technique. 
For the drill, provide a one-sentence context of what it helps improve. 
Also, return a progress_history array (last 5 sessions, simulated if needed) with accuracy values. 
Return a JSON object with keys: stroke_type (string), flaws (list of objects with description, reason, tip, timestamp, image_url), accuracy (int), drill (string), drill_context (string), progress_history (list of ints). 
If you can't tell, make your best guess.""",
    
    'drawing': """You are a world-class drawing technique analyzer. Given a sequence of video frames, 
analyze the artist's line quality, perspective, shading techniques, and overall drawing skills. 
For each flaw, provide: (1) a description, (2) reasoning for why it happened, (3) a specific tip to fix it, (4) an estimated timestamp in seconds (if possible), and (5) a reference image or GIF URL showing the correct technique. 
For the drill, provide a one-sentence context of what it helps improve. 
Also, return a progress_history array (last 5 sessions, simulated if needed) with accuracy values. 
Return a JSON object with keys: technique (string), flaws (list of objects with description, reason, tip, timestamp, image_url), accuracy (int), drill (string), drill_context (string), progress_history (list of ints). 
If you can't tell, make your best guess."""
}

class SkillDetector:
    """Detect skill type from video content"""
    
    def detect_skill_type(self, video_path):
        """Analyze video to determine skill category"""
        # For now, return 'guitar' as default
        # In future, use computer vision to detect skill type
        return 'guitar'
    
    def extract_skill_metrics(self, video_path, skill_type):
        """Extract relevant metrics for each skill"""
        frames = self._sample_frames(video_path)
        return self._analyze_frames(frames, skill_type)
    
    def _sample_frames(self, video_path, every_n=5, max_frames=20):
        """Sample frames from video"""
        cap = cv2.VideoCapture(video_path)
        frames = []
        count = 0
        while cap.isOpened() and len(frames) < max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            if count % every_n == 0:
                frame_small = cv2.resize(frame, (224, 224))
                frames.append(frame_small)
            count += 1
        cap.release()
        return frames
    
    def _analyze_frames(self, frames, skill_type):
        """Analyze frames using skill-specific prompts"""
        pil_images = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in frames]
        
        # Get skill-specific prompt
        prompt = SKILL_PROMPTS.get(skill_type, SKILL_PROMPTS['guitar'])
        
        # Use the existing analysis module
        return analysis.process_input_with_prompt('upload', {'frames': pil_images, 'prompt': prompt})

class SkillsStudio:
    """Main Skills Studio orchestrator"""
    
    def __init__(self):
        self.skill_detector = SkillDetector()
        self.available_skills = list(SKILL_PROMPTS.keys())
    
    def analyze_skill(self, video_path, skill_type=None):
        """Analyze video for specific skill or auto-detect"""
        if skill_type is None:
            skill_type = self.skill_detector.detect_skill_type(video_path)
        
        if skill_type not in self.available_skills:
            skill_type = 'guitar'  # Default fallback
        
        return self.skill_detector.extract_skill_metrics(video_path, skill_type)
    
    def get_available_skills(self):
        """Get list of available skills"""
        return self.available_skills
    
    def get_skill_prompt(self, skill_type):
        """Get prompt for specific skill"""
        return SKILL_PROMPTS.get(skill_type, SKILL_PROMPTS['guitar'])

# Global instance
skills_studio = SkillsStudio() 