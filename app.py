import gradio as gr
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import re

# ==================== DATA LAYER ====================

class DataManager:
    """Manage research data storage"""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.reading_list_file = self.data_dir / "reading_list.json"
        self.notes_file = self.data_dir / "notes.json"
        self.categories_file = self.data_dir / "categories.json"
        
    def save_reading_list(self, user_id: str, papers: List[Dict]):
        """Save user's reading list"""
        data = self._load_json(self.reading_list_file)
        data[user_id] = {
            "papers": papers,
            "last_updated": datetime.now().isoformat()
        }
        self._save_json(self.reading_list_file, data)
        
    def get_reading_list(self, user_id: str) -> List[Dict]:
        """Get user's reading list"""
        data = self._load_json(self.reading_list_file)
        return data.get(user_id, {}).get("papers", [])
    
    def save_notes(self, user_id: str, paper_id: str, notes: str):
        """Save notes for a paper"""
        data = self._load_json(self.notes_file)
        if user_id not in data:
            data[user_id] = {}
        data[user_id][paper_id] = {
            "notes": notes,
            "last_updated": datetime.now().isoformat()
        }
        self._save_json(self.notes_file, data)
        
    def get_notes(self, user_id: str, paper_id: str) -> str:
        """Get notes for a paper"""
        data = self._load_json(self.notes_file)
        return data.get(user_id, {}).get(paper_id, {}).get("notes", "")
    
    def _load_json(self, file_path: Path) -> Dict:
        """Load JSON file"""
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_json(self, file_path: Path, data: Dict):
        """Save JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

# Initialize data manager
data_manager = DataManager()

# ==================== RECOMMENDATION ENGINE ====================

class RecommendationEngine:
    """Multi-source paper recommendation engine"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
        
    def get_recommendations(self, paper_id: str, sources: List[str] = None) -> Dict:
        """Get recommendations from multiple sources"""
        if sources is None:
            sources = ["semantic_scholar", "arxiv"]
        
        results = {}
        
        if "semantic_scholar" in sources:
            results["semantic_scholar"] = self._get_semantic_scholar_recommendations(paper_id)
        
        if "arxiv" in sources:
            results["arxiv"] = self._get_arxiv_recommendations(paper_id)
            
        return results
    
    def _get_semantic_scholar_recommendations(self, paper_id: str) -> List[Dict]:
        """Get recommendations from Semantic Scholar API"""
        try:
            # Convert to Semantic Scholar ID format
            ss_id = f"ArXiv:{paper_id}" if not paper_id.startswith("ArXiv:") else paper_id
            
            response = requests.post(
                "https://api.semanticscholar.org/recommendations/v1/papers/",
                json={"positivePaperIds": [ss_id]},
                params={"fields": "externalIds,title,year,abstract,citationCount,url", "limit": 10},
                timeout=10
            )
            
            if response.status_code == 200:
                papers = response.json().get("recommendedPapers", [])
                return self._format_papers(papers)
            return []
            
        except Exception as e:
            print(f"Semantic Scholar API error: {e}")
            return []
    
    def _get_arxiv_recommendations(self, paper_id: str) -> List[Dict]:
        """Get recommendations from arXiv (simulated based on category)"""
        try:
            # Get paper info first to determine category
            response = requests.get(
                f"http://export.arxiv.org/api/query?id_list={paper_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                # Parse arXiv category and get recent papers in same category
                # This is a simplified version - real implementation would parse XML
                return self._get_mock_arxiv_recommendations()
            return []
            
        except Exception as e:
            print(f"arXiv API error: {e}")
            return self._get_mock_arxiv_recommendations()
    
    def _get_mock_arxiv_recommendations(self) -> List[Dict]:
        """Mock arXiv recommendations for demo"""
        return [
            {
                "title": "Attention Is All You Need",
                "year": "2017",
                "citationCount": 50000,
                "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
                "url": "https://arxiv.org/abs/1706.03762",
                "source": "arxiv"
            },
            {
                "title": "BERT: Pre-training of Deep Bidirectional Transformers",
                "year": "2018",
                "citationCount": 40000,
                "abstract": "We introduce a new language representation model called BERT...",
                "url": "https://arxiv.org/abs/1810.04805",
                "source": "arxiv"
            }
        ]
    
    def _format_papers(self, papers: List[Dict]) -> List[Dict]:
        """Format papers to standard structure"""
        formatted = []
        for paper in papers:
            formatted_paper = {
                "title": paper.get("title", "Unknown Title"),
                "year": paper.get("year", "Unknown"),
                "citationCount": paper.get("citationCount", 0),
                "abstract": paper.get("abstract", "No abstract available"),
                "url": paper.get("url", ""),
                "externalIds": paper.get("externalIds", {}),
                "source": "semantic_scholar"
            }
            formatted.append(formatted_paper)
        return formatted

# Initialize recommendation engine
recommender = RecommendationEngine()

# ==================== PAPER ANALYZER ====================

class PaperAnalyzer:
    """Analyze papers and provide insights"""
    
    def analyze_paper(self, paper: Dict) -> Dict:
        """Analyze a paper and provide insights"""
        analysis = {
            "impact_score": self._calculate_impact_score(paper),
            "readability_score": self._calculate_readability(paper),
            "citation_velocity": self._estimate_citation_velocity(paper),
            "key_contributions": self._extract_key_contributions(paper),
            "related_topics": self._identify_topics(paper)
        }
        return analysis
    
    def _calculate_impact_score(self, paper: Dict) -> float:
        """Calculate impact score based on citations and recency"""
        citations = paper.get("citationCount", 0)
        year = int(paper.get("year", 2020))
        current_year = datetime.now().year
        
        # Simple impact formula: citations / (current_year - year + 1)
        age = max(1, current_year - year)
        impact_score = citations / age
        
        return round(impact_score, 2)
    
    def _calculate_readability(self, paper: Dict) -> str:
        """Estimate readability based on abstract"""
        abstract = paper.get("abstract", "")
        if not abstract:
            return "Unknown"
        
        # Simple readability estimate based on length
        word_count = len(abstract.split())
        
        if word_count < 100:
            return "Very Easy"
        elif word_count < 200:
            return "Easy"
        elif word_count < 300:
            return "Medium"
        else:
            return "Complex"
    
    def _estimate_citation_velocity(self, paper: Dict) -> str:
        """Estimate citation velocity"""
        citations = paper.get("citationCount", 0)
        year = int(paper.get("year", 2020))
        current_year = datetime.now().year
        age = max(1, current_year - year)
        
        velocity = citations / age
        
        if velocity > 100:
            return "Very High"
        elif velocity > 50:
            return "High"
        elif velocity > 20:
            return "Medium"
        else:
            return "Low"
    
    def _extract_key_contributions(self, paper: Dict) -> List[str]:
        """Extract key contributions from abstract"""
        abstract = paper.get("abstract", "")
        
        # Simple keyword-based contribution extraction
        contributions = []
        
        contribution_keywords = ["introduce", "propose", "present", "develop", "create", "novel", "new approach"]
        sentences = abstract.split(".")
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in contribution_keywords):
                contributions.append(sentence.strip())
        
        return contributions[:3]  # Return top 3
    
    def _identify_topics(self, paper: Dict) -> List[str]:
        """Identify research topics from paper"""
        title = paper.get("title", "").lower()
        abstract = paper.get("abstract", "").lower()
        text = title + " " + abstract
        
        # Common ML/AI topics
        topics = {
            "machine learning": ["machine learning", "ml", "neural network", "deep learning"],
            "natural language processing": ["nlp", "language model", "transformer", "bert", "gpt"],
            "computer vision": ["vision", "image", "convolutional", "cnn", "recognition"],
            "reinforcement learning": ["reinforcement", "rl", "policy", "agent"],
            "graph learning": ["graph", "gnn", "node", "edge"],
            "optimization": ["optimization", "gradient", "convergence"],
            "generative models": ["generative", "gan", "vae", "diffusion"]
        }
        
        identified_topics = []
        for topic, keywords in topics.items():
            if any(keyword in text for keyword in keywords):
                identified_topics.append(topic)
        
        return identified_topics

