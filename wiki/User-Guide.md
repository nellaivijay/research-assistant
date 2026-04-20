# User Guide

Complete user manual for the Enhanced Research Assistant application.

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Interface Overview](#interface-overview)
3. [Paper Recommendations](#paper-recommendations)
4. [Reading List Management](#reading-list-management)
5. [Notes and Annotations](#notes-and-annotations)
6. [Citation Analysis](#citation-analysis)
7. [Export Functionality](#export-functionality)
8. [AI Model Selection](#ai-model-selection)
9. [Model Comparison](#model-comparison)
10. [Batch Processing](#batch-processing)
11. [Custom Prompts](#custom-prompts)
12. [Auto Model Selection](#auto-model-selection)
13. [A/B Testing](#ab-testing)
14. [Tips and Best Practices](#tips-and-best-practices)
15. [Troubleshooting](#troubleshooting)

## Introduction

The Enhanced Research Assistant is a comprehensive tool for academic researchers that combines paper discovery, AI-powered analysis, and workflow management in a single interface.

### Key Benefits
- **Save Time**: AI-powered analysis reduces manual literature review time
- **Stay Organized**: Built-in reading lists and note-taking
- **Make Informed Decisions**: A/B testing helps choose the best AI models
- **Cost Effective**: Smart model selection optimizes API costs
- **Collaborate Easily**: Multiple export formats for sharing

## Interface Overview

The application is organized into 11 tabs, each dedicated to a specific function:

### Navigation Tabs
1. **🔍 Paper Recommendations** - Discover related papers
2. **📖 Reading List** - Manage your reading queue
3. **📝 Notes & Annotations** - Take notes on papers
4. **📊 Citation Analysis** - Analyze citation metrics
5. **📤 Export** - Export your data
6. **🤖 Model Selection** - Configure AI models
7. **⚖️ Model Comparison** - Compare models side-by-side
8. **📦 Batch Processing** - Analyze multiple papers
9. **✏️ Custom Prompts** - Create custom analysis prompts
10. **🎯 Auto Model Selection** - Automatic model optimization
11. **🧪 A/B Testing** - Compare model performance

## Paper Recommendations

### How to Use

1. **Navigate** to the "🔍 Paper Recommendations" tab
2. **Enter** a paper ID or URL in the input field
3. **Click** "Get Recommendations" button
4. **Review** the recommended papers
5. **Add** interesting papers to your reading list

### Supported Input Formats

- **Semantic Scholar ID**: `10.1109/5.771073`
- **arXiv ID**: `2301.07041`
- **DOI**: `10.1038/nature12373`
- **URL**: Full paper URL from supported sources

### Understanding Results

Each recommended paper shows:
- **Title**: Paper title
- **Authors**: Author list
- **Year**: Publication year
- **Citations**: Number of citations
- **Venue**: Publication venue
- **Abstract**: Brief summary
- **Relevance Score**: How relevant to the input paper

## Reading List Management

### Adding Papers

1. **Search** for papers using recommendations
2. **Click** "Add to Reading List" button
3. **Enter** your user ID
4. **Set** priority level (optional)

### Viewing Reading List

1. **Navigate** to "📖 Reading List" tab
2. **Enter** your user ID
3. **Click** "View Reading List"

### Managing Papers

- **Remove papers**: Click remove button next to each paper
- **Update progress**: Mark papers as read/in progress
- **Set priorities**: High, Medium, Low
- **Add notes**: Link to notes from reading list

## Notes and Annotations

### Creating Notes

1. **Navigate** to "📝 Notes & Annotations" tab
2. **Enter** user ID and paper ID
3. **Write** your notes in the text area
4. **Click** "Save Note"

### Loading Notes

1. **Enter** user ID and paper ID
2. **Click** "Load Note"
3. **View** existing notes

### Best Practices

- **Be specific**: Reference specific sections or findings
- **Add context**: Explain why something is important
- **Use formatting**: Use markdown for structure
- **Link to papers**: Note which paper each note relates to

## Citation Analysis

### Analyzing Citations

1. **Navigate** to "📊 Citation Analysis" tab
2. **Enter** paper ID or URL
3. **Click** "Analyze Citations"

### Metrics Provided

- **Total Citations**: Overall citation count
- **Citation Velocity**: Rate of recent citations
- **Impact Score**: Composite impact metric
- **Field Comparison**: Compared to field average
- **Trend Analysis**: Citation trends over time

### Using Citation Data

- **Identify influential papers**: High citation counts
- **Discover emerging work**: High citation velocity
- **Assess impact**: Impact scores and trends
- **Find related work**: Citation network analysis

## Export Functionality

### Export Formats

1. **Navigate** to "📤 Export" tab
2. **Enter** your user ID
3. **Select** export format:
   - **Markdown**: Human-readable format
   - **JSON**: Machine-readable format
   - **BibTeX**: Academic citation format
4. **Click** "Export Reading List"

### Format Details

#### Markdown
```markdown
# Reading List

## Paper Title (2023)
- URL: https://...
- Added: 2024-01-15
- Priority: High
```

#### JSON
```json
[
  {
    "title": "Paper Title",
    "year": 2023,
    "url": "https://...",
    "priority": "High"
  }
]
```

#### BibTeX
```bibtex
@article{paper0_2023,
  title = {Paper Title},
  year = {2023},
  url = {https://...}
}
```

## AI Model Selection

### Available Models

#### Free Models
- **Rule-Based Analysis**: No API cost, basic analysis
- **Hugging Face Models**: Mistral 7B, Llama 3 8B, Gemma 7B
- **Ollama Models**: Local inference, Llama 3, Mistral, Mixtral

#### Paid Models
- **OpenAI**: GPT-4o Mini (Low cost), GPT-4o (High quality)
- **Anthropic**: Claude 3 Haiku (Fast), Claude 3 Sonnet (Balanced)
- **Google**: Gemini Pro (Standard), Gemini 1.5 Pro (Advanced)

### Setting Up API Keys

1. **Navigate** to "🤖 Model Selection" tab
2. **Select** service from dropdown
3. **Enter** API key in password field
4. **Click** "Save API Key"
5. **Verify** key is saved successfully

### Getting API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google**: https://makersuite.google.com/app/apikey

## Model Comparison

### Running Comparison

1. **Navigate** to "⚖️ Model Comparison" tab
2. **Enter** paper details in JSON format
3. **Select** two models to compare
4. **Choose** analysis type
5. **Click** "Compare Models"

### Understanding Results

- **Quality Scores**: 1-10 scale for each model
- **Cost Analysis**: Estimated cost for each model
- **Response Time**: How long each model took
- **Content Preview**: Sample of each analysis

### Making Decisions

Use comparison data to:
- Choose cost-effective options
- Select highest quality results
- Balance speed and accuracy
- Identify best models for your use case

## Batch Processing

### Processing Multiple Papers

1. **Navigate** to "📦 Batch Processing" tab
2. **Enter** papers as JSON array
3. **Select** model for analysis
4. **Click** "Process Batch"

### JSON Format

```json
[
  {
    "title": "Paper 1",
    "abstract": "...",
    "year": "2023"
  },
  {
    "title": "Paper 2",
    "abstract": "...",
    "year": "2023"
  }
]
```

### Benefits

- **Time Savings**: Process multiple papers at once
- **Consistency**: Same model for all papers
- **Efficiency**: Reduced API overhead
- **Organization**: Easy to review results

## Custom Prompts

### Creating Custom Prompts

1. **Navigate** to "✏️ Custom Prompts" tab
2. **Enter** prompt name
3. **Write** your custom prompt
4. **Click** "Save Prompt"

### Using Custom Prompts

1. **Select** from existing prompts dropdown
2. **Enter** paper details
3. **Choose** model
4. **Click** "Analyze with Custom Prompt"

### Prompt Tips

- **Be specific**: Clearly state what you want
- **Include context**: Provide relevant background
- **Define output**: Specify desired format
- **Test iteratively**: Refine based on results

## Auto Model Selection

### How It Works

The system automatically selects models based on:

- **Paper Complexity**: Basic, Advanced, Expert
- **Budget Preference**: Free, Balanced, Quality
- **Required Capabilities**: Analysis type needed

### Using Auto Selection

1. **Navigate** to "🎯 Auto Model Selection" tab
2. **Enter** paper details
3. **Select** budget preference
4. **Choose** analysis type
5. **Click** "Auto Select and Analyze"

### Complexity Levels

- **Basic**: Short papers, simple topics
- **Advanced**: Technical papers, specialized topics
- **Expert**: Highly technical, cutting-edge research

## A/B Testing

### Running A/B Tests

1. **Navigate** to "🧪 A/B Testing" tab
2. **Enter** paper details in JSON format
3. **Select** Model A and Model B
4. **Choose** analysis type
5. **Click** "Run A/B Test"

### Recording Preferences

1. **Review** both model outputs
2. **Select** preferred model (A, B, or Tie)
3. **Enter** reason for preference
4. **Click** "Record Preference"

### Viewing Statistics

1. **Click** "View A/B Test Statistics"
2. **Review**:
   - Total tests run
   - Win rates for each model
   - Personalized recommendations

### Using Results

- **Identify best models**: High win rates
- **Optimize costs**: Balance quality and cost
- **Personalize**: System learns your preferences
- **Make decisions**: Data-driven model selection

## Tips and Best Practices

### Paper Discovery
- Start with well-known papers for better recommendations
- Use multiple seed papers for diverse results
- Check citation counts for impact assessment
- Review abstracts before adding to reading list

### AI Analysis
- Start with free models to test features
- Use A/B testing to find preferred models
- Custom prompts work best for specific needs
- Batch processing saves time with multiple papers

### Cost Optimization
- Use free models when quality is acceptable
- Enable auto-selection for budget optimization
- Batch processing reduces API overhead
- Cache results when possible

### Workflow Management
- Organize reading list by project or topic
- Add detailed notes for future reference
- Use progress tracking to manage workload
- Export regularly for backup

## Troubleshooting

### Common Issues

**No recommendations found**
- Try a different paper ID or URL
- Check that the paper exists in the database
- Use a more well-known paper as seed

**AI analysis not working**
- Verify API keys are correctly saved
- Check your API credits/balance
- Try a different model or service
- Use rule-based analysis as fallback

**Export format issues**
- Ensure you have papers in your reading list
- Check the selected export format
- Try a different format if needed

**A/B testing not recording**
- Verify both models completed successfully
- Check that you selected a preference
- Ensure reason field is filled
- Try running the test again

### Getting Help

- Check the [GitHub Wiki](https://github.com/nellaivijay/research-assistant/wiki) for more documentation
- Open an issue on GitHub for bugs
- Contact maintainers for support

---

**For more information, visit the [GitHub Repository](https://github.com/nellaivijay/research-assistant)**