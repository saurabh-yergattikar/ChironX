# 🎯 Skills Studio - AI Coaching Platform

**Transform any skill with personalized AI coaching**

Skills Studio is a comprehensive AI coaching platform that analyzes your technique across multiple skills - from guitar to tennis, drawing to piano. Get instant feedback, personalized drills, and track your progress with cutting-edge AI analysis.

## 🚀 Quick Start

### One-Click Setup (Recommended)
```bash
git clone https://github.com/saurabh-yergattikar/ChironX.git
cd ChironX
./start.sh
```

### Manual Setup
```bash
git clone https://github.com/saurabh-yergattikar/ChironX.git
cd ChironX
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python start_chironx.py
```

**📖 For detailed installation instructions, see [INSTALLATION.md](INSTALLATION.md)**

## 🎨 Available Skills

### 🎸 **Music & Instruments**
- **Guitar** - Chord analysis, finger positioning, strumming patterns
- **Piano** - Hand positioning, finger independence, playing technique

### 🏃‍♂️ **Sports & Fitness**
- **Tennis** - Serve motion, grip analysis, footwork

### 🎨 **Arts & Crafts**
- **Drawing** - Line quality, perspective, shading techniques

*More skills coming soon: Drums, Basketball, Yoga, Cooking, and more!*

## 🔧 API Key Setup

### Method 1: Interactive Setup (Recommended)
Run the startup script and follow the prompts:
```bash
python start_chironx.py
```

### Method 2: Environment Variables
```bash
export GEMINI_API_KEY="your_gemini_api_key"
export GCP_PROJECT_ID="your_gcp_project_id"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
```

### Method 3: API Call
```bash
curl -X POST http://localhost:5001/setup \
  -H "Content-Type: application/json" \
  -d '{
    "gemini_key": "your_gemini_api_key",
    "gcp_project_id": "your_gcp_project_id",
    "gcp_credentials": "path/to/service-account.json"
  }'
```

## 🎯 How It Works

1. **Select Your Skill** - Choose from guitar, piano, tennis, drawing, and more
2. **Upload Your Video** - Record yourself practicing the skill
3. **Get AI Analysis** - Receive detailed feedback on technique, accuracy, and areas for improvement
4. **Practice with Drills** - Get personalized exercises to improve your skills
5. **Track Progress** - Monitor your improvement over time

## 🎮 Demo Mode

Skills Studio works without API keys in demo mode, providing simulated analysis for testing and demonstration purposes.

## 🌐 Accessing the Application

1. **Start the backend**: `python backend/app.py`
2. **Open the frontend**: 
   - **Skills Studio**: `frontend/skills-studio.html` (Multi-skill interface)
   - **Guitar Tutor**: `frontend/index.html` (Original guitar-focused interface)
3. **Upload a video** and get instant AI feedback!

## 🏗️ Architecture

```
Skills Studio
├── Skill Detection Engine
├── Multi-Skill Analysis Pipeline
├── Skill-Specific AI Models
└── Progress Tracking System
```

## 🎯 Features

- **Multi-Skill Support**: Analyze guitar, piano, tennis, drawing, and more
- **Real-time Analysis**: Get instant feedback on your technique
- **Personalized Drills**: Receive custom exercises for improvement
- **Progress Tracking**: Monitor your skill development over time
- **Demo Mode**: Test without API keys
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start for Different Users

### 🎓 **Beginner**
1. Download and run `./start.sh`
2. Follow the setup prompts
3. Open `frontend/skills-studio.html`
4. Select a skill and upload a video

### 👨‍💻 **Developer**
1. Clone the repository
2. Set up virtual environment
3. Configure API keys
4. Run `python backend/app.py`
5. Access the API at `http://localhost:5001`

### 🏢 **Enterprise**
1. Deploy using Docker: `docker build -t skills-studio .`
2. Run: `docker run -p 5001:5001 skills-studio`
3. Configure enterprise API keys
4. Scale as needed

## 🐳 Docker Users

```bash
# Build the image
docker build -t skills-studio .

# Run the container
docker run -p 5001:5001 skills-studio

# With custom API keys
docker run -p 5001:5001 \
  -e GEMINI_API_KEY="your_key" \
  -e GCP_PROJECT_ID="your_project" \
  skills-studio
```

## 📋 Requirements

- **Python 3.8+**
- **Google Cloud Platform** (for production)
- **Gemini API Key** (for production)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

## 🔧 Troubleshooting

### Common Issues

**"Module not found" errors**
```bash
pip install -r requirements.txt
```

**"API key not configured"**
- Set environment variables or use interactive setup
- Demo mode will work without keys

**"Backend not responding"**
```bash
# Check if port 5001 is in use
lsof -ti:5001 | xargs kill -9
# Restart the backend
python backend/app.py
```

**"Audio not playing"**
- Ensure backend is running on port 5001
- Check browser console for errors
- Try refreshing the page

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- **New Skills**: Add support for more skills (dancing, cooking, etc.)
- **UI/UX**: Improve the user interface and experience
- **AI Models**: Enhance analysis accuracy
- **Mobile App**: Create native mobile applications
- **Documentation**: Improve guides and tutorials

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Vision

**Skills Studio** aims to democratize AI coaching, making personalized skill development accessible to everyone, regardless of location or resources.

**"From guitar to golf, drawing to dancing - one AI platform for all skills."** 🚀

---

**Built with ❤️**
