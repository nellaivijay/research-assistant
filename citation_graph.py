"""
Citation Graph Visualization Module
Creates interactive citation network visualizations
"""
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Optional, Tuple
import json
from datetime import datetime
import random


class CitationGraphBuilder:
    """Builds citation graphs from paper data"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def add_paper(self, paper: Dict, citations: List[Dict] = None):
        """Add a paper and its citations to the graph"""
        paper_id = paper.get('externalIds', {}).get('ArXiv') or paper.get('paperId') or paper.get('title')
        
        # Add the paper node
        self.graph.add_node(paper_id, **{
            'title': paper.get('title', 'Unknown'),
            'year': paper.get('year', 'Unknown'),
            'citationCount': paper.get('citationCount', 0),
            'url': paper.get('url', ''),
            'abstract': paper.get('abstract', '')[:200],
            'node_type': 'main'
        })
        
        # Add citation edges
        if citations:
            for citation in citations:
                cite_id = citation.get('externalIds', {}).get('ArXiv') or citation.get('paperId') or citation.get('title')
                
                # Add citation node
                self.graph.add_node(cite_id, **{
                    'title': citation.get('title', 'Unknown'),
                    'year': citation.get('year', 'Unknown'),
                    'citationCount': citation.get('citationCount', 0),
                    'url': citation.get('url', ''),
                    'abstract': citation.get('abstract', '')[:200],
                    'node_type': 'citation'
                })
                
                # Add edge from paper to citation
                self.graph.add_edge(paper_id, cite_id)
    
    def add_related_papers(self, base_paper: Dict, related_papers: List[Dict], relationship_type: str = 'related'):
        """Add related papers with different relationship types"""
        base_id = base_paper.get('externalIds', {}).get('ArXiv') or base_paper.get('paperId') or base_paper.get('title')
        
        for related in related_papers:
            related_id = related.get('externalIds', {}).get('ArXiv') or related.get('paperId') or related.get('title')
            
            # Add related paper node
            self.graph.add_node(related_id, **{
                'title': related.get('title', 'Unknown'),
                'year': related.get('year', 'Unknown'),
                'citationCount': related.get('citationCount', 0),
                'url': related.get('url', ''),
                'abstract': related.get('abstract', '')[:200],
                'node_type': relationship_type
            })
            
            # Add relationship edge
            self.graph.add_edge(base_id, related_id, relationship=relationship_type)
    
    def build_from_recommendations(self, base_paper: Dict, recommendations: Dict):
        """Build graph from recommendation results"""
        # Add base paper
        self.add_paper(base_paper)
        
        # Add papers from different sources
        for source, papers in recommendations.items():
            if papers:
                for paper in papers:
                    self.add_related_papers(base_paper, [paper], f'recommended_{source}')
    
    def get_graph_statistics(self) -> Dict:
        """Get statistics about the citation graph"""
        return {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'is_connected': nx.is_weakly_connected(self.graph),
            'average_clustering': nx.average_clustering(self.graph.to_undirected()),
            'node_types': self._get_node_type_counts()
        }
    
    def _get_node_type_counts(self) -> Dict[str, int]:
        """Count nodes by type"""
        type_counts = {}
        for node, data in self.graph.nodes(data=True):
            node_type = data.get('node_type', 'unknown')
            type_counts[node_type] = type_counts.get(node_type, 0) + 1
        return type_counts


class CitationGraphVisualizer:
    """Creates interactive visualizations of citation graphs"""
    
    def __init__(self, graph_builder: CitationGraphBuilder):
        self.graph_builder = graph_builder
        self.graph = graph_builder.graph
    
    def create_interactive_plot(self, layout: str = 'spring', max_nodes: int = 50) -> go.Figure:
        """Create an interactive Plotly visualization"""
        
        # Limit nodes for performance
        if self.graph.number_of_nodes() > max_nodes:
            # Get most important nodes by citation count
            nodes_by_importance = sorted(
                self.graph.nodes(data=True),
                key=lambda x: x[1].get('citationCount', 0),
                reverse=True
            )[:max_nodes]
            
            subgraph = self.graph.subgraph([node[0] for node in nodes_by_importance])
        else:
            subgraph = self.graph
        
        # Calculate layout
        if layout == 'spring':
            pos = nx.spring_layout(subgraph, k=1, iterations=50)
        elif layout == 'circular':
            pos = nx.circular_layout(subgraph)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(subgraph)
        else:
            pos = nx.spring_layout(subgraph)
        
        # Extract node and edge information
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        node_sizes = []
        
        color_map = {
            'main': '#FF6B6B',      # Red for main paper
            'citation': '#4ECDC4',   # Teal for citations
            'related': '#45B7D1',    # Blue for related
            'recommended_semantic_scholar': '#96CEB4',  # Green
            'recommended_arxiv': '#FFEAA7',              # Yellow
            'unknown': '#95A5A6'     # Gray for unknown
        }
        
        for node, data in subgraph.nodes(data=True):
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            # Node text (title + year)
            title = data.get('title', 'Unknown')
            year = data.get('year', 'Unknown')
            citations = data.get('citationCount', 0)
            node_text.append(f"{title}<br>Year: {year}<br>Citations: {citations}")
            
            # Node color based on type
            node_type = data.get('node_type', 'unknown')
            node_colors.append(color_map.get(node_type, color_map['unknown']))
            
            # Node size based on citation count
            citation_count = data.get('citationCount', 0)
            node_sizes.append(10 + min(citation_count / 5, 30))  # Scale size
        
        # Extract edge information
        edge_x = []
        edge_y = []
        
        for edge in subgraph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        # Create edge trace
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create node trace
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=2, color='white')
            )
        )
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title='Citation Network Visualization',
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20, l=5, r=5, t=40),
                           annotations=[
                               dict(
                                   text="",
                                   showarrow=False,
                                   xref="paper", yref="paper",
                                   x=0.005, y=-0.002,
                                   xanchor='left', yanchor='bottom',
                                   font=dict(color='#888', size=12)
                               )
                           ],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                       ))
        
        return fig
    
    def create_statistics_plot(self) -> go.Figure:
        """Create a statistics visualization of the graph"""
        stats = self.graph_builder.get_graph_statistics()
        
        # Create subplots
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Node Types', 'Graph Statistics', 'Citation Distribution', 'Network Properties'),
            specs=[[{'type': 'bar'}, {'type': 'indicator'}],
                   [{'type': 'histogram'}, {'type': 'table'}]]
        )
        
        # Node types bar chart
        node_types = stats['node_types']
        fig.add_trace(
            go.Bar(x=list(node_types.keys()), y=list(node_types.values()),
                   marker_color='lightblue'),
            row=1, col=1
        )
        
        # Graph statistics indicator
        fig.add_trace(
            go.Indicator(
                mode="number+gauge",
                value=stats['total_nodes'],
                title={'text': "Total Nodes"},
                gauge={'axis': {'range': [None, stats['total_nodes']]}
                      }
            ),
            row=1, col=2
        )
        
        # Citation distribution histogram
        citation_counts = [data.get('citationCount', 0) for node, data in self.graph.nodes(data=True)]
        fig.add_trace(
            go.Histogram(x=citation_counts, nbinsx=20, marker_color='lightgreen'),
            row=2, col=1
        )
        
        # Network properties table
        fig.add_trace(
            go.Table(
                header=dict(values=['Metric', 'Value']),
                cells=dict(values=[
                    ['Total Nodes', 'Total Edges', 'Connected', 'Avg Clustering'],
                    [stats['total_nodes'], stats['total_edges'], 
                     str(stats['is_connected']), f"{stats['average_clustering']:.3f}"]
                ])
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False, title_text="Citation Graph Statistics")
        
        return fig
    
    def export_graph_json(self) -> str:
        """Export graph as JSON for external visualization"""
        from networkx.readwrite import json_graph
        
        graph_data = json_graph.node_link_data(self.graph)
        return json.dumps(graph_data, indent=2)


class CitationAnalysisEngine:
    """Main engine for citation analysis and visualization"""
    
    def __init__(self):
        self.graph_builder = CitationGraphBuilder()
        self.visualizer = CitationGraphVisualizer(self.graph_builder)
    
    def analyze_paper_citations(self, paper: Dict, recommendations: Dict = None) -> Dict:
        """Analyze citations for a paper and create visualization"""
        # Build graph
        if recommendations:
            self.graph_builder.build_from_recommendations(paper, recommendations)
        else:
            self.graph_builder.add_paper(paper)
        
        # Get statistics
        stats = self.graph_builder.get_graph_statistics()
        
        # Create visualizations
        network_plot = self.visualizer.create_interactive_plot()
        stats_plot = self.visualizer.create_statistics_plot()
        
        return {
            'statistics': stats,
            'network_plot': network_plot,
            'statistics_plot': stats_plot,
            'graph_json': self.visualizer.export_graph_json()
        }
    
    def create_comparison_graph(self, papers: List[Dict]) -> Dict:
        """Create a comparison graph showing relationships between multiple papers"""
        # Reset graph
        self.graph_builder = CitationGraphBuilder()
        self.visualizer = CitationGraphVisualizer(self.graph_builder)
        
        # Add all papers as nodes
        for i, paper in enumerate(papers):
            paper_id = f"paper_{i}"
            self.graph_builder.graph.add_node(paper_id, **{
                'title': paper.get('title', 'Unknown'),
                'year': paper.get('year', 'Unknown'),
                'citationCount': paper.get('citationCount', 0),
                'url': paper.get('url', ''),
                'node_type': 'comparison'
            })
        
        # Create edges between papers based on topic similarity (simplified)
        for i in range(len(papers)):
            for j in range(i+1, len(papers)):
                # Simple similarity based on shared topics
                topics_i = set(papers[i].get('topics', []))
                topics_j = set(papers[j].get('topics', []))
                similarity = len(topics_i & topics_j)
                
                if similarity > 0:
                    self.graph_builder.graph.add_edge(
                        f"paper_{i}", f"paper_{j}",
                        weight=similarity,
                        relationship='topic_similarity'
                    )
        
        # Create visualization
        network_plot = self.visualizer.create_interactive_plot(layout='circular')
        stats = self.graph_builder.get_graph_statistics()
        
        return {
            'network_plot': network_plot,
            'statistics': stats
        }


# Global citation analysis engine
citation_engine = CitationAnalysisEngine()