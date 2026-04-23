"""
AI Service Module - Handles actual API calls to various AI providers
"""
import os
import json
from typing import Dict, List, Optional, Union
from datetime import datetime
import requests


class AIService:
    """Base class for AI services"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get(self.api_key_env)
        self.is_available = bool(self.api_key)
    
    def analyze_paper(self, paper: Dict, analysis_type: str = "comprehensive") -> Dict:
        """Analyze a paper using the AI service"""
        raise NotImplementedError("Subclasses must implement analyze_paper")
    
    def check_availability(self) -> bool:
        """Check if the service is available"""
        return self.is_available


class OpenAIService(AIService):
    """OpenAI API integration"""
    
    api_key_env = "OPENAI_API_KEY"
    base_url = "https://api.openai.com/v1"
    
    def __init__(self, model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        super().__init__(api_key)
        self.model = model
    
    def analyze_paper(self, paper: Dict, analysis_type: str = "comprehensive") -> Dict:
        """Analyze paper using OpenAI API"""
        if not self.is_available:
            return {
                "error": "OpenAI API key not available",
                "analysis": self._fallback_analysis(paper)
            }
        
        try:
            # Prepare the prompt based on analysis type
            prompt = self._prepare_prompt(paper, analysis_type)
            
            # Make API call
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a research assistant that analyzes academic papers."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return self._parse_analysis_response(content, paper)
            else:
                error_msg = f"OpenAI API error: {response.status_code}"
                if response.text:
                    error_msg += f" - {response.text}"
                return {
                    "error": error_msg,
                    "analysis": self._fallback_analysis(paper)
                }
                
        except requests.exceptions.Timeout:
            return {
                "error": "OpenAI API request timed out",
                "analysis": self._fallback_analysis(paper)
            }
        except Exception as e:
            return {
                "error": f"OpenAI API error: {str(e)}",
                "analysis": self._fallback_analysis(paper)
            }
    
    def _prepare_prompt(self, paper: Dict, analysis_type: str) -> str:
        """Prepare the prompt for the AI model"""
        title = paper.get("title", "Unknown")
        abstract = paper.get("abstract", "No abstract available")
        year = paper.get("year", "Unknown")
        
        if analysis_type == "comprehensive":
            return f"""
Analyze the following academic paper comprehensively:

Title: {title}
Year: {year}
Abstract: {abstract}

Please provide:
1. A brief summary of the paper's main contributions
2. Key technical approaches and methodologies
3. Potential applications and impact
4. Novelty and significance assessment
5. Related research topics
6. Suggested future work directions

Format your response as structured text with clear sections.
"""
        elif analysis_type == "summarization":
            return f"""
Provide a concise summary of this paper:

Title: {title}
Year: {year}
Abstract: {abstract}

Focus on the main contributions and key findings in 2-3 paragraphs.
"""
        elif analysis_type == "methodology":
            return f"""
Analyze the methodology of this paper:

Title: {title}
Year: {year}
Abstract: {abstract}

