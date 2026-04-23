"""
Additional Data Sources Module
Integrates Google Scholar and PubMed APIs for expanded paper discovery
"""
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from datetime import datetime
import re
from error_handling import safe_api_call, NetworkError, APIError


class GoogleScholarAPI:
    """Google Scholar API integration for paper discovery"""
    
    def __init__(self):
        # Note: Google Scholar doesn't have an official public API
        # This implementation uses web scraping with proper headers
        self.base_url = "https://scholar.google.com/scholar"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_papers(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search for papers on Google Scholar"""
        try:
            params = {
                'q': query,
                'hl': 'en',
                'start': 0,
                'num': max_results
            }
            
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return self._parse_scholar_results(response.text)
            else:
                return []
                
        except Exception as e:
            print(f"Google Scholar search error: {e}")
            return []
    
    def _parse_scholar_results(self, html: str) -> List[Dict]:
        """Parse Google Scholar search results from HTML"""
        papers = []
        
        # Parse HTML content (simplified parsing)
        # In production, you'd want to use BeautifulSoup or similar
        try:
            # Extract paper information using regex patterns
            title_pattern = r'<h3[^>]*><a[^>]*>(.*?)</a>'
            author_pattern = r'<div[^>]*class="gs_a"[^>]*>(.*?)</div>'
            snippet_pattern = r'<div[^>]*class="gs_rs"[^>]*>(.*?)</div>'
            
            titles = re.findall(title_pattern, html, re.DOTALL)
            authors = re.findall(author_pattern, html, re.DOTALL)
            snippets = re.findall(snippet_pattern, html, re.DOTALL)
            
            for i in range(min(len(titles), max_results)):
                # Clean up HTML tags
                title = re.sub(r'<[^>]+>', '', titles[i]).strip()
                author_info = re.sub(r'<[^>]+>', '', authors[i]).strip() if i < len(authors) else ""
                snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ""
                
                # Extract year from author info
                year_match = re.search(r'\d{4}', author_info)
                year = year_match.group() if year_match else "Unknown"
                
                papers.append({
                    "title": title,
                    "authors": author_info.split('-')[0].strip() if '-' in author_info else author_info,
                    "year": year,
                    "abstract": snippet,
                    "source": "google_scholar",
                    "url": f"https://scholar.google.com/scholar?q={title.replace(' ', '+')}"
                })
                
        except Exception as e:
            print(f"Error parsing Google Scholar results: {e}")
        
        return papers
    
    def get_citations(self, paper_title: str) -> List[Dict]:
        """Get papers that cite a given paper"""
        try:
            query = f"cite:{paper_title}"
            return self.search_papers(query, max_results=10)
        except Exception as e:
            print(f"Error getting citations: {e}")
            return []


class PubMedAPI:
    """PubMed API integration for biomedical literature"""
    
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.tool = "research_assistant"
        self.email = "research@example.com"  # Should be configured
    
    def search_papers(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search for papers in PubMed"""
        try:
            # Step 1: Search for paper IDs
            search_url = f"{self.base_url}/esearch.fcgi"
            search_params = {
                'db': 'pubmed',
                'term': query,
                'retmax': max_results,
                'tool': self.tool,
                'email': self.email
            }
            
            search_response = requests.get(search_url, params=search_params, timeout=10)
            
            if search_response.status_code != 200:
                return []
            
            # Parse search results to get PMIDs
            root = ET.fromstring(search_response.text)
            id_list = root.find('.//IdList')
            
            if id_list is None:
                return []
            
            pmids = [id_elem.text for id_elem in id_list.findall('Id')]
            
            if not pmids:
                return []
            
            # Step 2: Fetch detailed information for each paper
            papers = self._fetch_paper_details(pmids)
            return papers
            
        except Exception as e:
            print(f"PubMed search error: {e}")
            return []
    
    def _fetch_paper_details(self, pmids: List[str]) -> List[Dict]:
        """Fetch detailed information for papers given their PMIDs"""
        try:
            fetch_url = f"{self.base_url}/efetch.fcgi"
            fetch_params = {
                'db': 'pubmed',
                'id': ','.join(pmids),
                'retmode': 'xml',
                'tool': self.tool,
                'email': self.email
            }
            
            fetch_response = requests.get(fetch_url, params=fetch_params, timeout=15)
            
            if fetch_response.status_code != 200:
                return []
            
            return self._parse_pubmed_xml(fetch_response.text)
            
        except Exception as e:
            print(f"Error fetching paper details: {e}")
            return []
    
    def _parse_pubmed_xml(self, xml_text: str) -> List[Dict]:
        """Parse PubMed XML response"""
        papers = []
        
        try:
            root = ET.fromstring(xml_text)
            articles = root.findall('.//PubmedArticle')
            
            for article in articles:
                try:
                    # Extract basic information
                    pmid_elem = article.find('.//PMID')
                    pmid = pmid_elem.text if pmid_elem is not None else ""
                    
                    title_elem = article.find('.//ArticleTitle')
                    title = title_elem.text if title_elem is not None else "Unknown"
                    
                    # Extract abstract
                    abstract_elem = article.find('.//AbstractText')
                    abstract = abstract_elem.text if abstract_elem is not None else ""
                    if not abstract:
                        # Try to get abstract from AbstractText with Label
                        abstract_texts = article.findall('.//AbstractText')
                        abstract = ' '.join([at.text for at in abstract_texts if at.text])
                    
                    # Extract authors
                    authors = []
                    author_list = article.find('.//AuthorList')
                    if author_list is not None:
                        for author in author_list.findall('Author'):
                            last_name = author.find('LastName')
                            first_name = author.find('ForeName')
                            if last_name is not None and first_name is not None:
                                authors.append(f"{first_name.text} {last_name.text}")
                            elif last_name is not None:
                                authors.append(last_name.text)
                    
                    # Extract publication date
                    pub_date_elem = article.find('.//PubDate')
                    year = "Unknown"
                    if pub_date_elem is not None:
                        year_elem = pub_date_elem.find('Year')
                        if year_elem is not None:
                            year = year_elem.text
                        else:
                            # Try MedlineDate
                            medline_date = pub_date_elem.find('MedlineDate')
                            if medline_date is not None:
                                year_match = re.search(r'\d{4}', medline_date.text)
                                year = year_match.group() if year_match else "Unknown"
                    
                    # Extract journal
                    journal_elem = article.find('.//Journal/Title')
                    journal = journal_elem.text if journal_elem is not None else ""
                    
                    papers.append({
                        "title": title,
                        "authors": ', '.join(authors) if authors else "Unknown",
                        "year": year,
                        "abstract": abstract,
                        "journal": journal,
                        "pmid": pmid,
                        "citationCount": 0,  # PubMed doesn't provide citation count directly
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        "source": "pubmed"
                    })
                    
                except Exception as e:
                    print(f"Error parsing individual article: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error parsing PubMed XML: {e}")
        
        return papers
    
    def get_similar_papers(self, pmid: str, max_results: int = 10) -> List[Dict]:
        """Get papers similar to a given paper (using Related Articles)"""
        try:
            similar_url = f"{self.base_url}/elink.fcgi"
            similar_params = {
                'dbfrom': 'pubmed',
                'id': pmid,
                'cmd': 'neighbor_score',
                'retmode': 'xml'
            }
            
            response = requests.get(similar_url, params=similar_params, timeout=10)
            
            if response.status_code != 200:
                return []
            
            root = ET.fromstring(response.text)
            id_list = root.find('.//IdList')
            
            if id_list is None:
                return []
            
            similar_pmids = [id_elem.text for id_elem in id_list.findall('Id')][:max_results]
            
            if not similar_pmids:
                return []
            
            return self._fetch_paper_details(similar_pmids)
            
        except Exception as e:
            print(f"Error getting similar papers: {e}")
            return []


class DataSourceManager:
    """Manages multiple data sources for paper discovery"""
    
    def __init__(self):
        self.google_scholar = GoogleScholarAPI()
        self.pubmed = PubMedAPI()
    
    def search_all_sources(self, query: str, sources: List[str] = None, max_results: int = 10) -> Dict[str, List[Dict]]:
        """Search across multiple data sources"""
        if sources is None:
            sources = ["google_scholar", "pubmed"]
        
        results = {}
        
        if "google_scholar" in sources:
            try:
                results["google_scholar"] = self.google_scholar.search_papers(query, max_results)
            except Exception as e:
                print(f"Google Scholar search failed: {e}")
                results["google_scholar"] = []
        
        if "pubmed" in sources:
            try:
                results["pubmed"] = self.pubmed.search_papers(query, max_results)
            except Exception as e:
                print(f"PubMed search failed: {e}")
                results["pubmed"] = []
        
        return results
    
    def get_paper_by_pmid(self, pmid: str) -> Optional[Dict]:
        """Get paper details by PubMed ID"""
        try:
            papers = self.pubmed._fetch_paper_details([pmid])
            return papers[0] if papers else None
        except Exception as e:
            print(f"Error getting paper by PMID: {e}")
            return None
    
    def format_for_app(self, papers: List[Dict], source: str) -> List[Dict]:
        """Format papers from external sources for app consumption"""
        formatted = []
        
        for paper in papers:
            formatted_paper = {
                "title": paper.get("title", "Unknown"),
                "year": paper.get("year", "Unknown"),
                "abstract": paper.get("abstract", "No abstract available"),
                "citationCount": paper.get("citationCount", 0),
                "url": paper.get("url", ""),
                "source": source,
                "externalIds": {}
            }
            
            # Add source-specific identifiers
            if source == "pubmed" and paper.get("pmid"):
                formatted_paper["externalIds"]["PubMed"] = paper["pmid"]
            
            formatted.append(formatted_paper)
        
        return formatted


# Global data source manager instance
data_source_manager = DataSourceManager()