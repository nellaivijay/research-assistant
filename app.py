import gradio as gr
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import re
import os
from ai_service import ai_manager
from error_handling import error_handler, safe_executor, safe_api_call, validate_json_input, validate_required_fields, UserFriendlyError
from config_manager import config_manager
from data_sources import data_source_manager
from citation_graph import citation_engine, CitationGraphVisualizer
from database import db_manager
from pdf_analysis import pdf_engine

# ==================== MODEL CONFIGURATION ====================

class ModelConfig:
    """Manage AI model configurations using external config file"""
    
    def __init__(self):
        self.models = config_manager.get_enabled_models()
    
    def reload_models(self):
        """Reload models from configuration"""
        self.models = config_manager.get_enabled_models()
    
    def get_available_models(self, capability_filter: str = None, complexity_filter: str = None) -> Dict:
        """Get available models, optionally filtered by capability or complexity"""
        models = self.models
        
        if capability_filter:
            models = {
                k: v for k, v in models.items()
                if capability_filter in v.get("capabilities", [])
            }
        
        if complexity_filter:
            models = {
                k: v for k, v in models.items()
                if v.get("complexity") == complexity_filter
            }
        
        return models
    
    def get_model_info(self, model_id: str) -> Dict:
        """Get information about a specific model"""
        return self.models.get(model_id, {})
    
    def check_api_key(self, model_id: str) -> bool:
        """Check if required API key is available"""
        model = self.models.get(model_id, {})
        api_key_env = model.get("api_key_env")
        
        if not api_key_env:
            return True  # No API key needed (local model)
        
        return bool(os.environ.get(api_key_env))
    
    def check_ollama_available(self) -> bool:
        """Check if Ollama is available locally"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def get_ollama_models(self) -> List[str]:
        """Get available Ollama models"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
        except:
            return []
        return []
    
    def add_custom_model(self, model_id: str, name: str, endpoint: str, capabilities: List[str]) -> bool:
        """Add a custom model endpoint"""
        try:
            self.models[model_id] = {
                "name": name,
                "type": "custom",
                "cost": "Variable",
                "api_endpoint": endpoint,
                "capabilities": capabilities,
                "complexity": "variable",
                "quality_score": 0,
                "requires_endpoint": True
            }
            return True
        except Exception as e:
            print(f"Error adding custom model: {e}")
            return False

model_config = ModelConfig()

# ==================== ADVANCED ANALYSIS FEATURES ====================