Focus on:
1. Technical approach and algorithms
2. Experimental setup
3. Evaluation metrics
4. Key innovations in the methodology
"""
        else:
            return f"Analyze this paper: {title}\n\nAbstract: {abstract}"
    
    def _parse_analysis_response(self, content: str, paper: Dict) -> Dict:
        """Parse the AI response into structured format"""
        return {
            "model_used": f"openai-{self.model}",
            "analysis_type": "ai_generated",
            "summary": content,
            "structured_data": {
                "title": paper.get("title", ""),
                "year": paper.get("year", ""),
                "analysis_timestamp": datetime.now().isoformat()
            },
            "raw_response": content
        }
    
    def _fallback_analysis(self, paper: Dict) -> Dict:
        """Fallback analysis when API is unavailable"""
        return {
            "model_used": "rule_based_fallback",
            "analysis_type": "basic",
            "summary": f"Basic analysis for: {paper.get('title', 'Unknown')}",
            "note": "AI analysis unavailable - using basic rule-based analysis"
        }


class AnthropicService(AIService):
    """Anthropic Claude API integration"""
    
    api_key_env = "ANTHROPIC_API_KEY"
    base_url = "https://api.anthropic.com/v1"
    
    def __init__(self, model: str = "claude-3-haiku", api_key: Optional[str] = None):
        super().__init__(api_key)
        self.model = model
    
    def analyze_paper(self, paper: Dict, analysis_type: str = "comprehensive") -> Dict:
        """Analyze paper using Anthropic API"""
        if not self.is_available:
            return {
                "error": "Anthropic API key not available",
                "analysis": self._fallback_analysis(paper)
            }
        
        try:
            prompt = self._prepare_prompt(paper, analysis_type)
            
            response = requests.post(
                f"{self.base_url}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "max_tokens": 1000,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["content"][0]["text"]
                return self._parse_analysis_response(content, paper)
            else:
                return {
                    "error": f"Anthropic API error: {response.status_code}",
                    "analysis": self._fallback_analysis(paper)
                }
                
        except Exception as e:
            return {
                "error": f"Anthropic API error: {str(e)}",
                "analysis": self._fallback_analysis(paper)
            }
    
    def _prepare_prompt(self, paper: Dict, analysis_type: str) -> str:
        """Prepare prompt for Claude"""
        title = paper.get("title", "Unknown")
        abstract = paper.get("abstract", "No abstract available")
        
        if analysis_type == "comprehensive":
            return f"Analyze this academic paper:\n\nTitle: {title}\nAbstract: {abstract}\n\nProvide comprehensive analysis including contributions, methodology, applications, and significance."
        else:
            return f"Analyze this paper: {title}\n\nAbstract: {abstract}"
    
    def _parse_analysis_response(self, content: str, paper: Dict) -> Dict:
        """Parse Claude response"""
        return {
            "model_used": f"anthropic-{self.model}",
            "analysis_type": "ai_generated",
            "summary": content,
            "structured_data": {
                "title": paper.get("title", ""),
                "analysis_timestamp": datetime.now().isoformat()
            }
        }
    
    def _fallback_analysis(self, paper: Dict) -> Dict:
        """Fallback analysis"""
        return {
            "model_used": "rule_based_fallback",
            "summary": f"Basic analysis for: {paper.get('title', 'Unknown')}"
        }


class GoogleAIService(AIService):
    """Google Gemini API integration"""
    
    api_key_env = "GOOGLE_API_KEY"
    base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    def __init__(self, model: str = "gemini-pro", api_key: Optional[str] = None):
        super().__init__(api_key)
        self.model = model
    
    def analyze_paper(self, paper: Dict, analysis_type: str = "comprehensive") -> Dict:
        """Analyze paper using Google Gemini API"""
        if not self.is_available:
            return {
                "error": "Google API key not available",
                "analysis": self._fallback_analysis(paper)
            }
        
        try:
            prompt = self._prepare_prompt(paper, analysis_type)
            
            response = requests.post(
                f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}",
                headers={"Content-Type": "application/json"},
                json={
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 1000
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                return self._parse_analysis_response(content, paper)
            else:
                return {
                    "error": f"Google API error: {response.status_code}",
                    "analysis": self._fallback_analysis(paper)
                }
                
        except Exception as e:
            return {
                "error": f"Google API error: {str(e)}",
                "analysis": self._fallback_analysis(paper)
            }
    
    def _prepare_prompt(self, paper: Dict, analysis_type: str) -> str:
        """Prepare prompt for Gemini"""
        title = paper.get("title", "Unknown")
        abstract = paper.get("abstract", "No abstract available")
        return f"Analyze this academic paper:\n\nTitle: {title}\nAbstract: {abstract}\n\nProvide comprehensive analysis."
    
    def _parse_analysis_response(self, content: str, paper: Dict) -> Dict:
        """Parse Gemini response"""
        return {
            "model_used": f"google-{self.model}",
            "analysis_type": "ai_generated",
            "summary": content,
            "structured_data": {
                "title": paper.get("title", ""),
                "analysis_timestamp": datetime.now().isoformat()
            }
        }
    
    def _fallback_analysis(self, paper: Dict) -> Dict:
        """Fallback analysis"""
        return {
            "model_used": "rule_based_fallback",
            "summary": f"Basic analysis for: {paper.get('title', 'Unknown')}"
        }


class OllamaService(AIService):
    """Local Ollama integration"""
    
    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.is_available = self._check_ollama_available()
    
    def _check_ollama_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def analyze_paper(self, paper: Dict, analysis_type: str = "comprehensive") -> Dict:
        """Analyze paper using local Ollama"""
        if not self.is_available:
            return {
                "error": "Ollama not available - make sure it's running locally",
                "analysis": self._fallback_analysis(paper)
            }
        
        try:
            prompt = self._prepare_prompt(paper, analysis_type)
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("response", "")
                return self._parse_analysis_response(content, paper)
            else:
                return {
                    "error": f"Ollama error: {response.status_code}",
                    "analysis": self._fallback_analysis(paper)
                }
                
        except Exception as e:
            return {
                "error": f"Ollama error: {str(e)}",
                "analysis": self._fallback_analysis(paper)
            }
    
    def _prepare_prompt(self, paper: Dict, analysis_type: str) -> str:
        """Prepare prompt for Ollama"""
        title = paper.get("title", "Unknown")
        abstract = paper.get("abstract", "No abstract available")
        return f"Analyze this academic paper:\n\nTitle: {title}\nAbstract: {abstract}\n\nProvide comprehensive analysis."
    
    def _parse_analysis_response(self, content: str, paper: Dict) -> Dict:
        """Parse Ollama response"""
        return {
            "model_used": f"ollama-{self.model}",
            "analysis_type": "ai_generated",
            "summary": content,
            "structured_data": {
                "title": paper.get("title", ""),
                "analysis_timestamp": datetime.now().isoformat()
            }
        }
    
    def _fallback_analysis(self, paper: Dict) -> Dict:
        """Fallback analysis"""
        return {
            "model_used": "rule_based_fallback",
            "summary": f"Basic analysis for: {paper.get('title', 'Unknown')}"
        }


class AIModelManager:
    """Manager for all AI services"""
    
    def __init__(self):
        self.services = {
            "openai": {
                "gpt-4o-mini": OpenAIService("gpt-4o-mini"),
                "gpt-4o": OpenAIService("gpt-4o")
            },
            "anthropic": {
                "claude-3-haiku": AnthropicService("claude-3-haiku"),
                "claude-3-sonnet": AnthropicService("claude-3-sonnet")
            },
            "google": {
                "gemini-pro": GoogleAIService("gemini-pro"),
                "gemini-1.5-pro": GoogleAIService("gemini-1.5-pro")
            },
            "ollama": {
                "llama3": OllamaService("llama3"),
                "llama3-70b": OllamaService("llama3-70b"),
                "mistral": OllamaService("mistral"),
                "mixtral": OllamaService("mixtral")
            }
        }
    
    def get_service(self, provider: str, model: str) -> Optional[AIService]:
        """Get a specific AI service"""
        if provider in self.services and model in self.services[provider]:
            return self.services[provider][model]
        return None
    
    def analyze_with_model(self, model_id: str, paper: Dict, analysis_type: str = "comprehensive") -> Dict:
        """Analyze paper using specific model"""
        # Map model IDs to services
        model_mapping = {
            "gpt-4o-mini": ("openai", "gpt-4o-mini"),
            "gpt-4o": ("openai", "gpt-4o"),
            "claude-3-haiku": ("anthropic", "claude-3-haiku"),
            "claude-3-sonnet": ("anthropic", "claude-3-sonnet"),
            "gemini-pro": ("google", "gemini-pro"),
            "gemini-1.5-pro": ("google", "gemini-1.5-pro"),
            "llama3": ("ollama", "llama3"),
            "llama3-70b": ("ollama", "llama3-70b"),
            "mistral": ("ollama", "mistral"),
            "mixtral": ("ollama", "mixtral")
        }
        
        if model_id in model_mapping:
            provider, model = model_mapping[model_id]
            service = self.get_service(provider, model)
            if service:
                return service.analyze_paper(paper, analysis_type)
        
        return {
            "error": f"Model {model_id} not available or not configured",
            "analysis": self._rule_based_analysis(paper)
        }
    
    def _rule_based_analysis(self, paper: Dict) -> Dict:
        """Fallback rule-based analysis"""
        title = paper.get("title", "Unknown")
        abstract = paper.get("abstract", "")
        
        # Simple rule-based analysis
        word_count = len(abstract.split())
        topics = self._extract_topics(title + " " + abstract)
        
        return {
            "model_used": "rule_based",
            "analysis_type": "basic",
            "summary": f"Rule-based analysis of: {title}",
            "word_count": word_count,
            "topics": topics,
            "readability": "Medium" if word_count > 200 else "Easy"
        }
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics using keyword matching"""
        topics = {
            "machine learning": ["machine learning", "ml", "neural network", "deep learning"],
            "nlp": ["nlp", "language model", "transformer", "bert", "gpt"],
            "computer vision": ["vision", "image", "convolutional", "cnn"],
            "reinforcement learning": ["reinforcement", "rl", "policy"]
        }
        
        found_topics = []
        text_lower = text.lower()
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                found_topics.append(topic)
        
        return found_topics


# Global AI manager instance
ai_manager = AIModelManager()