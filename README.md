---
title: Enhanced Research Assistant
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
python_version: "3.10"
app_file: app.py
pinned: false
license: mit
---

# 📚 Enhanced Research Assistant - AI Model Selection

[![CI/CD Pipeline](https://github.com/nellaivijay/research-assistant/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/nellaivijay/research-assistant/actions/workflows/ci-cd.yml)
[![Gradio](https://img.shields.io/badge/Gradio-4.0.0-orange)](https://gradio.app)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://python.org)
[![Hugging Face Spaces](https://img.shields.io/badge/Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/nellaivijay/research-assistant)

**🚀 Live Application:** [https://huggingface.co/spaces/nellaivijay/research-assistant](https://huggingface.co/spaces/nellaivijay/research-assistant)

AI-powered research companion with custom AI model selection, multi-source recommendations, analysis, and workflow management. An enhanced version of paper recommendation systems with comprehensive research workflow features and optional AI-powered analysis.

## 🎓 Educational Purpose

This project is created for **educational purposes only** to demonstrate:
- AI model integration and comparison
- Research workflow automation
- Modern web application development
- CI/CD pipeline implementation
- Documentation and SEO best practices

The system is designed to help researchers and students learn about AI-powered research tools and modern software development practices.

## 🎯 Key Features

### 🤖 AI Model Selection (NEW!)
- **15+ AI Models**: Rule-based, OpenAI, Anthropic, Google, Ollama (local), Hugging Face (free)
- **Cost Control**: Select free (rule-based, local, HF) or paid AI models as needed
- **API Key Management**: Secure local storage of API keys
- **Model Comparison**: Compare analysis results across different models
- **Flexible Analysis**: Switch between basic and advanced analysis
- **Local Models**: Use Ollama for free local inference (Llama 3, Mistral, Mixtral)
- **Custom Endpoints**: Bring your own model endpoints

### 🔍 Multi-Source Recommendations
- **Semantic Scholar**: Citation-based recommendations using academic graph
- **arXiv**: Category-based recommendations from recent preprints
- **Citation Analysis**: Papers that cite similar works
- **Smart Ranking**: Relevance scoring and filtering

### 📖 Reading List Management
- **Status Tracking**: to-read, reading, completed categories
- **Personal Organization**: Custom tags and priorities
- **Progress Tracking**: Monitor research progress over time
- **Quick Add**: Easy paper addition with metadata

### 📝 Notes & Annotations
- **Personal Notes**: Add insights and questions for each paper
- **Persistent Storage**: Notes saved locally for privacy
- **Quick Access**: Load notes by paper ID
- **Research Journal**: Build personal knowledge base

### 📊 Citation Analysis
- **Impact Scoring**: Calculate paper influence metrics
- **Citation Velocity**: Track how quickly papers gain citations
- **Readability Assessment**: Estimate paper complexity
- **Topic Identification**: Auto-detect research topics
- **Key Contributions**: Extract main contributions from abstracts

### 📤 Export Options
- **BibTeX**: Direct export for LaTeX/Overleaf
- **JSON**: Structured data for further processing
- **Markdown**: Human-readable format for sharing
- **Citation Styles**: Multiple format options

### ⚖️ Advanced Features (NEW!)
- **Model Comparison**: Side-by-side analysis comparison across different AI models
- **Batch Processing**: Analyze multiple papers with a single model selection
- **Custom Prompts**: Define and save custom analysis prompts for specific needs
- **Auto Model Selection**: Automatic model selection based on paper complexity
- **Cost Optimization**: Budget-aware model selection (free/balanced/quality)
- **Quality Scoring**: Rate analysis quality per model (1-10 scale)
- **A/B Testing**: Compare model performance on your papers and build preferences

## 🚀 How It Works

### 1. Paper Discovery
Enter a paper ID or arXiv URL to get recommendations from multiple academic sources.

### 2. Analysis & Insights
Get instant analysis of paper impact, readability, and key contributions.

### 3. Personal Organization
Add papers to your reading list, categorize by status, and track progress.

### 4. Knowledge Building
Add personal notes and annotations to build your research knowledge base.

### 5. Export & Share
Export your reading lists in multiple formats for use in other tools.

## 🎨 Dashboard Tabs

### 1. 🤖 Model Selection (NEW!)
- Choose from multiple AI analysis models
- Configure API keys for different services
- View model capabilities and costs
- Switch between free and paid analysis

### 2. 🔍 Paper Recommendations
- Multi-source paper discovery
- Smart ranking and filtering
- Abstract previews
- One-click access to full papers

### 3. 📖 Reading List
- Personal paper organization
- Status-based categorization
- Progress tracking
- Bulk operations

### 4. 📝 Notes & Annotations
- Per-paper note-taking
- Persistent storage
- Quick search and retrieval
- Research journal building

### 5. 📊 Citation Analysis
- Impact metrics
- Trend analysis
- Topic identification
- Contribution extraction

### 6. 📤 Export
- Multiple format support
- Bibliography generation
- Reading list export
- Citation formatting

### 7. ⚖️ Model Comparison (NEW!)
- Side-by-side model comparison
- Quality score comparison
- Cost vs quality analysis
- Performance metrics

### 8. 📦 Batch Processing (NEW!)
- Analyze multiple papers at once
- Single model selection for batch
- Progress tracking
- Results aggregation

### 9. ✏️ Custom Prompts (NEW!)
- Define custom analysis prompts
- Save and reuse prompts
- Pre-built prompt templates
- Specialized analysis workflows

### 10. 🎯 Auto Model Selection (NEW!)
- Automatic model selection based on complexity
- Budget preference settings (free/balanced/quality)
- Smart cost optimization
- Quality-aware recommendations

### 11. 🧪 A/B Testing (NEW!)
- Run A/B tests between any two models
- Record your preferences and reasons
- Build statistics on model performance
- Get personalized model recommendations
- Track win rates over time

## 🤖 Available AI Models

### Free Models
- **Rule-Based Analysis**: Pattern matching and keyword extraction (no API needed)
- **Hugging Face Inference**: Mistral 7B, Llama 3 8B, Gemma 7B (free HF API)
- **Ollama Local Models**: Llama 3, Llama 3 70B, Mistral, Mixtral (requires Ollama)

### Paid Models (Optional)
- **OpenAI**: GPT-4o Mini (low cost), GPT-4o (medium cost)
- **Anthropic**: Claude 3 Haiku (low cost), Claude 3 Sonnet (medium cost)
- **Google**: Gemini Pro (low cost), Gemini 1.5 Pro (medium cost)

### Custom Models
- **Custom Endpoints**: Bring your own model API endpoints

### Model Capabilities
- **Basic Analysis**: Topic identification, citation analysis, readability assessment
- **Advanced Analysis**: Deep insights, summarization, novelty assessment
- **Topic Modeling**: Research theme identification and clustering
- **Comparison Analysis**: Cross-paper comparison and synthesis
- **Synthesis**: Multi-paper synthesis and literature review generation

## 🧠 Research Workflow Integration

This assistant is designed to integrate into your research workflow:

- **Literature Review**: Discover relevant papers quickly
- **Research Planning**: Organize papers by project or topic
- **Knowledge Management**: Build personal research notes
- **Writing Support**: Export citations for papers
- **Progress Tracking**: Monitor reading progress over time

## 🛠️ Technology Stack

- **Frontend**: Gradio 4.0+
- **Recommendations**: Semantic Scholar API, arXiv API
- **AI Models**: Optional OpenAI, Anthropic integration
- **Data Storage**: Local JSON files (privacy-focused)
- **Analysis**: Custom citation and impact algorithms + optional AI analysis
- **Deployment**: Hugging Face Spaces

## 🔒 Privacy & Data

- All personal data stored locally
- No external data sharing
- User-controlled reading lists
- Private notes and annotations
- Optional export for backup

## 📈 Comparison with Basic Recommenders

| Feature | Basic Recommenders | Enhanced Research Assistant |
|---------|-------------------|----------------------------|
| Recommendation Sources | 1-2 sources | Multiple sources with ranking |
| Personal Organization | None | Full reading list management |
| Notes System | None | Per-paper notes system |
| Citation Analysis | Basic count | Impact scoring, velocity, trends |
| Export Options | Limited | BibTeX, JSON, Markdown |
| Research Workflow | Single-purpose | End-to-end workflow support |

## 🎓 Use Cases

- **Academic Researchers**: Literature review and paper discovery
- **Graduate Students**: Thesis research and reading organization
- **Industry Researchers**: Staying current with developments
- **Data Scientists**: ML/AI paper tracking and analysis
- **Research Groups**: Shared reading lists and collaboration

## 🛠️ Development & CI/CD

This project uses GitHub Actions for automated CI/CD pipeline:

- **Automated Testing**: Syntax checks, dependency validation, basic tests
- **Continuous Integration**: Tests run on every push and pull request
- **Automated Deployment**: Auto-deploys to Hugging Face Spaces on successful tests
- **Security Scanning**: Checks for hardcoded credentials and security issues

For detailed GitHub setup instructions, see [GITHUB_SETUP.md](GITHUB_SETUP.md)

## 🚀 Getting Started

### Quick Start
1. **🚀 Try the Live App**: Visit [https://huggingface.co/spaces/nellaivijay/research-assistant](https://huggingface.co/spaces/nellaivijay/research-assistant)
2. **📝 Find Papers**: Enter paper IDs or URLs to get recommendations
3. **🔍 Analyze Impact**: Review citation analysis and impact scores
4. **📖 Build Reading List**: Add relevant papers to your personal list
5. **✏️ Take Notes**: Add insights and annotations as you read
6. **📊 Track Progress**: Monitor your reading progress over time
7. **📤 Export**: Export citations and reading lists as needed

### Local Development
For local development setup, see the [Installation Guide](https://github.com/nellaivijay/research-assistant/wiki/Installation-Guide) in the GitHub Wiki.

## 📝 License

MIT License

## 🤝 Contributing

This is an enhanced version inspired by librarian-bots/recommend_similar_papers, with additional research workflow features and analysis capabilities.