class AdvancedAnalysisFeatures:
    """Advanced analysis features including comparison, batch processing, custom prompts, and A/B testing"""
    
    def __init__(self):
        self.custom_prompts = self._load_custom_prompts()
        self.analysis_history = []
        self.ab_test_results = self._load_ab_test_results()
    
    def _load_custom_prompts(self) -> Dict:
        """Load custom prompts from storage"""
        prompt_file = Path("data/custom_prompts.json")
        if prompt_file.exists():
            try:
                with open(prompt_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {
            "comprehensive": "Analyze this paper comprehensively including impact, novelty, and significance.",
            "summarization": "Provide a concise summary of the main contributions and results.",
            "methodology": "Focus on the methodology and technical approach.",
            "applications": "Identify potential applications and future work directions."
        }
    
    def _load_ab_test_results(self) -> Dict:
        """Load A/B test results from database"""
        try:
            # For now, we'll keep the in-memory storage for compatibility
            # In future, this could be migrated to database
            ab_test_file = Path("data/ab_test_results.json")
            if ab_test_file.exists():
                try:
                    with open(ab_test_file, 'r') as f:
                        return json.load(f)
                except:
                    return {}
            return {}
        except:
            return {}
    
    def save_ab_test_result(self, test_id: str, result: Dict) -> bool:
        """Save A/B test result"""
        try:
            self.ab_test_results[test_id] = result
            ab_test_file = Path("data/ab_test_results.json")
            ab_test_file.parent.mkdir(exist_ok=True)
            with open(ab_test_file, 'w') as f:
                json.dump(self.ab_test_results, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving AB test result: {e}")
            return False
    
    def save_custom_prompt(self, name: str, prompt: str) -> bool:
        """Save a custom prompt"""
        try:
            self.custom_prompts[name] = prompt
            prompt_file = Path("data/custom_prompts.json")
            prompt_file.parent.mkdir(exist_ok=True)
            with open(prompt_file, 'w') as f:
                json.dump(self.custom_prompts, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving prompt: {e}")
            return False
    
    def compare_models(self, paper: Dict, models: List[str]) -> Dict:
        """Compare analysis results from multiple models using real AI services"""
        results = {}
        
        for model_id in models:
            model_info = model_config.get_model_info(model_id)
            if model_info:
                # Use real AI analysis
                ai_analysis = ai_manager.analyze_with_model(model_id, paper, "comprehensive")
                
                results[model_id] = {
                    "model_name": model_info["name"],
                    "quality_score": model_info.get("quality_score", 0),
                    "complexity": model_info.get("complexity", "unknown"),
                    "cost": model_info.get("cost", "unknown"),
                    "analysis_depth": "advanced" if model_info.get("quality_score", 0) > 7 else "basic",
                    "ai_analysis": ai_analysis,
                    "analysis_available": not ai_analysis.get("error")
                }
        
        return results
    
    def batch_analyze(self, papers: List[Dict], model_id: str) -> List[Dict]:
        """Analyze multiple papers with the same model using real AI services"""
        results = []
        
        for i, paper in enumerate(papers):
            try:
                # Use real AI analysis
                ai_analysis = ai_manager.analyze_with_model(model_id, paper, "comprehensive")
                
                result = {
                    "paper_id": i,
                    "title": paper.get("title", "Unknown"),
                    "model_used": model_id,
                    "status": "completed" if not ai_analysis.get("error") else "failed",
                    "analysis_time": "2.5s",  # Approximate time
                    "ai_analysis": ai_analysis,
                    "error": ai_analysis.get("error") if ai_analysis.get("error") else None
                }
                results.append(result)
            except Exception as e:
                results.append({
                    "paper_id": i,
                    "title": paper.get("title", "Unknown"),
                    "model_used": model_id,
                    "status": "failed",
                    "error": str(e)
                })
        
        return results
    
    def calculate_paper_complexity(self, paper: Dict) -> str:
        """Calculate paper complexity for automatic model selection"""
        abstract = paper.get("abstract", "")
        title = paper.get("title", "")
        
        abstract_length = len(abstract.split())
        title_complexity = len(title.split())
        
        if abstract_length > 300 or title_complexity > 15:
            return "expert"
        elif abstract_length > 200 or title_complexity > 10:
            return "advanced"
        else:
            return "basic"
    
    def select_optimal_model(self, paper: Dict, budget_preference: str = "balanced") -> str:
        """Automatically select the optimal model based on paper complexity and budget"""
        complexity = self.calculate_paper_complexity(paper)
        
        available_models = model_config.get_available_models(complexity_filter=complexity)
        
        if budget_preference == "free":
            free_models = {k: v for k, v in available_models.items() if v["cost"] == "Free"}
            if free_models:
                return max(free_models.keys(), key=lambda x: free_models[x].get("quality_score", 0))
            return "rule_based"
        
        elif budget_preference == "quality":
            return max(available_models.keys(), key=lambda x: available_models[x].get("quality_score", 0))
        
        else:
            scored_models = []
            for model_id, model_info in available_models.items():
                cost_score = 10 if model_info["cost"] == "Free" else (5 if model_info["cost"] == "Low" else 0)
                quality_score = model_info.get("quality_score", 0)
                combined_score = cost_score + quality_score
                scored_models.append((combined_score, model_id))
            
            if scored_models:
                return max(scored_models, key=lambda x: x[0])[1]
            return "rule_based"
    
    def rate_analysis_quality(self, analysis: Dict, paper: Dict) -> float:
        """Rate the quality of an analysis"""
        quality_score = 0.0
        
        if analysis.get("structured_data"):
            quality_score += 2.0
        
        required_fields = ["impact_score", "readability", "topics"]
        if all(field in analysis for field in required_fields):
            quality_score += 2.0
        
        if analysis.get("key_contributions"):
            quality_score += 1.5
        
        if analysis.get("analysis_depth") == "advanced":
            quality_score += 2.0
        
        return min(quality_score, 10.0)
    
    def run_ab_test(self, paper: Dict, model_a: str, model_b: str, analysis_type: str = "comprehensive") -> Dict:
        """Run A/B test comparing two models on the same paper using real AI analysis"""
        model_a_info = model_config.get_model_info(model_a)
        model_b_info = model_config.get_model_info(model_b)
        
        # Run real AI analysis for both models
        analysis_a = ai_manager.analyze_with_model(model_a, paper, analysis_type)
        analysis_b = ai_manager.analyze_with_model(model_b, paper, analysis_type)
        
        result = {
            "paper_title": paper.get("title", "Unknown"),
            "model_a": model_a,
            "model_a_name": model_a_info.get("name", model_a),
            "model_b": model_b,
            "model_b_name": model_b_info.get("name", model_b),
            "model_a_quality": model_a_info.get("quality_score", 0),
            "model_b_quality": model_b_info.get("quality_score", 0),
            "model_a_cost": model_a_info.get("cost", "unknown"),
            "model_b_cost": model_b_info.get("cost", "unknown"),
            "analysis_type": analysis_type,
            "timestamp": datetime.now().isoformat(),
            "user_preference": None,
            "winner": None,
            "analysis_a": analysis_a,
            "analysis_b": analysis_b,
            "analysis_a_available": not analysis_a.get("error"),
            "analysis_b_available": not analysis_b.get("error")
        }
        
        return result
    
    def record_ab_test_preference(self, test_id: str, preferred_model: str, reason: str = "") -> bool:
        """Record user preference from A/B test"""
        if test_id in self.ab_test_results:
            self.ab_test_results[test_id]["user_preference"] = preferred_model
            self.ab_test_results[test_id]["preference_reason"] = reason
            self.ab_test_results[test_id]["winner"] = preferred_model
            
            # Save to file
            return self.save_ab_test_result(test_id, self.ab_test_results[test_id])
        return False
    
    def get_ab_test_statistics(self) -> Dict:
        """Get statistics from all A/B tests"""
        if not self.ab_test_results:
            return {"total_tests": 0, "model_wins": {}}
        
        model_wins = {}
        total_tests = len(self.ab_test_results)
        
        for test_id, result in self.ab_test_results.items():
            winner = result.get("winner")
            if winner:
                model_wins[winner] = model_wins.get(winner, 0) + 1
        
        return {
            "total_tests": total_tests,
            "model_wins": model_wins,
            "win_rates": {model: (wins / total_tests * 100) for model, wins in model_wins.items()}
        }
    
    def get_model_recommendation(self, analysis_type: str) -> str:
        """Get recommended model based on A/B test history"""
        stats = self.get_ab_test_statistics()
        
        if stats["total_tests"] > 0:
            # Recommend model with highest win rate
            win_rates = stats["win_rates"]
            if win_rates:
                return max(win_rates.keys(), key=lambda x: win_rates[x])
        
        # Fallback to highest quality model
        available_models = model_config.get_available_models()
        return max(available_models.keys(), key=lambda x: available_models[x].get("quality_score", 0))

# Initialize advanced features
advanced_features = AdvancedAnalysisFeatures()

# ==================== DATA LAYER ====================

class DataManager:
    """Manage research data storage using SQLite database"""
    
    def __init__(self):
        # Use the database manager instead of JSON files
        self.db = db_manager
    
    def save_reading_list(self, user_id: str, papers: List[Dict]):
        """Save user's reading list to database"""
        # Clear existing reading list for this user
        try:
            # Get current papers to determine which to add/update
            current_papers = self.db.get_reading_list(user_id)
            current_paper_ids = {p['paper_id'] for p in current_papers}
            
            # Add/update papers
            for paper in papers:
                paper_id = paper.get('externalIds', {}).get('ArXiv') or paper.get('paperId') or paper.get('title')
                if paper_id not in current_paper_ids or paper.get('status'):
                    self.db.add_to_reading_list(user_id, paper)
                    
        except Exception as e:
            print(f"Error saving reading list: {e}")
    
    def get_reading_list(self, user_id: str) -> List[Dict]:
        """Get user's reading list from database"""
        try:
            papers = self.db.get_reading_list(user_id)
            # Convert database format to expected format
            formatted_papers = []
            for paper in papers:
                formatted_paper = {
                    'title': paper.get('title', ''),
                    'year': paper.get('year', ''),
                    'url': paper.get('url', ''),
                    'abstract': paper.get('abstract', ''),
                    'citationCount': paper.get('citation_count', 0),
                    'status': paper.get('status', 'to-read'),
                    'added_date': paper.get('added_date', ''),
                    'paperId': paper.get('paper_id', '')
                }
                # Add external IDs if available
                if paper.get('paper_data'):
                    try:
                        paper_data = json.loads(paper['paper_data'])
                        formatted_paper.update(paper_data)
                    except:
                        pass
                formatted_papers.append(formatted_paper)
            return formatted_papers
        except Exception as e:
            print(f"Error getting reading list: {e}")
            return []
        
    def save_notes(self, user_id: str, paper_id: str, notes: str):
        """Save notes for a paper to database"""
        try:
            # Clean paper ID if it's a URL
            clean_paper_id = paper_id.split("/")[-1] if "/" in paper_id else paper_id
            self.db.save_note(user_id, clean_paper_id, notes)
        except Exception as e:
            print(f"Error saving notes: {e}")
    
    def get_notes(self, user_id: str, paper_id: str) -> str:
        """Get notes for a paper from database"""
        try:
            # Clean paper ID if it's a URL
            clean_paper_id = paper_id.split("/")[-1] if "/" in paper_id else paper_id
            notes = self.db.get_note(user_id, clean_paper_id)
            return notes if notes else ""
        except Exception as e:
            print(f"Error getting notes: {e}")
            return ""

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
        gr.Markdown("# 📚 Enhanced Research Assistant - AI Model Selection")
        gr.Markdown("Advanced research companion with custom AI model selection, multi-source recommendations, and workflow management")

        gr.Markdown("""
        ### 🆔 Quick Start Guide

        **How to Get Paper IDs:**
        - From arXiv URL: Use the last part (e.g., `1706.03762` from `https://arxiv.org/abs/1706.03762`)
        - From recommendations: Use the "Extract Paper ID" button in Reading List tab
        - From Paper JSON: Check the `externalIds.ArXiv` field in the Paper JSON output

        **How to Get User ID:**
        - Create your own: Use any identifier (email, username, or unique string)
        - Keep it consistent: Use the same ID across Reading List and Notes tabs
        - Privacy: Your data is stored locally and organized by your user ID

        **How to Get Paper JSON:**
        - Automatic: After getting recommendations, the Paper JSON field shows complete paper data
        - Copy & Paste: Use the JSON in Reading List and other features
        - Contains: Title, year, abstract, citations, URL, paper IDs, and more
        """)
        
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

                paper_json_output = gr.Code(label="Paper JSON (Click to Copy)", language="json", lines=10)

                def get_recommendations(paper_id, sources):
                    if not paper_id:
                        return "❌ Please enter a paper ID or URL", "", ""

                    # Extract arXiv ID from URL if needed
                    arxiv_id = paper_id.split("/")[-1] if "/" in paper_id else paper_id

                    # Get recommendations
                    source_map = {
                        "Semantic Scholar": "semantic_scholar",
                        "arXiv": "arxiv",
                        "Citations": "semantic_scholar"
                    }

                    selected_sources = [source_map[s] for s in sources if s in source_map]
                    
                    try:
                        # Safe API call for recommendations
                        def get_rec():
                            return recommender.get_recommendations(arxiv_id, selected_sources)
                        
                        rec_result = safe_api_call(get_rec, service_name="Recommendation API")
                        
                        if not rec_result["success"]:
                            return f"❌ {rec_result['error']['user_message']}", "", ""

                        results = rec_result["data"]

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
                        paper_json = ""
                        analysis_text = ""
                        
                        if results.get("semantic_scholar"):
                            input_paper = results["semantic_scholar"][0] if results["semantic_scholar"] else {}
                            try:
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

                                # Generate paper JSON for the user
                                paper_json = json.dumps(input_paper, indent=2)
                            except Exception as e:
                                analysis_text = f"⚠️ Analysis not available: {str(e)}"
                        else:
                            analysis_text = "⚠️ Analysis not available for this paper."

                        return output, analysis_text, paper_json
                        
                    except Exception as e:
                        error_info = error_handler.handle_error(e, {"function": "get_recommendations"})
                        return f"❌ {error_info['user_message']}\n\n💡 {error_info['recovery_suggestion']}", "", ""
                
                recommend_btn.click(get_recommendations, inputs=[paper_input, source_selector], outputs=[recommendations_output, analysis_output, paper_json_output])
            
            # ==================== READING LIST TAB ====================
            with gr.Tab("📖 Reading List"):
                gr.Markdown("## Personal Reading List Management")

                gr.Markdown("""
                **User ID**: Enter any identifier to create your personal reading list.
                - Use your email, username, or any unique identifier
                - Your data is stored locally and private
                - Same user ID will load your previous data
                """)

                user_id = gr.Textbox(label="User ID", placeholder="Enter your identifier (e.g., email, username)")

                with gr.Row():
                    add_paper_btn = gr.Button("Add to Reading List", variant="primary")
                    view_list_btn = gr.Button("View Reading List", variant="secondary")

                gr.Markdown("**Paper Details**: Paste the paper JSON from the recommendations above, or enter manually.")
                paper_to_add = gr.Textbox(label="Paper Details (JSON)", placeholder='{"title": "Paper Title", "year": "2023", "url": "..."}', lines=5)

                with gr.Row():
                    extract_paper_id_btn = gr.Button("📋 Extract Paper ID from JSON", variant="secondary")
                    paper_id_display = gr.Textbox(label="Extracted Paper ID", interactive=False)

                reading_list_output = gr.Markdown()

                def extract_paper_id_from_json(paper_json):
                    """Extract paper ID from JSON"""
                    if not paper_json:
                        return "Please paste paper JSON first."

                    try:
                        paper = json.loads(paper_json)
                        # Try to get paper ID from various fields
                        paper_id = (
                            paper.get("externalIds", {}).get("ArXiv", "") or
                            paper.get("paperId", "") or
                            paper.get("id", "") or
                            paper.get("url", "").split("/")[-1] if paper.get("url") else ""
                        )

                        if paper_id:
                            return f"Extracted Paper ID: {paper_id}"
                        else:
                            return "No paper ID found in JSON. Available fields: " + ", ".join(paper.keys())
                    except json.JSONDecodeError:
                        return "Invalid JSON format. Please provide valid JSON."

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
                extract_paper_id_btn.click(extract_paper_id_from_json, inputs=[paper_to_add], outputs=[paper_id_display])
            
            # ==================== NOTES & ANNOTATIONS TAB ====================
            with gr.Tab("📝 Notes & Annotations"):
                gr.Markdown("## Personal Notes and Annotations")

                gr.Markdown("""
                **User ID**: Enter the same identifier you used in the Reading List tab.
                - Your notes are linked to your user ID
                - Notes are stored privately and locally
                """)

                note_user_id = gr.Textbox(label="User ID", placeholder="Enter your identifier (same as Reading List)")

                gr.Markdown("""
                **Paper ID**: Enter the paper ID you want to add notes for.
                - You can extract paper IDs from the Paper JSON in the recommendations tab
                - Or enter arXiv IDs directly (e.g., "1706.03762")
                - Or use paper URLs (e.g., "https://arxiv.org/abs/1706.03762")
                """)

                note_paper_id = gr.Textbox(label="Paper ID", placeholder="Enter paper ID or URL")
                note_content = gr.Textbox(label="Your Notes", lines=10, placeholder="Write your notes, insights, and questions here...")
                
                save_note_btn = gr.Button("Save Note", variant="primary")
                load_note_btn = gr.Button("Load Note", variant="secondary")
                
                note_output = gr.Markdown()
                
                def save_note(user_id, paper_id, notes):
                    if not user_id or not paper_id:
                        return "Please provide user ID and paper ID."

                    # Extract paper ID from URL if needed
                    clean_paper_id = paper_id.split("/")[-1] if "/" in paper_id else paper_id

                    data_manager.save_notes(user_id, clean_paper_id, notes)
                    return f"Notes saved successfully for paper: {clean_paper_id}"

                def load_note(user_id, paper_id):
                    if not user_id or not paper_id:
                        return "Please provide user ID and paper ID."

                    # Extract paper ID from URL if needed
                    clean_paper_id = paper_id.split("/")[-1] if "/" in paper_id else paper_id

                    notes = data_manager.get_notes(user_id, clean_paper_id)
                    if notes:
                        return f"## Notes for Paper {clean_paper_id}\n\n{notes}"
                    else:
                        return f"No notes found for paper {clean_paper_id}."
                
                save_note_btn.click(save_note, inputs=[note_user_id, note_paper_id, note_content], outputs=[note_output])
                load_note_btn.click(load_note, inputs=[note_user_id, note_paper_id], outputs=[note_output])
            
            # ==================== ADDITIONAL DATA SOURCES TAB ====================
            with gr.Tab("🌐 Additional Data Sources"):
                gr.Markdown("## Google Scholar & PubMed Integration")
                
                gr.Markdown("""
                **Expanded Paper Discovery:**
                - **Google Scholar**: Broad academic search across all disciplines
                - **PubMed**: Biomedical and life sciences literature
                - **Combined Search**: Search multiple sources simultaneously
                """)
                
                search_query = gr.Textbox(
                    label="Search Query",
                    placeholder="e.g., 'machine learning healthcare' or 'neural networks interpretation'"
                )
                
                source_selector_extended = gr.CheckboxGroup(
                    choices=["Google Scholar", "PubMed", "Both"],
                    value=["Google Scholar"],
                    label="Data Sources"
                )
                
                max_results = gr.Slider(
                    minimum=5,
                    maximum=20,
                    value=10,
                    step=1,
                    label="Max Results per Source"
                )
                
                search_btn = gr.Button("🔍 Search", variant="primary")
                search_output = gr.Markdown()
                
                def search_additional_sources(query, sources, max_res):
                    if not query:
                        return "❌ Please enter a search query."
                    
                    try:
                        source_map = {
                            "Google Scholar": "google_scholar",
                            "PubMed": "pubmed",
                            "Both": ["google_scholar", "pubmed"]
                        }
                        
                        selected_sources = []
                        if "Google Scholar" in sources or "Both" in sources:
                            selected_sources.append("google_scholar")
                        if "PubMed" in sources or "Both" in sources:
                            selected_sources.append("pubmed")
                        
                        if not selected_sources:
                            return "❌ Please select at least one data source."
                        
                        # Perform search
                        results = data_source_manager.search_all_sources(query, selected_sources, max_res)
                        
                        output = f"## Search Results for: '{query}'\n\n"
                        
                        for source, papers in results.items():
                            if papers:
                                source_name = source.replace('_', ' ').title()
                                output += f"### 📚 {source_name} ({len(papers)} papers)\n\n"
                                
                                for i, paper in enumerate(papers[:max_res], 1):
                                    output += f"**{i}. {paper['title']}** ({paper['year']})\n"
                                    
                                    if paper.get('authors'):
                                        output += f"- **Authors**: {paper['authors']}\n"
                                    
                                    if paper.get('journal'):
                                        output += f"- **Journal**: {paper['journal']}\n"
                                    
                                    if paper.get('pmid'):
                                        output += f"- **PMID**: {paper['pmid']}\n"
                                    
                                    output += f"- [View Paper]({paper['url']})\n"
                                    
                                    if paper.get('abstract'):
                                        abstract_preview = paper['abstract'][:200] + "..." if len(paper['abstract']) > 200 else paper['abstract']
                                        output += f"- **Abstract**: {abstract_preview}\n"
                                    
                                    output += "\n"
                            else:
                                source_name = source.replace('_', ' ').title()
                                output += f"### 📚 {source_name}\n\nNo papers found.\n\n"
                        
                        return output
                        
                    except Exception as e:
                        error_info = error_handler.handle_error(e, {"function": "search_additional_sources"})
                        return f"❌ {error_info['user_message']}\n\n💡 {error_info['recovery_suggestion']}"
                
                search_btn.click(search_additional_sources, inputs=[search_query, source_selector_extended, max_results], outputs=[search_output])
                
                gr.Markdown("---")
                gr.Markdown("### 🔍 Search by PubMed ID")
                
                pmid_input = gr.Textbox(label="PubMed ID (PMID)", placeholder="e.g., 34567890")
                pmid_search_btn = gr.Button("Get Paper Details", variant="secondary")
                pmid_output = gr.Markdown()
                
                def search_by_pmid(pmid):
                    if not pmid:
                        return "❌ Please enter a PubMed ID."
                    
                    try:
                        paper = data_source_manager.get_paper_by_pmid(pmid)
                        
                        if not paper:
                            return f"❌ No paper found with PMID: {pmid}"
                        
                        output = f"## Paper Details\n\n"
                        output += f"**Title**: {paper['title']}\n"
                        output += f"**Authors**: {paper['authors']}\n"
                        output += f"**Year**: {paper['year']}\n"
                        output += f"**Journal**: {paper['journal']}\n"
                        output += f"**PMID**: {paper['pmid']}\n"
                        output += f"**URL**: {paper['url']}\n\n"
                        output += f"**Abstract**:\n{paper['abstract']}\n"
                        
                        return output
                        
                    except Exception as e:
                        error_info = error_handler.handle_error(e, {"function": "search_by_pmid"})
                        return f"❌ {error_info['user_message']}\n\n💡 {error_info['recovery_suggestion']}"
                
                pmid_search_btn.click(search_by_pmid, inputs=[pmid_input], outputs=[pmid_output])
            
            # ==================== PDF UPLOAD TAB ====================
            with gr.Tab("📄 PDF Upload & Analysis"):
                gr.Markdown("## Upload and Analyze PDF Documents")
                
                gr.Markdown("""
                **PDF Analysis Features:**
                - **Text Extraction**: Extract text from PDF documents
                - **Structure Analysis**: Identify sections, abstract, authors
                - **AI Analysis**: Analyze uploaded papers with AI models
                - **Integration**: Use analyzed papers in other features
                """)
                
                pdf_upload = gr.File(
                    label="Upload PDF",
                    file_types=[".pdf"],
                    type="binary"
                )
                
                analyze_pdf_btn = gr.Button("📄 Analyze PDF", variant="primary")
                
                pdf_summary_output = gr.Markdown()
                pdf_json_output = gr.Code(label="Paper JSON (for use in other features)", language="json", lines=10)
                
                gr.Markdown("---")
                gr.Markdown("### 🤖 AI Analysis of Uploaded PDF")
                
                pdf_model_selector = gr.Dropdown(
                    choices=[f"{info['name']} ({model_id})" for model_id, info in model_config.get_available_models().items()],
                    value=None,
                    label="Select AI Model for Analysis"
                )
                
                pdf_analysis_type = gr.Radio(
                    choices=["comprehensive", "summarization", "methodology", "applications"],
                    value="comprehensive",
                    label="Analysis Type"
                )
                
                analyze_pdf_with_ai_btn = gr.Button("🧠 Analyze with AI", variant="secondary")
                pdf_ai_output = gr.Markdown()
                
                def analyze_uploaded_pdf(pdf_file):
                    if pdf_file is None:
                        return "❌ Please upload a PDF file.", ""
                    
                    try:
                        filename = pdf_file.name if hasattr(pdf_file, 'name') else "uploaded.pdf"
                        
                        # Analyze PDF
                        analysis_result = pdf_engine.analyze_uploaded_pdf(pdf_file, filename)
                        
                        if not analysis_result['success']:
                            return f"❌ PDF analysis failed: {analysis_result['error']}", ""
                        
                        # Generate summary
                        summary = pdf_engine.get_pdf_summary(analysis_result)
                        
                        # Get paper JSON
                        paper_json = pdf_engine.get_paper_json(analysis_result)
                        
                        return summary, paper_json
                        
                    except Exception as e:
                        error_info = error_handler.handle_error(e, {"function": "analyze_uploaded_pdf"})
                        return f"❌ {error_info['user_message']}\n\n💡 {error_info['recovery_suggestion']}", ""
                
                def analyze_pdf_with_ai(pdf_file, model_selection, analysis_type):
                    if pdf_file is None:
                        return "❌ Please upload a PDF file first."
                    
                    if not model_selection:
                        return "❌ Please select an AI model."
                    
                    try:
                        filename = pdf_file.name if hasattr(pdf_file, 'name') else "uploaded.pdf"
                        
                        # Analyze PDF
                        pdf_result = pdf_engine.analyze_uploaded_pdf(pdf_file, filename)
                        
                        if not pdf_result['success']:
                            return f"❌ PDF analysis failed: {pdf_result['error']}"
                        
                        # Get paper dict
                        paper = pdf_result['paper']
                        
                        # Extract model ID
                        model_id = model_selection.split("(")[-1].replace(")", "")
                        
                        # Run AI analysis
                        ai_analysis = ai_manager.analyze_with_model(model_id, paper, analysis_type)
                        
                        # Format output
                        output = "## AI Analysis of Uploaded PDF\n\n"
                        output += f"**Paper**: {paper.get('title', 'Unknown')}\n"
                        output += f"**Model**: {model_selection}\n"
                        output += f"**Analysis Type**: {analysis_type}\n\n"
                        
                        if ai_analysis.get('error'):
                            output += f"❌ AI Analysis Error: {ai_analysis['error']}\n"
                            if ai_analysis.get('analysis'):
                                output += f"\nFallback Analysis: {ai_analysis['analysis']}\n"
                        else:
                            output += f"### AI Analysis Summary\n\n{ai_analysis.get('summary', 'No analysis available')}\n"
                        
                        return output
                        
                    except Exception as e:
                        error_info = error_handler.handle_error(e, {"function": "analyze_pdf_with_ai"})
                        return f"❌ {error_info['user_message']}\n\n💡 {error_info['recovery_suggestion']}"
                
                analyze_pdf_btn.click(analyze_uploaded_pdf, inputs=[pdf_upload], outputs=[pdf_summary_output, pdf_json_output])
                analyze_pdf_with_ai_btn.click(analyze_pdf_with_ai, inputs=[pdf_upload, pdf_model_selector, pdf_analysis_type], outputs=[pdf_ai_output])
            
            # ==================== MODEL SELECTION TAB ====================
            with gr.Tab("🤖 Model Selection"):
                gr.Markdown("## Select Analysis Model")
                
                model_selector = gr.Dropdown(
                    choices=[f"{info['name']} ({model_id})" for model_id, info in model_config.get_available_models().items()],
                    value=None,
                    label="Select Analysis Model"
                )
                
                model_info = gr.Markdown()
                
                def show_model_info(model_selection):
                    model_id = model_selection.split("(")[-1].replace(")", "")
                    info = model_config.models.get(model_id, {})
                    if info:
                        return f"### {info['name']}\n- **Cost**: {info['cost']}\n- **Capabilities**: {', '.join(info['capabilities'])}"
                    return "Model not found"
                
                model_selector.change(show_model_info, inputs=[model_selector], outputs=[model_info])
                
                gr.Markdown("### API Key Configuration")
                api_key_service = gr.Dropdown(choices=["OpenAI", "Anthropic"], label="Service")
                api_key_input = gr.Textbox(label="API Key", type="password")
                save_key_btn = gr.Button("Save API Key")
                key_status = gr.Markdown()
                
                def save_key(service, key):
                    if key:
                        env_var = f"{service.upper()}_API_KEY"
                        os.environ[env_var] = key
                        return f"✅ API key saved for {service}"
                    return "Please enter an API key"
                
                save_key_btn.click(save_key, inputs=[api_key_service, api_key_input], outputs=[key_status])
            
            # ==================== MODEL COMPARISON TAB ====================
            with gr.Tab("⚖️ Model Comparison"):
                gr.Markdown("## Compare AI Models Side-by-Side")
                
                comparison_paper_input = gr.Textbox(
                    label="Paper Details (JSON)",
                    placeholder='{"title": "Paper Title", "abstract": "...", "year": "2023", "citationCount": 100}',
                    lines=3
                )
                
                models_to_compare = gr.CheckboxGroup(
                    choices=[f"{info['name']} ({model_id})" for model_id, info in model_config.get_available_models().items()],
                    value=["rule_based (rule_based)", "gpt-4o-mini (gpt-4o-mini)"],
                    label="Models to Compare"
                )
                
                compare_btn = gr.Button("Compare Models", variant="primary")
                comparison_output = gr.Markdown()
                
                def perform_model_comparison(paper_json, models_selection, progress=gr.Progress()):
                    if not paper_json:
                        return "Please enter paper details in JSON format."
                    
                    try:
                        paper = json.loads(paper_json)
                        model_ids = [m.split("(")[-1].replace(")", "") for m in models_selection]
                        
                        progress(0, desc="Starting model comparison...")
                        
                        results = {}
                        total_models = len(model_ids)
                        
                        for i, model_id in enumerate(model_ids):
                            progress((i + 1) / total_models, desc=f"Analyzing with model {i+1}/{total_models}...")
                            results[model_id] = advanced_features.compare_models(paper, [model_id])[model_id]
                        
                        progress(1.0, desc="Model comparison complete!")
                        
                        output = "## Model Comparison Results\n\n"
                        output += f"**Paper**: {paper.get('title', 'Unknown')}\n\n"
                        
                        for model_id, comparison in results.items():
                            output += f"### {comparison['model_name']}\n"
                            output += f"- **Quality Score**: {comparison['quality_score']}/10\n"
                            output += f"- **Complexity**: {comparison['complexity']}\n"
                            output += f"- **Cost**: {comparison['cost']}\n"
                            output += f"- **Analysis Depth**: {comparison['analysis_depth']}\n"
                            output += f"- **AI Analysis Available**: {'✅ Yes' if comparison['analysis_available'] else '❌ No'}\n\n"
                            
                            if comparison['analysis_available']:
                                ai_analysis = comparison.get('ai_analysis', {})
                                if ai_analysis.get('summary'):
                                    output += f"**AI Analysis Summary**:\n{ai_analysis['summary'][:500]}...\n\n"
                            elif comparison.get('ai_analysis', {}).get('error'):
                                output += f"**Error**: {comparison['ai_analysis']['error']}\n\n"
                        
                        return output
                        
                    except json.JSONDecodeError:
                        return "Invalid JSON format. Please provide valid JSON."
                    except Exception as e:
                        return f"Error during comparison: {str(e)}"
                
                compare_btn.click(perform_model_comparison, inputs=[comparison_paper_input, models_to_compare], outputs=[comparison_output])
            
            # ==================== BATCH PROCESSING TAB ====================
            with gr.Tab("📦 Batch Processing"):
                gr.Markdown("## Analyze Multiple Papers at Once")
                
                batch_model_selector = gr.Dropdown(
                    choices=[f"{info['name']} ({model_id})" for model_id, info in model_config.get_available_models().items()],
                    value=None,
                    label="Select Model for Batch Analysis"
                )
                
                batch_papers_input = gr.Textbox(
                    label="Multiple Papers (JSON Array)",
                    placeholder='[{"title": "Paper 1", ...}, {"title": "Paper 2", ...}]',
                    lines=5
                )
                
                batch_process_btn = gr.Button("Process Batch", variant="primary")
                batch_output = gr.Markdown()
                
                def process_batch(papers_json, model_selection, progress=gr.Progress()):
                    if not papers_json:
                        return "Please enter papers in JSON array format."
                    
                    try:
                        papers = json.loads(papers_json)
                        model_id = model_selection.split("(")[-1].replace(")", "")
                        
                        progress(0, desc="Starting batch processing...")
                        
                        results = []
                        total_papers = len(papers)
                        
                        for i, paper in enumerate(papers):
                            progress((i + 1) / total_papers, desc=f"Processing paper {i+1}/{total_papers}...")
                            
                            try:
                                # Use real AI analysis
                                ai_analysis = ai_manager.analyze_with_model(model_id, paper, "comprehensive")
                                
                                result = {
                                    "paper_id": i,
                                    "title": paper.get("title", "Unknown"),
                                    "model_used": model_id,
                                    "status": "completed" if not ai_analysis.get("error") else "failed",
                                    "analysis_time": "2.5s",  # Approximate time
                                    "ai_analysis": ai_analysis,
                                    "error": ai_analysis.get("error") if ai_analysis.get("error") else None
                                }
                                results.append(result)
                            except Exception as e:
                                results.append({
                                    "paper_id": i,
                                    "title": paper.get("title", "Unknown"),
                                    "model_used": model_id,
                                    "status": "failed",
                                    "error": str(e)
                                })
                        
                        progress(1.0, desc="Batch processing complete!")
                        
                        output = f"## Batch Processing Results\n\n"
                        output += f"**Model Used**: {model_id}\n"
                        output += f"**Papers Processed**: {len(results)}\n\n"
                        
                        successful = sum(1 for r in results if r['status'] == 'completed')
                        failed = len(results) - successful
                        
                        output += f"**Successful**: {successful}\n"
                        output += f"**Failed**: {failed}\n\n"
                        
                        for result in results:
                            status_emoji = "✅" if result['status'] == 'completed' else "❌"
                            output += f"{status_emoji} **{result['title']}**: {result['status']}"
                            if result.get('error'):
                                output += f" - Error: {result['error']}"
                            output += "\n"
                        
                        return output
                        
                    except json.JSONDecodeError:
                        return "Invalid JSON array format."
                    except Exception as e:
                        return f"Error during batch processing: {str(e)}"
                
                batch_process_btn.click(process_batch, inputs=[batch_papers_input, batch_model_selector], outputs=[batch_output])
            
            # ==================== CUSTOM PROMPTS TAB ====================
            with gr.Tab("✏️ Custom Prompts"):
                gr.Markdown("## Define Custom Analysis Prompts")
                
                prompt_name = gr.Textbox(label="Prompt Name", placeholder="e.g., technical_review")
                prompt_content = gr.Textbox(
                    label="Prompt Content",
                    lines=5,
                    placeholder="Enter your custom analysis prompt..."
                )
                
                save_prompt_btn = gr.Button("Save Prompt", variant="primary")
                prompt_status = gr.Markdown()
                
                existing_prompts = gr.Dropdown(
                    choices=list(advanced_features.custom_prompts.keys()),
                    label="Existing Prompts"
                )
                
                prompt_preview = gr.Markdown()
                
                def save_custom_prompt(name, content):
                    if not name or not content:
                        return "Please provide both name and content."
                    
                    if advanced_features.save_custom_prompt(name, content):
                        return f"✅ Prompt '{name}' saved successfully!"
                    return "❌ Failed to save prompt."
                
                def show_prompt_preview(prompt_name):
                    prompt = advanced_features.custom_prompts.get(prompt_name, "")
                    return f"### {prompt_name}\n\n{prompt}"
                
                save_prompt_btn.click(save_custom_prompt, inputs=[prompt_name, prompt_content], outputs=[prompt_status])
                existing_prompts.change(show_prompt_preview, inputs=[existing_prompts], outputs=[prompt_preview])
            
            # ==================== AUTO MODEL SELECTION TAB ====================
            with gr.Tab("🎯 Auto Model Selection"):
                gr.Markdown("## Automatic Model Selection Based on Paper Complexity")
                
                auto_paper_input = gr.Textbox(
                    label="Paper Details (JSON)",
                    placeholder='{"title": "Paper Title", "abstract": "...", "year": "2023"}',
                    lines=3
                )
                
                budget_preference = gr.Radio(
                    choices=["free", "balanced", "quality"],
                    value="balanced",
                    label="Budget Preference"
                )
                
                auto_select_btn = gr.Button("Auto-Select Model", variant="primary")
                auto_selection_output = gr.Markdown()
                
                def auto_select_model(paper_json, budget):
                    if not paper_json:
                        return "Please enter paper details in JSON format."
                    
                    try:
                        paper = json.loads(paper_json)
                        complexity = advanced_features.calculate_paper_complexity(paper)
                        selected_model = advanced_features.select_optimal_model(paper, budget)
                        model_info = model_config.get_model_info(selected_model)
                        
                        output = f"## Auto Model Selection Results\n\n"
                        output += f"**Paper Complexity**: {complexity}\n"
                        output += f"**Budget Preference**: {budget}\n"
                        output += f"**Selected Model**: {model_info['name']}\n"
                        output += f"**Model Cost**: {model_info['cost']}\n"
                        output += f"**Model Quality Score**: {model_info.get('quality_score', 'N/A')}/10\n\n"
                        output += f"**Rationale**: This model was selected based on the paper's complexity level and your budget preferences."
                        
                        return output
                        
                    except json.JSONDecodeError:
                        return "Invalid JSON format."
                    except Exception as e:
                        return f"Error during selection: {str(e)}"
                
                auto_select_btn.click(auto_select_model, inputs=[auto_paper_input, budget_preference], outputs=[auto_selection_output])
            
            # ==================== A/B TESTING TAB ====================
            with gr.Tab("🧪 A/B Testing"):
                gr.Markdown("## A/B Test Models on Your Papers")
                
                ab_test_paper_input = gr.Textbox(
                    label="Paper Details (JSON)",
                    placeholder='{"title": "Paper Title", "abstract": "...", "year": "2023"}',
                    lines=3
                )
                
                with gr.Row():
                    model_a_selector = gr.Dropdown(
                        choices=[f"{info['name']} ({model_id})" for model_id, info in model_config.get_available_models().items()],
                        value=None,
                        label="Model A"
                    )
                    model_b_selector = gr.Dropdown(
                        choices=[f"{info['name']} ({model_id})" for model_id, info in model_config.get_available_models().items()],
                        value=None,
                        label="Model B"
                    )
                
                analysis_type_selector = gr.Dropdown(
                    choices=["comprehensive", "summarization", "topic_modeling", "quick"],
                    value="comprehensive",
                    label="Analysis Type"
                )
                
                run_ab_test_btn = gr.Button("Run A/B Test", variant="primary")
                
                ab_test_output = gr.Markdown()
                
                with gr.Row():
                    preferred_model = gr.Radio(
                        choices=["Model A", "Model B", "Tie"],
                        label="Which analysis did you prefer?"
                    )
                    preference_reason = gr.Textbox(label="Reason for preference", placeholder="Why did you prefer this model?")
                    record_preference_btn = gr.Button("Record Preference", variant="secondary")
                
                preference_status = gr.Markdown()
                
                ab_statistics_btn = gr.Button("View A/B Test Statistics", variant="secondary")
                ab_statistics_output = gr.Markdown()
                
                def run_ab_test(paper_json, model_a, model_b, analysis_type, progress=gr.Progress()):
                    if not paper_json:
                        return "Please enter paper details in JSON format."
                    
                    try:
                        paper = json.loads(paper_json)
                        model_a_id = model_a.split("(")[-1].replace(")", "")
                        model_b_id = model_b.split("(")[-1].replace(")", "")
                        
                        progress(0, desc="Starting A/B test...")
                        
                        # Run A/B test with real AI analysis
                        progress(0.3, desc=f"Analyzing with Model A: {model_a_id}...")
                        analysis_a = ai_manager.analyze_with_model(model_a_id, paper, analysis_type)
                        
                        progress(0.6, desc=f"Analyzing with Model B: {model_b_id}...")
                        analysis_b = ai_manager.analyze_with_model(model_b_id, paper, analysis_type)
                        
                        progress(0.8, desc="Compiling results...")
                        
                        model_a_info = model_config.get_model_info(model_a_id)
                        model_b_info = model_config.get_model_info(model_b_id)
                        
                        test_result = {
                            "paper_title": paper.get("title", "Unknown"),
                            "model_a": model_a_id,
                            "model_a_name": model_a_info.get("name", model_a_id),
                            "model_b": model_b_id,
                            "model_b_name": model_b_info.get("name", model_b_id),
                            "model_a_quality": model_a_info.get("quality_score", 0),
                            "model_b_quality": model_b_info.get("quality_score", 0),
                            "model_a_cost": model_a_info.get("cost", "unknown"),
                            "model_b_cost": model_b_info.get("cost", "unknown"),
                            "analysis_type": analysis_type,
                            "timestamp": datetime.now().isoformat(),
                            "user_preference": None,
                            "winner": None,
                            "analysis_a": analysis_a,
                            "analysis_b": analysis_b,
                            "analysis_a_available": not analysis_a.get("error"),
                            "analysis_b_available": not analysis_b.get("error")
                        }
                        
                        # Store result temporarily for preference recording
                        test_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        advanced_features.save_ab_test_result(test_id, test_result)
                        
                        progress(1.0, desc="A/B test complete!")
                        
                        output = f"## A/B Test Results\n\n"
                        output += f"**Test ID**: {test_id}\n"
                        output += f"**Paper**: {test_result['paper_title']}\n\n"
                        
                        output += f"### Model A: {test_result['model_a_name']}\n"
                        output += f"- Quality Score: {test_result['model_a_quality']}/10\n"
                        output += f"- Cost: {test_result['model_a_cost']}\n"
                        output += f"- Analysis Available: {'✅ Yes' if test_result['analysis_a_available'] else '❌ No'}\n"
                        
                        if test_result['analysis_a_available']:
                            analysis_a = test_result.get('analysis_a', {})
                            if analysis_a.get('summary'):
                                output += f"- **AI Analysis**: {analysis_a['summary'][:300]}...\n"
                        elif test_result.get('analysis_a', {}).get('error'):
                            output += f"- **Error**: {test_result['analysis_a']['error']}\n"
                        
                        output += "\n"
                        
                        output += f"### Model B: {test_result['model_b_name']}\n"
                        output += f"- Quality Score: {test_result['model_b_quality']}/10\n"
                        output += f"- Cost: {test_result['model_b_cost']}\n"
                        output += f"- Analysis Available: {'✅ Yes' if test_result['analysis_b_available'] else '❌ No'}\n"
                        
                        if test_result['analysis_b_available']:
                            analysis_b = test_result.get('analysis_b', {})
                            if analysis_b.get('summary'):
                                output += f"- **AI Analysis**: {analysis_b['summary'][:300]}...\n"
                        elif test_result.get('analysis_b', {}).get('error'):
                            output += f"- **Error**: {test_result['analysis_b']['error']}\n"
                        
                        output += f"\n**Analysis Type**: {analysis_type}\n\n"
                        output += "Review the analysis results above and record your preference."
                        
                        return output
                        
                    except json.JSONDecodeError:
                        return "Invalid JSON format."
                    except Exception as e:
                        return f"Error during A/B test: {str(e)}"
                
                def record_preference(paper_json, model_a, model_b, preference, reason):
                    if not paper_json:
                        return "No A/B test has been run yet."
                    
                    try:
                        paper = json.loads(paper_json)
                        model_a_id = model_a.split("(")[-1].replace(")", "")
                        model_b_id = model_b.split("(")[-1].replace(")", "")
                        
                        # Get the most recent test
                        if advanced_features.ab_test_results:
                            test_id = list(advanced_features.ab_test_results.keys())[-1]
                            preferred_model_id = model_a_id if preference == "Model A" else (model_b_id if preference == "Model B" else None)
                            
                            if preferred_model_id:
                                if advanced_features.record_ab_test_preference(test_id, preferred_model_id, reason):
                                    return f"✅ Preference recorded for {preference}. Thank you for your feedback!"
                                else:
                                    return "❌ Failed to record preference."
                            else:
                                return "Preference recorded as tie."
                        else:
                            return "No A/B test found to record preference for."
                            
                    except Exception as e:
                        return f"Error recording preference: {str(e)}"
                
                def show_ab_statistics():
                    stats = advanced_features.get_ab_test_statistics()
                    
                    output = "## A/B Test Statistics\n\n"
                    output += f"**Total Tests Run**: {stats['total_tests']}\n\n"
                    
                    if stats['model_wins']:
                        output += "### Model Win Rates:\n\n"
                        sorted_wins = sorted(stats['win_rates'].items(), key=lambda x: x[1], reverse=True)
                        for model, win_rate in sorted_wins:
                            wins = stats['model_wins'][model]
                            model_info = model_config.get_model_info(model, {})
                            model_name = model_info.get('name', model)
                            output += f"- **{model_name}**: {win_rate:.1f}% ({wins} wins)\n"
                        
                        # Get recommendation
                        recommended = advanced_features.get_model_recommendation("comprehensive")
                        rec_info = model_config.get_model_info(recommended, {})
                        output += f"\n### Recommended Model\n\nBased on your preferences, we recommend: **{rec_info.get('name', recommended)}**"
                    else:
                        output += "No test data available yet. Run A/B tests to build statistics."
                    
                    return output
                
                run_ab_test_btn.click(run_ab_test, inputs=[ab_test_paper_input, model_a_selector, model_b_selector, analysis_type_selector], outputs=[ab_test_output])
                record_preference_btn.click(record_preference, inputs=[ab_test_paper_input, model_a_selector, model_b_selector, preferred_model, preference_reason], outputs=[preference_status])
                ab_statistics_btn.click(show_ab_statistics, outputs=[ab_statistics_output])
            
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
            
            # ==================== CITATION GRAPH VISUALIZATION TAB ====================
            with gr.Tab("🕸️ Citation Graph Visualization"):
                gr.Markdown("## Interactive Citation Network Visualization")
                
                gr.Markdown("""
                **Visualize Citation Relationships:**
                - **Network Graph**: Interactive network showing paper relationships
                - **Node Analysis**: Papers sized by citation count
                - **Color Coding**: Different colors for paper types and sources
                - **Statistics**: Comprehensive graph statistics and metrics
                """)
                
                graph_paper_input = gr.Textbox(
                    label="Paper Details (JSON)",
                    placeholder='{"title": "Paper Title", "abstract": "...", "year": "2023", "citationCount": 100}',
                    lines=3
                )
                
                graph_recommendations_input = gr.Textbox(
                    label="Recommendations (JSON Array, optional)",
                    placeholder='[{"title": "Related Paper 1", ...}, {"title": "Related Paper 2", ...}]',
                    lines=3
                )
                
                layout_selector = gr.Radio(
                    choices=["spring", "circular", "kamada_kawai"],
                    value="spring",
                    label="Graph Layout"
                )
                
                generate_graph_btn = gr.Button("🕸️ Generate Citation Graph", variant="primary")
                
                with gr.Row():
                    network_plot_output = gr.Plot(label="Citation Network")
                    stats_plot_output = gr.Plot(label="Graph Statistics")
                
                graph_stats_output = gr.Markdown()
                
                def generate_citation_graph(paper_json, recommendations_json, layout):
                    if not paper_json:
                        return None, None, "❌ Please enter paper details in JSON format."
                    
                    try:
                        paper = json.loads(paper_json)
                        recommendations = json.loads(recommendations_json) if recommendations_json else None
                        
                        # Analyze and create visualizations
                        analysis = citation_engine.analyze_paper_citations(paper, recommendations)
                        
                        # Update graph layout
                        citation_engine.visualizer = CitationGraphVisualizer(citation_engine.graph_builder)
                        network_plot = citation_engine.visualizer.create_interactive_plot(layout=layout)
                        stats_plot = citation_engine.visualizer.create_statistics_plot()
                        
                        # Format statistics
                        stats = analysis['statistics']
                        stats_text = "## Citation Graph Statistics\n\n"
                        stats_text += f"- **Total Papers**: {stats['total_nodes']}\n"
                        stats_text += f"- **Total Relationships**: {stats['total_edges']}\n"
                        stats_text += f"- **Network Connected**: {'Yes' if stats['is_connected'] else 'No'}\n"
                        stats_text += f"- **Average Clustering**: {stats['average_clustering']:.3f}\n\n"
                        
                        stats_text += "### Paper Types:\n"
                        for node_type, count in stats['node_types'].items():
                            stats_text += f"- **{node_type}**: {count}\n"
                        
                        return network_plot, stats_plot, stats_text
                        
                    except json.JSONDecodeError:
                        return None, None, "❌ Invalid JSON format. Please provide valid JSON."
                    except Exception as e:
                        error_info = error_handler.handle_error(e, {"function": "generate_citation_graph"})
                        return None, None, f"❌ {error_info['user_message']}\n\n💡 {error_info['recovery_suggestion']}"
                
                generate_graph_btn.click(generate_citation_graph, inputs=[graph_paper_input, graph_recommendations_input, layout_selector], outputs=[network_plot_output, stats_plot_output, graph_stats_output])
                
                gr.Markdown("---")
                gr.Markdown("### 📊 Multi-Paper Comparison Graph")
                
                comparison_papers_input = gr.Textbox(
                    label="Multiple Papers (JSON Array)",
                    placeholder='[{"title": "Paper 1", "topics": ["ml", "nlp"]}, {"title": "Paper 2", "topics": ["ml", "cv"]}]',
                    lines=5
                )
                
                comparison_btn = gr.Button("🔗 Create Comparison Graph", variant="secondary")
                comparison_plot_output = gr.Plot(label="Paper Comparison Network")
                comparison_stats_output = gr.Markdown()
                
                def create_comparison_graph(papers_json):
                    if not papers_json:
                        return None, "❌ Please enter papers in JSON array format."
                    
                    try:
                        papers = json.loads(papers_json)
                        
                        # Create comparison graph
                        analysis = citation_engine.create_comparison_graph(papers)
                        
                        # Format statistics
                        stats = analysis['statistics']
                        stats_text = "## Comparison Graph Statistics\n\n"
                        stats_text += f"- **Total Papers**: {stats['total_nodes']}\n"
                        stats_text += f"- **Similarity Relationships**: {stats['total_edges']}\n"
                        stats_text += f"- **Network Connected**: {'Yes' if stats['is_connected'] else 'No'}\n"
                        
                        return analysis['network_plot'], stats_text
                        
                    except json.JSONDecodeError:
                        return None, "❌ Invalid JSON array format."
                    except Exception as e:
                        error_info = error_handler.handle_error(e, {"function": "create_comparison_graph"})
                        return None, f"❌ {error_info['user_message']}\n\n💡 {error_info['recovery_suggestion']}"
                
                comparison_btn.click(create_comparison_graph, inputs=[comparison_papers_input], outputs=[comparison_plot_output, comparison_stats_output])
            
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
                export_output = gr.Code(language="markdown", label="Export Output")
                
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
                            bibtex += f"@article{{{key}}},\n"
                            bibtex += f"  title = {{{{paper['title']}}}},\n"
                            bibtex += f"  year = {{{{paper['year']}}}},\n"
                            bibtex += f"  url = {{{{paper['url']}}}}\n"
                            bibtex += "}\n\n"
                        return bibtex
                
                export_btn.click(export_reading_list, inputs=[export_user_id, export_format], outputs=[export_output])
            
            # ==================== ABOUT TAB ====================
            with gr.Tab("ℹ️ About"):
                gr.Markdown("## About Enhanced Research Assistant\n\n")
                gr.Markdown("### Features\n")
                gr.Markdown("- **🤖 Model Selection**: Choose from multiple AI models for analysis\n")
                gr.Markdown("- **⚖️ Model Comparison**: Compare models side-by-side\n")
                gr.Markdown("- **📦 Batch Processing**: Process multiple papers at once\n")
                gr.Markdown("- **✏️ Custom Prompts**: Define your own analysis prompts\n")
                gr.Markdown("- **🎯 Auto Model Selection**: Automatic model selection based on complexity\n")
                gr.Markdown("- **🧪 A/B Testing**: Compare model performance on your papers\n")
                gr.Markdown("- **Multi-Source Recommendations**: Semantic Scholar, arXiv, citation-based\n")
                gr.Markdown("- **Reading List Management**: Organize papers by status and priority\n")
                gr.Markdown("- **Notes & Annotations**: Personal notes for each paper\n")
                gr.Markdown("- **Citation Analysis**: Impact scoring and trend analysis\n")
                gr.Markdown("- **Export Options**: BibTeX, JSON, Markdown formats\n")
                gr.Markdown("\n### AI Models Available\n")
                gr.Markdown("- **Rule-Based**: Free, no API needed (basic analysis)\n")
                gr.Markdown("- **GPT-4o Mini**: Low cost, advanced analysis (OpenAI API key)\n")
                gr.Markdown("- **Claude 3 Haiku**: Low cost, advanced analysis (Anthropic API key)\n")
                gr.Markdown("- **Ollama Models**: Free local models (Llama 3, Mistral, Mixtral)\n")
                gr.Markdown("- **Hugging Face**: Free inference API models\n")
                gr.Markdown("- **Google AI**: Gemini Pro and 1.5 Pro (Google API key)\n")
                gr.Markdown("\n### Technology\n")
                gr.Markdown("- Gradio 4.0+ Interface\n")
                gr.Markdown("- Multi-source recommendation APIs\n")
                gr.Markdown("- Local data storage for privacy\n")
                gr.Markdown("- Optional AI model integration\n")
                gr.Markdown("- A/B testing and model optimization\n")
                gr.Markdown("\n### Research Focus\n")
                gr.Markdown("This assistant focuses on research workflow automation and paper discovery with optional AI-powered analysis, model comparison, and performance optimization for deeper insights.")
    
    return demo

# ==================== MAIN ENTRY POINT ====================

if __name__ == "__main__":
    demo = create_research_assistant()
    
    # Custom CSS for responsive design and mobile optimization
    custom_css = """
    /* Mobile Optimization */
    @media (max-width: 768px) {
        .gradio-container {
            padding: 10px !important;
        }
        
        .tab-nav {
            flex-wrap: wrap !important;
        }
        
        .tab-nav button {
            flex: 1 1 auto !important;
            min-width: 80px !important;
            font-size: 12px !important;
            padding: 8px 4px !important;
        }
        
        .gr-button {
            width: 100% !important;
            margin: 5px 0 !important;
        }
        
        .gr-textbox, .gr-dropdown {
            width: 100% !important;
        }
        
        .gr-row {
            flex-direction: column !important;
        }
        
        .gr-column {
            width: 100% !important;
            margin: 5px 0 !important;
        }
        
        /* Improve plot visibility on mobile */
        .gr-plot {
            min-height: 300px !important;
        }
    }
    
    /* Tablet Optimization */
    @media (min-width: 769px) and (max-width: 1024px) {
        .gradio-container {
            padding: 15px !important;
        }
        
        .gr-row {
            flex-wrap: wrap !important;
        }
        
        .gr-column {
            flex: 1 1 45% !important;
            margin: 5px !important;
        }
    }
    
    /* General Improvements */
    .gradio-container {
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    
    /* Better spacing */
    .gr-form {
        gap: 15px !important;
    }
    
    /* Improved button styling */
    .gr-button-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        font-weight: 600 !important;
        transition: transform 0.2s !important;
    }
    
    .gr-button-primary:hover {
        transform: translateY(-2px) !important;
    }
    
    /* Card-like styling for containers */
    .gr-box {
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Better typography */
    .gr-markdown {
        line-height: 1.6 !important;
    }
    
    /* Improved input fields */
    .gr-textbox:focus, .gr-dropdown:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Loading animation */
    .gr-loading {
        border-top-color: #667eea !important;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .gradio-container {
            background-color: #1a1a1a !important;
            color: #e0e0e0 !important;
        }
        
        .gr-box {
            background-color: #2d2d2d !important;
            border-color: #404040 !important;
        }
        
        .gr-textbox, .gr-dropdown {
            background-color: #2d2d2d !important;
            color: #e0e0e0 !important;
            border-color: #404040 !important;
        }
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth !important;
    }
    
    /* Better tab navigation */
    .tab-nav {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }
    
    /* Responsive tables */
    .gr-dataframe {
        overflow-x: auto !important;
    }
    
    /* Touch-friendly targets */
    .gr-button, .gr-dropdown, .gr-checkbox {
        min-height: 44px !important;
    }
    
    /* Print-friendly */
    @media print {
        .gr-button, .tab-nav {
            display: none !important;
        }
        
        .gradio-container {
            width: 100% !important;
            max-width: none !important;
        }
    }
    """
    
    demo.launch(css=custom_css, theme=gr.themes.Soft())
