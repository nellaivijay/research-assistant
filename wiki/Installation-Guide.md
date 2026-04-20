# Installation Guide

Complete guide for installing and setting up the Enhanced Research Assistant.

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Local Installation](#local-installation)
3. [Environment Setup](#environment-setup)
4. [Dependencies Installation](#dependencies-installation)
5. [Configuration](#configuration)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Python**: 3.10 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum
- **Disk Space**: 500MB free space
- **Network**: Internet connection for API calls

### Recommended Requirements
- **Python**: 3.10 or 3.11
- **Memory**: 8GB RAM or more
- **Disk Space**: 1GB free space
- **Network**: Stable internet connection

## Local Installation

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/nellaivijay/research-assistant.git
cd research-assistant
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list
```

## Environment Setup

### Development Environment

#### For Python Development
```bash
# Install development tools
pip install black flake8 mypy pytest
```

#### For Code Formatting
```bash
# Install black for code formatting
pip install black

# Format code
black app.py
```

#### For Linting
```bash
# Install flake8 for linting
pip install flake8

# Run linting
flake8 app.py
```

### Production Environment

#### Docker Setup (Optional)
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

```bash
# Build Docker image
docker build -t research-assistant .

# Run container
docker run -p 7860:7860 research-assistant
```

## Dependencies Installation

### Core Dependencies

The `requirements.txt` file includes:

```
gradio==4.0.0           # Web interface framework
requests>=2.31.0      # HTTP client library
cachetools>=5.3.0     # Caching utilities
openai>=1.0.0         # OpenAI API client
anthropic>=0.18.0     # Anthropic API client
google-generativeai>=0.3.0  # Google AI API client
```

### Optional Dependencies

For development and testing:

```
black==23.0.0          # Code formatting
flake8==6.0.0          # Linting
pytest==7.0.0          # Testing framework
mypy==1.0.0            # Type checking
```

### Installing Optional Dependencies

```bash
# Install development dependencies
pip install black flake8 pytest mypy
```

## Configuration

### Environment Variables

Create a `.env` file for local development:

```env
# OpenAI API Key (optional)
OPENAI_API_KEY=your_openai_key_here

# Anthropic API Key (optional)
ANTHROPIC_API_KEY=your_anthropic_key_here

# Google AI API Key (optional)
GOOGLE_API_KEY=your_google_key_here

# Hugging Face Token (for deployment)
HF_TOKEN=your_huggingface_token_here
```

### API Key Setup

#### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-`)
4. Add to `.env` file or application UI

#### Anthropic API Key
1. Go to https://console.anthropic.com/
2. Create API key
3. Copy the key
4. Add to `.env` file or application UI

#### Google AI API Key
1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Copy the key
4. Add to `.env` file or application UI

### Gradio Configuration

The application uses Gradio 4.0.0 with default settings:

```python
# In app.py, the Gradio interface is configured as:
demo = create_research_assistant()
demo.launch()
```

Custom Gradio settings (optional):
```python
demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False,
    show_error=True,
    quiet=False
)
```

## Verification

### Test Installation

```bash
# Run Python syntax check
python -m py_compile app.py

# Run the application
python app.py
```

### Verify Dependencies

```bash
# Check if all dependencies are installed
python -c "import gradio; print('Gradio:', gradio.__version__)"
python -c "import requests; print('Requests:', requests.__version__)"
python -c "import json; print('JSON module OK')"
```

### Test Application Functionality

1. **Start the application**:
```bash
python app.py
```

2. **Access the interface**:
   - Open http://localhost:7860 in your browser
   - Verify all tabs are visible
   - Test basic functionality

3. **Test model configuration**:
   - Go to Model Selection tab
   - Verify available models are listed
   - Test API key saving (if configured)

## Troubleshooting

### Common Installation Issues

#### Python Version Issues
**Problem**: Python version too old
```bash
# Check Python version
python --version

# Solution: Install Python 3.10+
# Visit https://www.python.org/downloads/
```

#### Virtual Environment Issues
**Problem**: Virtual environment not activating
```bash
# Solution: Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

#### Dependency Installation Failures
**Problem**: pip install fails
```bash
# Solution 1: Upgrade pip
pip install --upgrade pip

# Solution 2: Install dependencies individually
pip install gradio==4.0.0
pip install requests
pip install cachetools
```

#### Import Errors
**Problem**: Module not found errors
```bash
# Solution: Verify installation
pip list

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
**Problem**: Port 7860 already in use
```bash
# Solution: Kill existing process
# On Linux/macOS:
lsof -ti:7860 | xargs kill

# On Windows:
netstat -ano | findstr :7860
taskkill /PID <PID> /F
```

### API Key Issues
**Problem**: API keys not working
```bash
# Solution: Verify API key format
# Check that keys don't have extra spaces or quotes
# Verify API key has proper permissions
```

### Memory Issues
**Problem**: Application runs out of memory
```bash
# Solution: Increase system memory
# Close other applications
# Use lighter AI models
```

## Advanced Installation

### Custom Python Installation

```bash
# Install specific Python version using pyenv (macOS/Linux)
pyenv install 3.10.0
pyenv local 3.10.0
```

### Using Conda

```bash
# Create conda environment
conda create -n research-assistant python=3.10
conda activate research-assistant

# Install dependencies
pip install -r requirements.txt
```

### Development Installation

```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Post-Installation Steps

### 1. Configure API Keys (Optional)
- Set up OpenAI API key if using GPT models
- Set up Anthropic API key if using Claude models
- Set up Google AI API key if using Gemini models

### 2. Test Basic Functionality
- Start the application: `python app.py`
- Access interface at http://localhost:7860
- Test paper recommendations
- Test reading list management

### 3. Configure Git (Optional)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4. Set Up GitHub Integration (Optional)
- Add GitHub remote
- Configure GitHub Actions
- Set up GitHub Pages

## Uninstallation

### Remove Virtual Environment
```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment directory
rm -rf venv
```

### Remove Application Files
```bash
# Remove cloned repository
cd ..
rm -rf research-assistant
```

## Next Steps

After installation:

1. **Read the [Getting Started Guide](Getting-Started.md)**
2. **Configure API keys** for AI features
3. **Explore the [User Guide](User-Guide.md)**
4. **Set up GitHub integration** (optional)
5. **Deploy to production** (optional)

---

**For more information, visit the [GitHub Repository](https://github.com/nellaivijay/research-assistant)**