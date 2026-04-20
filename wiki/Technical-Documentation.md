# Technical Documentation

Complete technical documentation for developers working on the Enhanced Research Assistant.

## 📚 Table of Contents

1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [API Integration](#api-integration)
5. [Database Schema](#database-schema)
6. [Testing Guide](#testing-guide)
7. [Deployment](#deployment)
8. [Contributing](#contributing)

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment (recommended)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/nellaivijay/research-assistant.git
cd research-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Access the application**
- Open http://localhost:7860 in your browser

### Environment Variables

Create a `.env` file for local development:

```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
HF_TOKEN=your_huggingface_token
```

## Project Structure

```
research-assistant/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── .github/
│   └── workflows/
│       ├── ci-cd.yml          # CI/CD pipeline
│       └── docs-deploy.yml    # Documentation deployment
├── docs/
│   └── index.html             # GitHub Pages site
├── wiki/                       # GitHub Wiki content
│   ├── _Home.md
│   ├── Getting-Started.md
│   ├── User-Guide.md
│   └── ...
├── GITHUB_SETUP.md            # GitHub setup guide
├── README.md                  # Project README
└── .gitignore                 # Git ignore rules
```

## Core Components

### 1. ModelConfig Class

Manages AI model configurations and capabilities.

```python
class ModelConfig:
    def __init__(self):
        self.models = {
            "model_id": {
                "name": "Human-readable name",
                "type": "api_type",
                "cost": "Free|Low|Medium|High",
                "capabilities": ["list", "of", "capabilities"],
                "complexity": "basic|advanced|expert",
                "api_key_env": "ENV_VAR_NAME"
            }
        }
    
    def get_available_models(self):
        """Return all available models"""
        return self.models
    
    def get_models_by_capability(self, capability):
        """Return models with specific capability"""
        return {k: v for k, v in self.models.items() 
                if capability in v['capabilities']}
```

### 2. DataManager Class

Handles reading list, notes, and progress tracking.

```python
class DataManager:
    def __init__(self):
        self.reading_lists = {}
        self.notes = {}
        self.progress = {}
    
    def add_to_reading_list(self, user_id, paper):
        """Add paper to user's reading list"""
        if user_id not in self.reading_lists:
            self.reading_lists[user_id] = []
        self.reading_lists[user_id].append(paper)
    
    def get_reading_list(self, user_id):
        """Get user's reading list"""
        return self.reading_lists.get(user_id, [])
    
    def save_note(self, user_id, paper_id, note):
        """Save note for a paper"""
        key = f"{user_id}_{paper_id}"
        self.notes[key] = note
    
    def get_notes(self, user_id, paper_id):
        """Get notes for a paper"""
        key = f"{user_id}_{paper_id}"
        return self.notes.get(key, "")
```

### 3. AIServices Class

Manages AI model invocation and response processing.

```python
class AIServices:
    def __init__(self, model_config):
        self.model_config = model_config
        self.api_clients = {}
    
    def analyze_paper(self, model_id, paper_data, prompt):
        """Analyze paper using specified model"""
        model_info = self.model_config.models[model_id]
        
        if model_info['type'] == 'rule_based':
            return self._rule_based_analysis(paper_data, prompt)
        elif model_info['type'] == 'openai':
            return self._openai_analysis(model_id, paper_data, prompt)
        # ... other model types
    
    def _rule_based_analysis(self, paper_data, prompt):
        """Rule-based analysis without API calls"""
        # Implementation using pattern matching and heuristics
        pass
    
    def _openai_analysis(self, model_id, paper_data, prompt):
        """OpenAI API analysis"""
        client = self._get_openai_client()
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": str(paper_data)}
            ]
        )
        return response.choices[0].message.content
```

### 4. ABTestManager Class

Manages A/B testing functionality.

```python
class ABTestManager:
    def __init__(self):
        self.test_history = []
        self.preferences = {}
    
    def run_test(self, paper_data, model_a, model_b, analysis_type):
        """Run A/B test between two models"""
        result_a = self._analyze_with_model(paper_data, model_a, analysis_type)
        result_b = self._analyze_with_model(paper_data, model_b, analysis_type)
        
        return {
            'model_a': model_a,
            'model_b': model_b,
            'result_a': result_a,
            'result_b': result_b,
            'timestamp': datetime.now()
        }
    
    def record_preference(self, test_result, preference, reason):
        """Record user preference from A/B test"""
        self.test_history.append({
            'test': test_result,
            'preference': preference,
            'reason': reason,
            'timestamp': datetime.now()
        })
    
    def get_statistics(self):
        """Calculate A/B test statistics"""
        # Calculate win rates, preferences, etc.
        pass
```

## API Integration

### Semantic Scholar API

```python
import requests

def get_paper_recommendations(paper_id):
    """Get recommendations from Semantic Scholar"""
    url = f"https://api.semanticscholar.org/recommendations/v1/papers/{paper_id}"
    params = {
        'limit': 10,
        'fields': 'title,authors,year,citationCount,abstract,url'
    }
    response = requests.get(url, params=params)
    return response.json()
```

### OpenAI API

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def analyze_with_openai(paper_text, prompt):
    """Analyze paper using OpenAI"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": paper_text}
        ]
    )
    return response.choices[0].message.content
```

### Anthropic API

```python
import anthropic

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def analyze_with_anthropic(paper_text, prompt):
    """Analyze paper using Anthropic"""
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        system=prompt,
        messages=[
            {"role": "user", "content": paper_text}
        ]
    )
    return response.content[0].text
```

## Database Schema

### Reading List Structure

```json
{
  "user_id": {
    "papers": [
      {
        "title": "Paper Title",
        "authors": ["Author 1", "Author 2"],
        "year": 2023,
        "url": "https://...",
        "citation_count": 150,
        "added_date": "2024-01-15",
        "priority": "High",
        "status": "unread"
      }
    ]
  }
}
```

### Notes Structure

```json
{
  "user_id_paper_id": {
    "content": "Note content",
    "created_date": "2024-01-15",
    "updated_date": "2024-01-16"
  }
}
```

### A/B Test Structure

```json
{
  "tests": [
    {
      "test_id": "test_001",
      "paper_data": {...},
      "model_a": "gpt-4o-mini",
      "model_b": "claude-3-haiku",
      "result_a": {...},
      "result_b": {...},
      "preference": "model_a",
      "reason": "More detailed analysis",
      "timestamp": "2024-01-15T10:30:00"
    }
  ]
}
```

## Testing Guide

### Unit Tests

```python
import unittest
from app import ModelConfig, DataManager

class TestModelConfig(unittest.TestCase):
    def setUp(self):
        self.model_config = ModelConfig()
    
    def test_get_available_models(self):
        models = self.model_config.get_available_models()
        self.assertIsInstance(models, dict)
        self.assertGreater(len(models), 0)
    
    def test_get_models_by_capability(self):
        models = self.model_config.get_models_by_capability('basic_analysis')
        self.assertGreater(len(models), 0)

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
    
    def test_add_to_reading_list(self):
        paper = {"title": "Test Paper", "year": 2023}
        self.data_manager.add_to_reading_list("user1", paper)
        reading_list = self.data_manager.get_reading_list("user1")
        self.assertEqual(len(reading_list), 1)
```

### Integration Tests

```python
def test_semantic_scholar_api():
    """Test Semantic Scholar API integration"""
    response = get_paper_recommendations("10.1109/5.771073")
    assert 'recommendedPapers' in response
    assert len(response['recommendedPapers']) > 0
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_model_config.py

# Run with coverage
python -m pytest --cov=. tests/
```

## Deployment

### Hugging Face Spaces

1. **Connect repository to Hugging Face**
```bash
git remote add hf https://huggingface.co/spaces/nellaivijay/research-assistant
```

2. **Push to Hugging Face**
```bash
git push hf main
```

3. **Configure Space**
- Set SDK to Gradio
- Set Python version to 3.10
- Add secrets for API keys

### GitHub Actions

The CI/CD pipeline automatically:
- Runs syntax checks
- Installs dependencies
- Runs basic tests
- Deploys to Hugging Face on success

### Manual Deployment

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

## Contributing

### Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions
- Keep functions focused and small

### Commit Messages

```
type(scope): subject

body

footer
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build process or tools

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit pull request

### Adding New Features

1. Update relevant components
2. Add tests for new functionality
3. Update documentation
4. Test thoroughly
5. Submit pull request

---

**For more information, visit the [GitHub Repository](https://github.com/nellaivijay/research-assistant)**