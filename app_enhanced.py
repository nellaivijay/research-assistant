import gradio as gr
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import re
import os

# ==================== MODEL CONFIGURATION ====================

class ModelConfig:
    """Manage AI model configurations and API keys"""
    
    def __init__(self):
        self.models = {
            # Free/Default Models
            "rule_based": {
                "name": "Rule-Based Analysis",
                "type": "local",
                "cost": "Free",
                "description": "Pattern matching and keyword extraction (no API needed)",
                "capabilities": ["basic_analysis", "topic_identification", "citation_analysis"]
            },
            # OpenAI Models
            "gpt-4o-mini": {
                "name": "GPT-4o Mini",
                "type": "openai",
                "cost": "Low",
                "description": "Fast, efficient model for paper analysis",
                "api_key_env": "OPENAI_API_KEY",
                "capabilities": ["advanced_analysis", "summarization", "topic_modeling", "insight_generation"]
            },
            "gpt-4o": {
                "name": "GPT-4o",
                "type": "openai",
                "cost": "Medium",
                "description": "Most capable model for deep research analysis",
                "api_key_env": "OPENAI_API_KEY",
                "capabilities": ["advanced_analysis", "summarization", "topic_modeling", "insight_generation", "comparison_analysis"]
            },
            # Anthropic Models
            "claude-3-haiku": {
                "name": "Claude 3 Haiku",
                "type": "anthropic",
                "cost": "Low",
                "description": "Fast and efficient for quick analysis",
                "api_key_env": "ANTHROPIC_API_KEY",
                "capabilities": ["advanced_analysis", "summarization", "topic_modeling"]
            },
            "claude-3-sonnet": {
                "name": "Claude 3 Sonnet",
                "type": "anthropic",
                "cost": "Medium",
                "description": "Balanced performance for research tasks",
                "api_key_env": "ANTHROPIC_API_KEY",
                "capabilities": ["advanced_analysis", "summarization", "topic_modeling", "insight_generation"]
            },
            # Google Models
            "gemini-pro": {
                "name": "Gemini Pro",
                "type": "google",
                "cost": "Low",
                "description": "Google's capable model for analysis",
                "api_key_env": "GOOGLE_API_KEY",
                "capabilities": ["advanced_analysis", "summarization", "topic_modeling"]
            },
            # Local Models (Ollama)
            "llama3": {
                "name": "Llama 3 (Local)",
                "type": "local_ollama",
                "cost": "Free",
                "description": "Local model via Ollama (requires Ollama installation)",
                "api_endpoint": "http://localhost:11434/api/generate",
                "capabilities": ["advanced_analysis", "summarization", "topic_modeling"]
            },
            "mistral": {
                "name": "Mistral (Local)",
                "type": "local_ollama",
                "cost": "Free",
                "description": "Local model via Ollama (requires Ollama installation)",
                "api_endpoint": "http://localhost:11434/api/generate",
                "capabilities": ["advanced_analysis", "summarization", "topic_modeling"]
            },
            # Hugging Face Inference
            "hf-mistral-7b": {
                "name": "Mistral 7B (HF Inference)",
                "type": "huggingface",
                "cost": "Free/Low",
                "description": "Hugging Face free inference API",
                "model_id": "mistralai/Mistral-7B-Instruct-v0.2",
                "api_key_env": "HF_TOKEN",
                "capabilities": ["advanced_analysis", "summarization", "topic_modeling"]
            }
        }
    
    def get_available_models(self, capability_filter: str = None) -> Dict:
        """Get available models, optionally filtered by capability"""
        if capability_filter:
            return {
                k: v for k, v in self.models.items()
                if capability_filter in v.get("capabilities", [])
            }
        return self.models
    
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

# Initialize model configuration
model_config = ModelConfig()

# ==================== ENHANCED ANALYSIS ENGINE ====================