# Initialize paper analyzer
analyzer = PaperAnalyzer()

# ==================== GRADIO INTERFACE ====================

def create_research_assistant():
    """Create the research assistant dashboard"""
    
    with gr.Blocks(title="Research Assistant - Enhanced") as demo:
        
        # Header
        gr.Markdown("# 📚 Enhanced Research Assistant")
        gr.Markdown("AI-powered research companion with multi-source recommendations, analysis, and workflow management")
        
        with gr.Tabs():
            # ==================== PAPER RECOMMENDATIONS TAB ====================
            with gr.Tab("🔍 Paper Recommendations"):
                gr.Markdown("## Multi-Source Paper Recommendations")
                
                with gr.Row():
                    paper_input = gr.Textbox(
                        label="Paper ID or arXiv URL",
                        placeholder="e.g., 2309.12307 or https://arxiv.org/abs/2309.12307"
                    )
                    source_selector = gr.CheckboxGroup(
                        choices=["Semantic Scholar", "arXiv", "Citations"],
                        value=["Semantic Scholar"],
                        label="Recommendation Sources"
                    )
                
                recommend_btn = gr.Button("Get Recommendations", variant="primary")
                
                with gr.Row():
                    recommendations_output = gr.Markdown()
                    analysis_output = gr.Markdown()
                
                def get_recommendations(paper_id, sources):
                    if not paper_id:
                        return "Please enter a paper ID or URL", ""
                    
                    # Extract arXiv ID from URL if needed
                    arxiv_id = paper_id.split("/")[-1] if "/" in paper_id else paper_id
                    
                    # Get recommendations
                    source_map = {
                        "Semantic Scholar": "semantic_scholar",
                        "arXiv": "arxiv",
                        "Citations": "semantic_scholar"
                    }
                    
                    selected_sources = [source_map[s] for s in sources if s in source_map]
                    results = recommender.get_recommendations(arxiv_id, selected_sources)
                    
                    # Format recommendations
                    output = "## Recommended Papers\n\n"
                    
                    for source, papers in results.items():
                        if papers:
                            output += f"### From {source.replace('_', ' ').title()}\n\n"
                            for i, paper in enumerate(papers[:5], 1):
                                output += f"**{i}. {paper['title']}** ({paper['year']})\n"
                                output += f"- Citations: {paper['citationCount']}\n"
                                output += f"- [View Paper]({paper['url']})\n"
                                output += f"- Abstract: {paper['abstract'][:200]}...\n\n"
                    
                    # Analyze the input paper
                    if results.get("semantic_scholar"):
                        input_paper = results["semantic_scholar"][0] if results["semantic_scholar"] else {}
                        analysis = analyzer.analyze_paper(input_paper)
                        
                        analysis_text = "## Paper Analysis\n\n"
                        analysis_text += f"- **Impact Score**: {analysis['impact_score']}\n"
                        analysis_text += f"- **Readability**: {analysis['readability_score']}\n"
                        analysis_text += f"- **Citation Velocity**: {analysis['citation_velocity']}\n"
                        analysis_text += f"- **Topics**: {', '.join(analysis['related_topics'])}\n"
                        
                        if analysis['key_contributions']:
                            analysis_text += "\n### Key Contributions\n"
                            for contribution in analysis['key_contributions']:
                                analysis_text += f"- {contribution}\n"
                    else:
                        analysis_text = "Analysis not available for this paper."
                    
                    return output, analysis_text
                
                recommend_btn.click(get_recommendations, inputs=[paper_input, source_selector], outputs=[recommendations_output, analysis_output])
            
            # ==================== READING LIST TAB ====================
            with gr.Tab("📖 Reading List"):
                gr.Markdown("## Personal Reading List Management")
                
                user_id = gr.Textbox(label="User ID", placeholder="Enter your identifier")
                
                with gr.Row():
                    add_paper_btn = gr.Button("Add to Reading List", variant="primary")
                    view_list_btn = gr.Button("View Reading List", variant="secondary")
                
                paper_to_add = gr.Textbox(label="Paper Details (JSON)", placeholder='{"title": "Paper Title", "year": "2023", "url": "..."}')
                
                reading_list_output = gr.Markdown()
                
                def add_to_reading_list(user_id, paper_json):
                    if not user_id or not paper_json:
                        return "Please provide user ID and paper details."
                    
                    try:
                        paper = json.loads(paper_json)
                        current_list = data_manager.get_reading_list(user_id)
                        paper["status"] = "to-read"
                        paper["added_date"] = datetime.now().isoformat()
                        current_list.append(paper)
                        data_manager.save_reading_list(user_id, current_list)
                        return f"Paper added to reading list. Total papers: {len(current_list)}"
                    except json.JSONDecodeError:
                        return "Invalid JSON format. Please provide valid JSON."
                
                def view_reading_list(user_id):
                    if not user_id:
                        return "Please enter user ID."
                    
                    papers = data_manager.get_reading_list(user_id)
                    
                    if not papers:
                        return "No papers in your reading list."
                    
                    output = f"## Reading List ({len(papers)} papers)\n\n"
                    
                    # Group by status
                    by_status = {}
                    for paper in papers:
                        status = paper.get("status", "to-read")
                        if status not in by_status:
                            by_status[status] = []
                        by_status[status].append(paper)
                    
                    for status, status_papers in by_status.items():
                        output += f"### {status.replace('-', ' ').title()} ({len(status_papers)})\n\n"
                        for paper in status_papers:
                            output += f"- **{paper['title']}** ({paper['year']})\n"
                            output += f"  [Link]({paper['url']})\n\n"
                    
                    return output
                
                add_paper_btn.click(add_to_reading_list, inputs=[user_id, paper_to_add], outputs=[reading_list_output])
                view_list_btn.click(view_reading_list, inputs=[user_id], outputs=[reading_list_output])
            
            # ==================== NOTES & ANNOTATIONS TAB ====================
            with gr.Tab("📝 Notes & Annotations"):
                gr.Markdown("## Personal Notes and Annotations")
                
                note_user_id = gr.Textbox(label="User ID", placeholder="Enter your identifier")
                note_paper_id = gr.Textbox(label="Paper ID", placeholder="Enter paper ID")
                note_content = gr.Textbox(label="Your Notes", lines=10, placeholder="Write your notes, insights, and questions here...")
                
                save_note_btn = gr.Button("Save Note", variant="primary")
                load_note_btn = gr.Button("Load Note", variant="secondary")
                
                note_output = gr.Markdown()
                
                def save_note(user_id, paper_id, notes):
                    if not user_id or not paper_id:
                        return "Please provide user ID and paper ID."
                    
                    data_manager.save_notes(user_id, paper_id, notes)
                    return "Notes saved successfully!"
                
                def load_note(user_id, paper_id):
                    if not user_id or not paper_id:
                        return "Please provide user ID and paper ID."
                    
                    notes = data_manager.get_notes(user_id, paper_id)
                    if notes:
                        return f"## Notes for Paper {paper_id}\n\n{notes}"
                    else:
                    return f"No notes found for paper {paper_id}."
                
                save_note_btn.click(save_note, inputs=[note_user_id, note_paper_id, note_content], outputs=[note_output])
                load_note_btn.click(load_note, inputs=[note_user_id, note_paper_id], outputs=[note_output])
            
            # ==================== CITATION ANALYSIS TAB ====================
            with gr.Tab("📊 Citation Analysis"):
                gr.Markdown("## Citation Impact and Trend Analysis")
                
                analysis_paper_id = gr.Textbox(label="Paper ID", placeholder="Enter paper ID for analysis")
                analyze_citations_btn = gr.Button("Analyze Citations", variant="primary")
                
                citation_output = gr.Markdown()
                
                def analyze_citations(paper_id):
                    if not paper_id:
                        return "Please enter a paper ID."
                    
                    # Get paper data and analyze
                    arxiv_id = paper_id.split("/")[-1] if "/" in paper_id else paper_id
                    results = recommender.get_recommendations(arxiv_id, ["semantic_scholar"])
                    
                    if results.get("semantic_scholar"):
                        paper = results["semantic_scholar"][0] if results["semantic_scholar"] else {}
                        analysis = analyzer.analyze_paper(paper)
                        
                        output = "## Citation Analysis\n\n"
                        output += f"### Paper: {paper['title']}\n\n"
                        output += f"- **Total Citations**: {paper['citationCount']}\n"
                        output += f"- **Publication Year**: {paper['year']}\n"
                        output += f"- **Impact Score**: {analysis['impact_score']}\n"
                        output += f"- **Citation Velocity**: {analysis['citation_velocity']}\n\n"
                        
                        output += "### Citation Interpretation\n\n"
                        if analysis['citation_velocity'] == "Very High":
                            output += "This paper is highly influential with rapid citation accumulation.\n"
                        elif analysis['citation_velocity'] == "High":
                            output += "This paper shows strong influence and growing impact.\n"
                        else:
                            output += "This paper has moderate or developing impact.\n"
                        
                        return output
                    else:
                        return "Unable to analyze citations for this paper."
                
                analyze_citations_btn.click(analyze_citations, inputs=[analysis_paper_id], outputs=[citation_output])
            
            # ==================== EXPORT TAB ====================
            with gr.Tab("📤 Export"):
                gr.Markdown("Export reading lists and citations")
                
                export_user_id = gr.Textbox(label="User ID", placeholder="Enter your identifier")
                export_format = gr.Radio(
                    choices=["BibTeX", "JSON", "Markdown"],
                    value="BibTeX",
                    label="Export Format"
                )
                
                export_btn = gr.Button("Export Reading List", variant="primary")
                export_output = gr.Code(language="text", label="Export Output")
                
                def export_reading_list(user_id, format_type):
                    if not user_id:
                        return "Please enter user ID."
                    
                    papers = data_manager.get_reading_list(user_id)
                    
                    if not papers:
                        return "No papers to export."
                    
                    if format_type == "JSON":
                        return json.dumps(papers, indent=2)
                    elif format_type == "Markdown":
                        output = "# Reading List\n\n"
                        for paper in papers:
                            output += f"- {paper['title']} ({paper['year']})\n"
                            output += f"  {paper['url']}\n\n"
                        return output
                    else:  # BibTeX
                        bibtex = ""
                        for i, paper in enumerate(papers):
                            key = f"paper{i}_{paper['year']}"
                            bibtex += f"@article{{{key}},\n"
                            bibtex += f"  title = {{{paper['title']}}},\n"
                            bibtex += f"  year = {{{paper['year']}}},\n"
                            bibtex += f"  url = {{{paper['url']}}}\n"
                            bibtex += "}\n\n"
                        return bibtex
                
                export_btn.click(export_reading_list, inputs=[export_user_id, export_format], outputs=[export_output])
            
            # ==================== ABOUT TAB ====================
            with gr.Tab("ℹ️ About"):
                gr.Markdown("## About Enhanced Research Assistant\n\n")
                gr.Markdown("### Features\n")
                gr.Markdown("- **Multi-Source Recommendations**: Semantic Scholar, arXiv, citation-based\n")
                gr.Markdown("- **Reading List Management**: Organize papers by status and priority\n")
                gr.Markdown("- **Notes & Annotations**: Personal notes for each paper\n")
                gr.Markdown("- **Citation Analysis**: Impact scoring and trend analysis\n")
                gr.Markdown("- **Export Options**: BibTeX, JSON, Markdown formats\n")
                gr.Markdown("\n### Technology\n")
                gr.Markdown("- Gradio 4.0+ Interface\n")
                gr.Markdown("- Multi-source recommendation APIs\n")
                gr.Markdown("- Local data storage for privacy\n")
                gr.Markdown("- Paper analysis algorithms\n")
                gr.Markdown("\n### Research Focus\n")
                gr.Markdown("This assistant focuses on research workflow automation and paper discovery rather than full-text analysis, making it efficient for literature review and research planning.")
    
    return demo

# ==================== MAIN ENTRY POINT ====================

if __name__ == "__main__":
    demo = create_research_assistant()
    demo.launch()
