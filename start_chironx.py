#!/usr/bin/env python3
"""
ChironX Startup Script
Prompts for API keys and starts the application
"""

import os
import sys
import subprocess
import getpass
from pathlib import Path

def print_banner():
    """Print the ChironX banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║  🎸 ChironX - Skills Studio
║  Built   July 2025                                           ║
║  Transform your guitar playing with AI analysis              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def configure_manual_keys():
    """Configure API keys manually."""
    print("\n🔑 Manual API Key Configuration")
    print("=" * 40)
    
    # Get Gemini API Key
    gemini_key = input("Enter your Gemini API Key: ").strip()
    if not gemini_key:
        print("❌ Gemini API Key is required!")
        return False
    
    # Get GCP Project ID
    gcp_project = input("Enter your GCP Project ID: ").strip()
    if not gcp_project:
        print("❌ GCP Project ID is required!")
        return False
    
    # Get GCP Credentials (optional)
    gcp_credentials = input("Enter path to GCP service account JSON (optional): ").strip()
    
    # Set environment variables
    os.environ['GEMINI_API_KEY'] = gemini_key
    os.environ['GCP_PROJECT_ID'] = gcp_project
    if gcp_credentials:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = gcp_credentials
    
    print("✅ API keys configured!")
    start_backend()
    return True

def start_backend():
    """Start the Flask backend server."""
    print("\n🚀 Starting ChironX Backend...")
    print("📍 Backend will be available at: http://localhost:5001")
    print("🌐 Frontend: Open frontend/index.html in your browser")
    print("\n" + "="*50)
    
    # Start the backend
    try:
        subprocess.run([sys.executable, "backend/app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 ChironX stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to start backend: {e}")
        return False
    
    return True

def main():
    """Main startup function."""
    print_banner()
    
    print("\n🔧 API Key Configuration")
    print("=" * 50)
    print("Choose how to configure your API keys:")
    print("1. Use environment variables (if already set)")
    print("2. Enter API keys manually")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Check if environment variables are already set
            gemini_key = os.environ.get('GEMINI_API_KEY')
            gcp_project = os.environ.get('GCP_PROJECT_ID')
            
            if gemini_key and gcp_project:
                print("✅ Environment variables found!")
                print(f"   Gemini API Key: {gemini_key[:10]}...")
                print(f"   GCP Project ID: {gcp_project}")
                start_backend()
                break
            else:
                print("❌ Environment variables not found.")
                print("Please set GEMINI_API_KEY and GCP_PROJECT_ID, or choose option 2.")
                continue
                
        elif choice == "2":
            configure_manual_keys()
            break
            
        elif choice == "3":
            print("👋 Goodbye!")
            sys.exit(0)
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main() 