class EnhancedAnalysisEngine:
    """Enhanced analysis with multiple model support"""
    
    def __init__(self):
        self.current_model = "rule_based"  # Default to rule-based
        self.model_config = model_config
    
    def set_model(self, model_id: str) -> bool:
        """Set the active analysis model"""
        if model_id in self.model_config.models:
            self.current_model = model_id
            return True
        return False
    
    def analyze_paper(self, paper: Dict, analysis_type: str = "comprehensive") -> Dict:
        """Analyze paper using current model"""
        model_info = self.model_config.get_model_info(self.current_model)
        model_type = model_info.get("type")
        
        if model_type == "local":
            return self._rule_based_analysis(paper)
        elif model_type == "openai":
            return self._openai_analysis(paper, self.current_model, analysis_type)
        elif model_type == "anthropic":
            return self._anthropic_analysis(paper, self.current_model, analysis_type)
        elif model_type == "google":
            return self._google_analysis(paper, self.current_model, analysis_type)
        elif model_type == "local_ollama":
            return self._ollama_analysis(paper, self.current_model, analysis_type)
        elif model_type == "huggingface":
            return self._huggingface_analysis(paper, self.current_model, analysis_type)
        else:
            return self._rule_based_analysis(paper)
    
    def _rule_based_analysis(self, paper: Dict) -> Dict:
        """Original rule-based analysis"""
        return {
            "impact_score": self._calculate_impact_score(paper),
            "readability_score": self._calculate_readability(paper),
            "citation_velocity": self._estimate_citation_velocity(paper),
            "key_contributions": self._extract_key_contributions(paper),
            "related_topics": self._identify_topics(paper),
            "model_used": "rule_based",
            "analysis_depth": "basic"
        }
    
    def _openai_analysis(self, paper: Dict, model: str, analysis_type: str) -> Dict:
        """Analysis using OpenAI API"""
        try:
            import openai
            client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            
            prompt = self._build_analysis_prompt(paper, analysis_type)
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert research assistant specializing in academic paper analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            analysis_text = response.choices[0].message.content
            return self._parse_ai_analysis(analysis_text, model)
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._rule_based_analysis(paper)
    
    def _anthropic_analysis(self, paper: Dict, model: str, analysis_type: str) -> Dict:
        """Analysis using Anthropic API"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            
            prompt = self._build_analysis_prompt(paper, analysis_type)
            
            response = client.messages.create(
                model=model,
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            analysis_text = response.content[0].text
            return self._parse_ai_analysis(analysis_text, model)
            
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return self._rule_based_analysis(paper)
    
    def _google_analysis(self, paper: Dict, model: str, analysis_type: str) -> Dict:
        """Analysis using Google API"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
            
            model_instance = genai.GenerativeModel(model)
            prompt = self._build_analysis_prompt(paper, analysis_type)
            
            response = model_instance.generate_content(prompt)
            analysis_text = response.text
            return self._parse_ai_analysis(analysis_text, model)
            
        except Exception as e:
            print(f"Google API error: {e}")
            return self._rule_based_analysis(paper)
    
    def _ollama_analysis(self, paper: Dict, model: str, analysis_type: str) -> Dict:
        """Analysis using local Ollama model"""
        try:
            prompt = self._build_analysis_prompt(paper, analysis_type)
            
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                analysis_text = response.json().get("response", "")
                return self._parse_ai_analysis(analysis_text, model)
            else:
                return self._rule_based_analysis(paper)
                
        except Exception as e:
            print(f"Ollama error: {e}")
            return self._rule_based_analysis(paper)
    
    def _huggingface_analysis(self, paper: Dict, model: str, analysis_type: str) -> Dict:
        """Analysis using Hugging Face Inference API"""
        try:
            model_info = self.model_config.get_model_info(model)
            model_id = model_info.get("model_id")
            
            prompt = self._build_analysis_prompt(paper, analysis_type)
            
            API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
            headers = {"Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"}
            
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
            
            if response.status_code == 200:
                analysis_text = response.json()[0].get("generated_text", "")
                return self._parse_ai_analysis(analysis_text, model)
            else:
                return self._rule_based_analysis(paper)
                
        except Exception as e:
            print(f"Hugging Face API error: {e}")
            return self._rule_based_analysis(paper)
    
    def _build_analysis_prompt(self, paper: Dict, analysis_type: str) -> str:
        """Build analysis prompt for AI models"""
        title = paper.get("title", "Unknown")
        abstract = paper.get("abstract", "No abstract available")
        year = paper.get("year", "Unknown")
        citations = paper.get("citationCount", 0)
        
        if analysis_type == "comprehensive":
            prompt = f"""Analyze this academic paper comprehensively:

Title: {title}
Year: {year}
Citations: {citations}
Abstract: {abstract}

Please provide:
1. Impact assessment (1-10 scale with reasoning)
2. Key contributions (3-5 main contributions)
3. Research topics (3-5 relevant topics)
4. Novelty assessment (how novel is this work?)
5. Technical complexity (basic/intermediate/advanced)
6. Potential applications (2-3 practical applications)
7. Related research areas (2-3 related fields)
8. Reading difficulty (easy/medium/hard)

Format your response as structured JSON."""
        
        elif analysis_type == "summarization":
            prompt = f"""Provide a concise summary of this paper:

Title: {title}
Abstract: {abstract}

Include: main problem, approach, key results, and significance."""
        
        elif analysis_type == "topic_modeling":
            prompt = f"""Identify the research topics and themes in this paper:

Title: {title}
Abstract: {abstract}

List 5-7 specific research topics and explain why each is relevant."""
        
        else:
            prompt = f"""Analyze this paper:

Title: {title}
Abstract: {abstract}

Provide insights about the research significance, methodology, and potential impact."""
        
        return prompt
    
    def _parse_ai_analysis(self, analysis_text: str, model: str) -> Dict:
        """Parse AI model analysis response"""
        # Try to extract JSON from response
        try:
            # Look for JSON patterns in the response
            import re
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                parsed["model_used"] = model
                parsed["analysis_depth"] = "advanced"
                return parsed
        except:
            pass
        
        # Fallback: return text-based analysis
        return {
            "analysis_text": analysis_text,
            "model_used": model,
            "analysis_depth": "advanced",
            "structured_data": False
        }
    
    def _calculate_impact_score(self, paper: Dict) -> float:
        """Calculate impact score based on citations and recency"""
        citations = paper.get("citationCount", 0)
        year = int(paper.get("year", 2020))
        current_year = datetime.now().year
        
        age = max(1, current_year - year)
        impact_score = citations / age
        
        return round(impact_score, 2)
    
    def _calculate_readability(self, paper: Dict) -> str:
        """Estimate readability based on abstract"""
        abstract = paper.get("abstract", "")
        if not abstract:
            return "Unknown"
        
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
        
        contributions = []
        contribution_keywords = ["introduce", "propose", "present", "develop", "create", "novel", "new approach"]
        sentences = abstract.split(".")
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in contribution_keywords):
                contributions.append(sentence.strip())
        
        return contributions[:3]
    
    def _identify_topics(self, paper: Dict) -> List[str]:
        """Identify research topics from paper"""
        title = paper.get("title", "").lower()
        abstract = paper.get("abstract", "").lower()
        text = title + " " + abstract
        
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

