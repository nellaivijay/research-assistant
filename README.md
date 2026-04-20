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

AI-powered research companion with custom AI model selection, multi-source recommendations, analysis, and workflow management. An enhanced version of paper recommendation systems with comprehensive research workflow features and optional AI-powered analysis.

## 🎯 Key Features

### 🤖 AI Model Selection (NEW!)
- **Multiple AI Models**: Choose from rule-based, OpenAI, Anthropic models
- **Cost Control**: Select free (rule-based) or paid AI models as needed
- **API Key Management**: Secure local storage of API keys
- **Model Comparison**: Compare analysis results across different models
- **Flexible Analysis**: Switch between basic and advanced analysis

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

## 🤖 Available AI Models

### Free Models
- **Rule-Based Analysis**: Pattern matching and keyword extraction (no API needed)

### Paid Models (Optional)
- **GPT-4o Mini**: Fast, efficient analysis (OpenAI API key required)
- **Claude 3 Haiku**: Quick analysis with good quality (Anthropic API key required)

### Model Capabilities
- **Basic Analysis**: Topic identification, citation analysis, readability assessment
- **Advanced Analysis**: Deep insights, summarization, novelty assessment
- **Topic Modeling**: Research theme identification and clustering
- **Comparison Analysis**: Cross-paper comparison and synthesis

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

## 🚀 Getting Started

1. **Find Papers**: Enter paper IDs or URLs to get recommendations
2. **Analyze Impact**: Review citation analysis and impact scores
3. **Build Reading List**: Add relevant papers to your personal list
4. **Take Notes**: Add insights and annotations as you read
5. **Track Progress**: Monitor your reading progress over time
6. **Export**: Export citations and reading lists as needed

## 📝 License

MIT License

## 🤝 Contributing

This is an enhanced version inspired by librarian-bots/recommend_similar_papers, with additional research workflow features and analysis capabilities.
