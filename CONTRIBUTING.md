# Contributing to ChironX

Thank you for your interest in contributing to ChironX! This document provides guidelines and information for contributors.

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/saurabh-yergattikar/ChironX
   cd ChironX
   ```
3. **Set up the development environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🔧 Development Setup

### Running in Development Mode
```bash
# Start the backend with debug mode
python backend/app.py

# The frontend can be opened directly in your browser
# Open frontend/index.html
```

### Testing Your Changes
```bash
# Test the backend API
curl http://localhost:5001/status

# Test video upload (replace with your video file)
curl -X POST -F "video=@your_video.mp4" http://localhost:5001/analyze
```

## 📝 Making Changes

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

### Commit Messages
Use conventional commit format:
```
feat: add new guitar analysis feature
fix: resolve video upload issue
docs: update installation instructions
style: format code according to PEP 8
refactor: simplify API key configuration
test: add unit tests for video processing
```

### Pull Request Process
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test your changes thoroughly
4. Commit with a descriptive message
5. Push to your fork: `git push origin feature/your-feature`
6. Create a Pull Request with a clear description

## 🎯 Areas for Contribution

### High Priority
- **Frontend Improvements**: Better UI/UX, responsive design
- **Video Processing**: Support for more video formats
- **Analysis Accuracy**: Improve guitar technique detection
- **Documentation**: Better guides and examples

### Medium Priority
- **New Instruments**: Extend to piano, drums, etc.
- **Real-time Analysis**: Live video streaming
- **User Management**: User accounts and progress tracking
- **Mobile Support**: Progressive Web App features

### Low Priority
- **Advanced Features**: Multi-user sessions, competitions
- **Integration**: Music theory apps, sheet music generation
- **Analytics**: Detailed progress tracking and insights

## 🐛 Reporting Issues

When reporting issues, please include:
- **Description**: What happened vs. what you expected
- **Steps to Reproduce**: Clear, numbered steps
- **Environment**: OS, Python version, browser
- **Screenshots**: If applicable
- **Logs**: Any error messages or console output

## 💡 Feature Requests

For feature requests:
- **Use Case**: Describe the problem you're solving
- **Proposed Solution**: How you think it should work
- **Alternatives**: Other approaches you've considered
- **Mockups**: If applicable, include UI mockups

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=backend tests/
```

### Writing Tests
- Test both success and failure cases
- Mock external API calls
- Test edge cases and error conditions
- Aim for good test coverage

## 📚 Documentation

### Code Documentation
- Add docstrings to all functions and classes
- Include type hints where possible
- Document complex algorithms

### User Documentation
- Update README.md for new features
- Add examples and use cases
- Include troubleshooting guides

## 🔐 Security

- Never commit API keys or sensitive data
- Use environment variables for configuration
- Validate all user inputs
- Follow security best practices

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Wiki**: For detailed documentation

## 🎉 Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for contributing to ChironX! 🎸 