# Initialize enhanced analysis engine
analysis_engine = EnhancedAnalysisEngine()

# ==================== API KEY MANAGEMENT ====================

class APIKeyManager:
    """Manage API keys for different services"""
    
    def __init__(self):
        self.config_file = Path("data/api_keys.json")
        self.config_file.parent.mkdir(exist_ok=True)
        self.keys = self._load_keys()
    
    def _load_keys(self) -> Dict:
        """Load API keys from storage"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_key(self, service: str, key: str) -> bool:
        """Save API key for a service"""
        try:
            self.keys[service] = key
            with open(self.config_file, 'w') as f:
                json.dump(self.keys, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving key: {e}")
            return False
    
    def get_key(self, service: str) -> Optional[str]:
        """Get API key for a service"""
        return self.keys.get(service)
    
    def set_environment_key(self, service: str) -> bool:
        """Set API key as environment variable"""
        key = self.get_key(service)
        if key:
            env_var_map = {
                "openai": "OPENAI_API_KEY",
                "anthropic": "ANTHROPIC_API_KEY",
                "google": "GOOGLE_API_KEY",
                "huggingface": "HF_TOKEN"
            }
            env_var = env_var_map.get(service)
            if env_var:
                os.environ[env_var] = key
                return True
        return False

# Initialize API key manager
key_manager = APIKeyManager()

# ==================== ENHANCED GRADIO INTERFACE ====================

def create_enhanced_research_assistant():
    """Create enhanced research assistant with model selection"""
    
    with gr.Blocks(title="Enhanced Research Assistant - AI Model Selection") as demo:
        
        # Header
        gr.Markdown("# 📚 Enhanced Research Assistant - AI Model Selection")
        gr.Markdown("Advanced research companion with custom AI model selection and multi-source recommendations")
        
        with gr.Tabs():
            # ==================== MODEL SELECTION TAB ====================
            with gr.Tab("🤖 Model Selection"):
                gr.Markdown("## Select Your AI Model for Analysis")
                
                with gr.Row():
                    model_selector = gr.Dropdown(
                        choices=[f"{info['name']} ({model_id})" for model_id, info in model_config.get_available_models().items()],
                        value="rule_based (rule_based)",
                        label="Select Analysis Model"
                    )
                    model_info_display = gr.Markdown()
                
                def update_model_info(model_selection):
                    model_id = model_selection.split("(")[-1].replace(")", "")
                    info = model_config.get_model_info(model_id)
                    
                    if info:
                        output = f"### {info['name']}\n\n"
                        output += f"- **Type**: {info['type']}\n"
                        output += f"- **Cost**: {info['cost']}\n"
                        output += f"- **Description**: {info['description']}\n"
                        output += f"- **Capabilities**: {', '.join(info.get('capabilities', []))}\n"
                        
                        # Check API key status
                        if info.get("api_key_env"):
                            api_key_env = info['api_key_env']
                            has_key = bool(os.environ.get(api_key_env))
                            status = "✅ Configured" if has_key else "❌ Not configured"
                            output += f"- **API Key Status**: {status}\n"
                        
                        return output
                    return "Model information not available."
                
                model_selector.change(update_model_info, inputs=[model_selector], outputs=[model_info_display])
                
                gr.Markdown("### API Key Configuration")
                gr.Markdown("Configure API keys for different AI models (keys are stored locally)")
                
                with gr.Row():
                    service_selector = gr.Dropdown(
                        choices=["OpenAI", "Anthropic", "Google", "Hugging Face"],
                        label="Service"
                    )
                    api_key_input = gr.Textbox(
                        label="API Key",
                        type="password",
                        placeholder="Enter your API key"
                    )
                    save_key_btn = gr.Button("Save API Key", variant="primary")
                
                key_status = gr.Markdown()
                
                def save_api_key(service, key):
                    if not key:
                        return "Please enter an API key."
                    
                    service_map = {
                        "OpenAI": "openai",
                        "Anthropic": "anthropic", 
                        "Google": "google",
                        "Hugging Face": "huggingface"
                    }
                    
                    service_id = service_map.get(service, service.lower())
                    if key_manager.save_key(service_id, key):
                        key_manager.set_environment_key(service_id)
                        return f"✅ API key saved for {service}"
                    return "❌ Failed to save API key"
                
                save_key_btn.click(save_api_key, inputs=[service_selector, api_key_input], outputs=[key_status])
            
            # ==================== PAPER ANALYSIS WITH MODEL TAB ====================
            with gr.Tab("📊 Enhanced Analysis"):
                gr.Markdown("## Advanced Paper Analysis with Custom Models")
                
                with gr.Row():
                    analysis_model_selector = gr.Dropdown(
                        choices=[f"{info['name']} ({model_id})" for model_id, info in model_config.get_available_models().items()],
                        value="rule_based (rule_based)",
                        label="Select Analysis Model"
                    )
                    analysis_type_selector = gr.Dropdown(
                        choices=["comprehensive", "summarization", "topic_modeling", "quick"],
                        value="comprehensive",
                        label="Analysis Type"
                    )
                
                paper_input = gr.Textbox(
                    label="Paper Details (JSON)",
                    placeholder='{"title": "Paper Title", "abstract": "...", "year": "2023", "citationCount": 100}',
                    lines=3
                )
                
                analyze_btn = gr.Button("Analyze with Selected Model", variant="primary")
                analysis_output = gr.Markdown()
                
                def analyze_with_model(model_selection, analysis_type, paper_json):
                    if not paper_json:
                        return "Please enter paper details in JSON format."
                    
                    try:
                        paper = json.loads(paper_json)
                        model_id = model_selection.split("(")[-1].replace(")", "")
                        
                        # Set the model
                        analysis_engine.set_model(model_id)
                        
                        # Perform analysis
                        analysis = analysis_engine.analyze_paper(paper, analysis_type)
                        
                        # Format output
                        output = f"## Analysis Results\n\n"
                        output += f"**Model Used**: {analysis.get('model_used', 'unknown')}\n"
                        output += f"**Analysis Depth**: {analysis.get('analysis_depth', 'unknown')}\n\n"
                        
                        if analysis.get('structured_data'):
                            # Structured data from AI model
                            for key, value in analysis.items():
                                if key not in ['model_used', 'analysis_depth', 'structured_data']:
                                    output += f"**{key.replace('_', ' ').title()}**: {value}\n"
                        elif analysis.get('analysis_text'):
                            # Text-based analysis
                            output += f"### AI Analysis\n\n{analysis['analysis_text']}"
                        else:
                            # Rule-based analysis
                            output += f"- **Impact Score**: {analysis.get('impact_score', 'N/A')}\n"
                            output += f"- **Readability**: {analysis.get('readability_score', 'N/A')}\n"
                            output += f"- **Citation Velocity**: {analysis.get('citation_velocity', 'N/A')}\n"
                            output += f"- **Topics**: {', '.join(analysis.get('related_topics', []))}\n"
                            
                            if analysis.get('key_contributions'):
                                output += "\n### Key Contributions\n"
                                for contribution in analysis['key_contributions']:
                                    output += f"- {contribution}\n"
                        
                        return output
                        
                    except json.JSONDecodeError:
                        return "Invalid JSON format. Please provide valid JSON."
                    except Exception as e:
                        return f"Error during analysis: {str(e)}"
                
                analyze_btn.click(analyze_with_model, inputs=[analysis_model_selector, analysis_type_selector, paper_input], outputs=[analysis_output])
            
            # ==================== MODEL COMPARISON TAB ====================
            with gr.Tab("⚖️ Model Comparison"):
                gr.Markdown("## Compare Different AI Models")
                
                gr.Markdown("Analyze the same paper with different models to compare results")
                
                comparison_paper_input = gr.Textbox(
                    label="Paper Details (JSON)",
                    placeholder='{"title": "Paper Title", "abstract": "...", "year": "2023", "citationCount": 100}',
                    lines=3
                )
                
                models_to_compare = gr.CheckboxGroup(
                    choices=["rule_based", "gpt-4o-mini", "claude-3-haiku", "gemini-pro"],
                    value=["rule_based", "gpt-4o-mini"],
                    label="Models to Compare"
                )
                
                compare_btn = gr.Button("Compare Models", variant="primary")
                comparison_output = gr.Markdown()
                
                def compare_models(paper_json, models):
                    if not paper_json:
                        return "Please enter paper details in JSON format."
                    
                    try:
                        paper = json.loads(paper_json)
                        results = {}
                        
                        for model_id in models:
                            analysis_engine.set_model(model_id)
                            analysis = analysis_engine.analyze_paper(paper, "comprehensive")
                            results[model_id] = analysis
                        
                        # Format comparison
                        output = "## Model Comparison Results\n\n"
                        
                        for model_id, analysis in results.items():
                            model_info = model_config.get_model_info(model_id)
                            model_name = model_info.get('name', model_id)
                            
                            output += f"### {model_name}\n"
                            output += f"- **Analysis Depth**: {analysis.get('analysis_depth', 'unknown')}\n"
                            
                            if analysis.get('impact_score'):
                                output += f"- **Impact Score**: {analysis['impact_score']}\n"
                            if analysis.get('readability_score'):
                                output += f"- **Readability**: {analysis['readability_score']}\n"
                            if analysis.get('citation_velocity'):
                                output += f"- **Citation Velocity**: {analysis['citation_velocity']}\n"
                            if analysis.get('related_topics'):
                                output += f"- **Topics**: {', '.join(analysis['related_topics'])}\n"
                            if analysis.get('analysis_text'):
                                output += f"- **Summary**: {analysis['analysis_text'][:200]}...\n"
                            
                            output += "\n"
                        
                        return output
                        
                    except json.JSONDecodeError:
                        return "Invalid JSON format. Please provide valid JSON."
                    except Exception as e:
                        return f"Error during comparison: {str(e)}"
                
                compare_btn.click(compare_models, inputs=[comparison_paper_input, models_to_compare], outputs=[comparison_output])
            
            # ==================== ORIGINAL TABS ====================
            with gr.Tab("🔍 Paper Recommendations"):
                gr.Markdown("## Multi-Source Paper Recommendations (Original Feature)")
                gr.Markdown("*Use the enhanced analysis features for deeper insights*")
                
                paper_rec_input = gr.Textbox(label="Paper ID or arXiv URL")
                recommend_rec_btn = gr.Button("Get Recommendations", variant="primary")
                recommendations_output = gr.Markdown()
                
                def get_recommendations_simple(paper_id):
                    return "Recommendations feature - integrate with existing recommendation engine"
                
                recommend_rec_btn.click(get_recommendations_simple, inputs=[paper_rec_input], outputs=[recommendations_output])
        
        return demo

if __name__ == "__main__":
    demo = create_enhanced_research_assistant()
    demo.launch()
