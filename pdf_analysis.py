"""
PDF Analysis Module
Handles PDF upload, text extraction, and analysis
"""
import PyPDF2
import pdfplumber
from typing import Dict, Optional, List
from pathlib import Path
import re
from datetime import datetime


class PDFAnalyzer:
    """Analyzes PDF documents for research papers"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text_from_pdf(self, pdf_path: str) -> Dict:
        """Extract text and metadata from PDF"""
        try:
            result = {
                'text': '',
                'metadata': {},
                'pages': 0,
                'success': False,
                'error': None
            }
            
            # Try pdfplumber first (better text extraction)
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    result['pages'] = len(pdf.pages)
                    text_parts = []
                    
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            text_parts.append(text)
                    
                    result['text'] = '\n'.join(text_parts)
                    result['metadata'] = pdf.metadata or {}
                    result['success'] = True
                    
            except Exception as e:
                # Fallback to PyPDF2
                try:
                    with open(pdf_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        result['pages'] = len(pdf_reader.pages)
                        text_parts = []
                        
                        for page in pdf_reader.pages:
                            text = page.extract_text()
                            if text:
                                text_parts.append(text)
                        
                        result['text'] = '\n'.join(text_parts)
                        result['metadata'] = pdf_reader.metadata or {}
                        result['success'] = True
                        
                except Exception as e2:
                    result['error'] = f"Both extraction methods failed: {str(e)}, {str(e2)}"
                    return result
            
            return result
            
        except Exception as e:
            return {
                'text': '',
                'metadata': {},
                'pages': 0,
                'success': False,
                'error': str(e)
            }
    
    def analyze_pdf_structure(self, pdf_path: str) -> Dict:
        """Analyze the structure of a PDF document"""
        try:
            extraction_result = self.extract_text_from_pdf(pdf_path)
            
            if not extraction_result['success']:
                return extraction_result
            
            text = extraction_result['text']
            
            analysis = {
                'title': self._extract_title(text),
                'authors': self._extract_authors(text),
                'abstract': self._extract_abstract(text),
                'sections': self._extract_sections(text),
                'references': self._extract_references(text),
                'word_count': len(text.split()),
                'char_count': len(text),
                'pages': extraction_result['pages'],
                'metadata': extraction_result['metadata']
            }
            
            return analysis
            
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }
    
    def _extract_title(self, text: str) -> str:
        """Extract title from PDF text"""
        lines = text.split('\n')
        
        # Title is usually the first substantial line
        for i, line in enumerate(lines[:10]):
            line = line.strip()
            if len(line) > 10 and len(line) < 200:  # Reasonable title length
                # Check if it looks like a title (no numbers at start, etc.)
                if not re.match(r'^\d+[\.\)]', line):
                    return line
        
        return "Unknown Title"
    
    def _extract_authors(self, text: str) -> List[str]:
        """Extract authors from PDF text"""
        authors = []
        lines = text.split('\n')
        
        # Look for author patterns (usually after title)
        for i, line in enumerate(lines[1:20]):  # Check first 20 lines after title
            line = line.strip()
            # Common author patterns
            if re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', line) and ',' in line:
                # Split by common separators
                potential_authors = re.split(r',|and|&', line)
                for author in potential_authors:
                    author = author.strip()
                    if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+', author):
                        authors.append(author)
                if authors:
                    break
        
        return authors if authors else ["Unknown Authors"]
    
    def _extract_abstract(self, text: str) -> str:
        """Extract abstract from PDF text"""
        # Look for abstract section
        abstract_match = re.search(
            r'(?:Abstract|ABSTRACT)\s*[:\-]?\s*(.*?)(?=\n\s*(?:Keywords|Introduction|1\.|I\.))',
            text,
            re.DOTALL | re.IGNORECASE
        )
        
        if abstract_match:
            abstract = abstract_match.group(1).strip()
            # Clean up the abstract
            abstract = re.sub(r'\s+', ' ', abstract)
            return abstract
        
        return "No abstract found"
    
    def _extract_sections(self, text: str) -> List[Dict]:
        """Extract main sections from PDF"""
        sections = []
        
        # Common section patterns
        section_patterns = [
            r'(Introduction|INTRODUCTION)\s*[:\-]?\s*(.*?)(?=\n\s*(?:\d+\.|[A-Z][A-Z]+))',
            r'(Related Work|RELATED WORK)\s*[:\-]?\s*(.*?)(?=\n\s*(?:\d+\.|[A-Z][A-Z]+))',
            r'(Methodology|METHODOLOGY)\s*[:\-]?\s*(.*?)(?=\n\s*(?:\d+\.|[A-Z][A-Z]+))',
            r'(Results|RESULTS)\s*[:\-]?\s*(.*?)(?=\n\s*(?:\d+\.|[A-Z][A-Z]+))',
            r'(Discussion|DISCUSSION)\s*[:\-]?\s*(.*?)(?=\n\s*(?:\d+\.|[A-Z][A-Z]+))',
            r'(Conclusion|CONCLUSION)\s*[:\-]?\s*(.*?)(?=\n\s*(?:\d+\.|[A-Z][A-Z]+))',
        ]
        
        for pattern in section_patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                sections.append({
                    'name': match.group(1),
                    'content': match.group(2).strip()[:500]  # First 500 chars
                })
        
        return sections
    
    def _extract_references(self, text: str) -> List[str]:
        """Extract references from PDF"""
        references = []
        
        # Look for references section
        ref_match = re.search(
            r'(?:References|REFERENCES|Bibliography|BIBLIOGRAPHY)\s*[:\-]?\s*(.*?)(?=\n\s*$)',
            text,
            re.DOTALL | re.IGNORECASE
        )
        
        if ref_match:
            ref_text = ref_match.group(1)
            # Split by common reference patterns
            ref_items = re.split(r'\n\s*\d+[\.\)]', ref_text)
            
            for ref in ref_items[:20]:  # Limit to first 20 references
                ref = ref.strip()
                if len(ref) > 20:  # Minimum length for a reference
                    references.append(ref)
        
        return references
    
    def convert_to_paper_dict(self, pdf_analysis: Dict, filename: str) -> Dict:
        """Convert PDF analysis to standard paper dictionary format"""
        return {
            'title': pdf_analysis.get('title', 'Unknown'),
            'authors': pdf_analysis.get('authors', ['Unknown']),
            'abstract': pdf_analysis.get('abstract', ''),
            'year': self._extract_year_from_metadata(pdf_analysis.get('metadata', {})),
            'citationCount': 0,  # PDF doesn't have citation count
            'url': filename,  # Use filename as URL for local files
            'source': 'pdf_upload',
            'externalIds': {},
            'sections': pdf_analysis.get('sections', []),
            'word_count': pdf_analysis.get('word_count', 0),
            'pages': pdf_analysis.get('pages', 0)
        }
    
    def _extract_year_from_metadata(self, metadata: Dict) -> str:
        """Extract year from PDF metadata"""
        # Check common metadata fields
        for field in ['/CreationDate', '/ModDate', '/Producer']:
            if field in metadata:
                date_str = metadata[field]
                # Try to extract year from date string
                year_match = re.search(r'(\d{4})', date_str)
                if year_match:
                    return year_match.group(1)
        
        return "Unknown"


class PDFAnalysisEngine:
    """Main engine for PDF analysis workflow"""
    
    def __init__(self):
        self.analyzer = PDFAnalyzer()
    
    def analyze_uploaded_pdf(self, pdf_file, filename: str) -> Dict:
        """Complete analysis workflow for uploaded PDF"""
        try:
            # Save uploaded file temporarily
            temp_path = f"/tmp/{filename}"
            with open(temp_path, 'wb') as f:
                f.write(pdf_file)
            
            # Analyze PDF structure
            structure_analysis = self.analyzer.analyze_pdf_structure(temp_path)
            
            if not structure_analysis.get('success'):
                return {
                    'success': False,
                    'error': structure_analysis.get('error', 'Analysis failed')
                }
            
            # Convert to standard format
            paper_dict = self.analyzer.convert_to_paper_dict(structure_analysis, filename)
            
            # Extract full text for AI analysis
            text_extraction = self.analyzer.extract_text_from_pdf(temp_path)
            
            # Clean up temporary file
            import os
            os.remove(temp_path)
            
            return {
                'success': True,
                'paper': paper_dict,
                'full_text': text_extraction.get('text', ''),
                'structure': structure_analysis,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_pdf_summary(self, pdf_analysis_result: Dict) -> str:
        """Generate a summary of PDF analysis results"""
        if not pdf_analysis_result.get('success'):
            return f"❌ PDF analysis failed: {pdf_analysis_result.get('error', 'Unknown error')}"
        
        paper = pdf_analysis_result.get('paper', {})
        structure = pdf_analysis_result.get('structure', {})
        
        summary = "## PDF Analysis Results\n\n"
        summary += f"**Title**: {paper.get('title', 'Unknown')}\n"
        summary += f"**Authors**: {', '.join(paper.get('authors', ['Unknown']))}\n"
        summary += f"**Year**: {paper.get('year', 'Unknown')}\n"
        summary += f"**Pages**: {paper.get('pages', 0)}\n"
        summary += f"**Word Count**: {paper.get('word_count', 0)}\n\n"
        
        summary += "### Abstract\n\n"
        abstract = paper.get('abstract', 'No abstract found')
        if abstract != 'No abstract found':
            summary += f"{abstract}\n\n"
        else:
            summary += "No abstract detected in the PDF.\n\n"
        
        summary += "### Document Structure\n\n"
        sections = structure.get('sections', [])
        if sections:
            for section in sections:
                summary += f"- **{section.get('name', 'Unknown')}**: {section.get('content', '')[:100]}...\n"
        else:
            summary += "No clear sections detected.\n"
        
        summary += f"\n### Text Statistics\n\n"
        summary += f"- **Total Words**: {paper.get('word_count', 0)}\n"
        summary += f"- **Total Characters**: {paper.get('char_count', 0)}\n"
        
        return summary
    
    def get_paper_json(self, pdf_analysis_result: Dict) -> str:
        """Get paper JSON from PDF analysis for use in other features"""
        if not pdf_analysis_result.get('success'):
            return json.dumps({'error': 'Analysis failed'})
        
        paper = pdf_analysis_result.get('paper', {})
        return json.dumps(paper, indent=2)


# Global PDF analysis engine
pdf_engine = PDFAnalysisEngine()