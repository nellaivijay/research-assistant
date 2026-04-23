"""
Database Module - SQLite implementation for better data management
"""
import sqlite3
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager


class DatabaseManager:
    """Manages SQLite database operations for the research assistant"""
    
    def __init__(self, db_path: str = "research_assistant.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database with required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Reading lists table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reading_lists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    paper_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    year TEXT,
                    abstract TEXT,
                    url TEXT,
                    citation_count INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'to-read',
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    paper_data TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    UNIQUE(user_id, paper_id)
                )
            """)
            
            # Notes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    paper_id TEXT NOT NULL,
                    notes TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    UNIQUE(user_id, paper_id)
                )
            """)
            
            # Custom prompts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS custom_prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    prompt_name TEXT NOT NULL,
                    prompt_content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    UNIQUE(user_id, prompt_name)
                )
            """)
            
            # A/B test results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ab_test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    test_id TEXT NOT NULL,
                    paper_title TEXT,
                    model_a TEXT,
                    model_b TEXT,
                    analysis_type TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_preference TEXT,
                    preference_reason TEXT,
                    winner TEXT,
                    test_data TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            # Search history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    search_query TEXT NOT NULL,
                    source TEXT,
                    results_count INTEGER DEFAULT 0,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_reading_lists_user ON reading_lists(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_reading_lists_status ON reading_lists(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_notes_user ON notes(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_notes_paper ON notes(paper_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_ab_tests_user ON ab_test_results(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_history_user ON search_history(user_id)")
            
            conn.commit()
    
    def get_or_create_user(self, user_id: str) -> int:
        """Get existing user or create new one"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Try to get existing user
            cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            
            if result:
                # Update last active
                cursor.execute(
                    "UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE user_id = ?",
                    (user_id,)
                )
                return result['id']
            else:
                # Create new user
                cursor.execute(
                    "INSERT INTO users (user_id) VALUES (?)",
                    (user_id,)
                )
                return cursor.lastrowid
    
    # Reading List Operations
    def add_to_reading_list(self, user_id: str, paper: Dict) -> bool:
        """Add paper to user's reading list"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Ensure user exists
                self.get_or_create_user(user_id)
                
                # Insert paper
                cursor.execute("""
                    INSERT OR REPLACE INTO reading_lists 
                    (user_id, paper_id, title, year, abstract, url, citation_count, status, paper_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    paper.get('externalIds', {}).get('ArXiv') or paper.get('paperId') or paper.get('title'),
                    paper.get('title', ''),
                    paper.get('year', ''),
                    paper.get('abstract', ''),
                    paper.get('url', ''),
                    paper.get('citationCount', 0),
                    paper.get('status', 'to-read'),
                    json.dumps(paper)
                ))
                
                return True
        except Exception as e:
            print(f"Error adding to reading list: {e}")
            return False
    
    def get_reading_list(self, user_id: str) -> List[Dict]:
        """Get user's reading list"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM reading_lists 
                    WHERE user_id = ? 
                    ORDER BY added_date DESC
                """, (user_id,))
                
                papers = []
                for row in cursor.fetchall():
                    paper = dict(row)
                    # Parse JSON data
                    if paper['paper_data']:
                        try:
                            paper.update(json.loads(paper['paper_data']))
                        except:
                            pass
                    papers.append(paper)
                
                return papers
        except Exception as e:
            print(f"Error getting reading list: {e}")
            return []
    
    def update_reading_status(self, user_id: str, paper_id: str, status: str) -> bool:
        """Update status of paper in reading list"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE reading_lists 
                    SET status = ? 
                    WHERE user_id = ? AND paper_id = ?
                """, (status, user_id, paper_id))
                
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating reading status: {e}")
            return False
    
    def remove_from_reading_list(self, user_id: str, paper_id: str) -> bool:
        """Remove paper from reading list"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM reading_lists 
                    WHERE user_id = ? AND paper_id = ?
                """, (user_id, paper_id))
                
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error removing from reading list: {e}")
            return False
    
    # Notes Operations
    def save_note(self, user_id: str, paper_id: str, notes: str) -> bool:
        """Save notes for a paper"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Ensure user exists
                self.get_or_create_user(user_id)
                
                cursor.execute("""
                    INSERT OR REPLACE INTO notes (user_id, paper_id, notes, updated_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """, (user_id, paper_id, notes))
                
                return True
        except Exception as e:
            print(f"Error saving note: {e}")
            return False
    
    def get_note(self, user_id: str, paper_id: str) -> Optional[str]:
        """Get notes for a paper"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT notes FROM notes 
                    WHERE user_id = ? AND paper_id = ?
                """, (user_id, paper_id))
                
                result = cursor.fetchone()
                return result['notes'] if result else None
        except Exception as e:
            print(f"Error getting note: {e}")
            return None
    
    def get_all_notes(self, user_id: str) -> List[Dict]:
        """Get all notes for a user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM notes 
                    WHERE user_id = ? 
                    ORDER BY updated_at DESC
                """, (user_id,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting all notes: {e}")
            return []
    
    # Custom Prompts Operations
    def save_custom_prompt(self, user_id: str, name: str, content: str) -> bool:
        """Save custom prompt"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO custom_prompts (user_id, prompt_name, prompt_content)
                    VALUES (?, ?, ?)
                """, (user_id, name, content))
                
                return True
        except Exception as e:
            print(f"Error saving custom prompt: {e}")
            return False
    
    def get_custom_prompts(self, user_id: str = None) -> List[Dict]:
        """Get custom prompts"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if user_id:
                    cursor.execute("""
                        SELECT * FROM custom_prompts 
                        WHERE user_id = ? OR user_id IS NULL
                    """, (user_id,))
                else:
                    cursor.execute("SELECT * FROM custom_prompts WHERE user_id IS NULL")
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting custom prompts: {e}")
            return []
    
    # A/B Test Operations
    def save_ab_test_result(self, user_id: str, test_data: Dict) -> bool:
        """Save A/B test result"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO ab_test_results 
                    (user_id, test_id, paper_title, model_a, model_b, analysis_type, test_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    test_data.get('test_id'),
                    test_data.get('paper_title'),
                    test_data.get('model_a'),
                    test_data.get('model_b'),
                    test_data.get('analysis_type'),
                    json.dumps(test_data)
                ))
                
                return True
        except Exception as e:
            print(f"Error saving A/B test result: {e}")
            return False
    
    def update_ab_test_preference(self, test_id: str, preference: str, reason: str = "") -> bool:
        """Update A/B test preference"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE ab_test_results 
                    SET user_preference = ?, preference_reason = ?, winner = ?
                    WHERE test_id = ?
                """, (preference, reason, preference, test_id))
                
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating A/B test preference: {e}")
            return False
    
    def get_ab_test_statistics(self, user_id: str = None) -> Dict:
        """Get A/B test statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if user_id:
                    cursor.execute("""
                        SELECT model_a, model_b, winner 
                        FROM ab_test_results 
                        WHERE user_id = ? AND winner IS NOT NULL
                    """, (user_id,))
                else:
                    cursor.execute("""
                        SELECT model_a, model_b, winner 
                        FROM ab_test_results 
                        WHERE winner IS NOT NULL
                    """)
                
                results = cursor.fetchall()
                
                model_wins = {}
                total_tests = len(results)
                
                for row in results:
                    winner = row['winner']
                    if winner:
                        model_wins[winner] = model_wins.get(winner, 0) + 1
                
                return {
                    'total_tests': total_tests,
                    'model_wins': model_wins,
                    'win_rates': {
                        model: (wins / total_tests * 100) if total_tests > 0 else 0
                        for model, wins in model_wins.items()
                    }
                }
        except Exception as e:
            print(f"Error getting A/B test statistics: {e}")
            return {'total_tests': 0, 'model_wins': {}, 'win_rates': {}}
    
    # Search History Operations
    def save_search(self, user_id: str, query: str, source: str, results_count: int) -> bool:
        """Save search to history"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO search_history (user_id, search_query, source, results_count)
                    VALUES (?, ?, ?, ?)
                """, (user_id, query, source, results_count))
                
                return True
        except Exception as e:
            print(f"Error saving search: {e}")
            return False
    
    def get_search_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get recent search history"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM search_history 
                    WHERE user_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (user_id, limit))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting search history: {e}")
            return []
    
    # Utility Operations
    def get_user_statistics(self, user_id: str) -> Dict:
        """Get comprehensive user statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Reading list count
                cursor.execute("SELECT COUNT(*) as count FROM reading_lists WHERE user_id = ?", (user_id,))
                stats['reading_list_count'] = cursor.fetchone()['count']
                
                # Notes count
                cursor.execute("SELECT COUNT(*) as count FROM notes WHERE user_id = ?", (user_id,))
                stats['notes_count'] = cursor.fetchone()['count']
                
                # A/B tests count
                cursor.execute("SELECT COUNT(*) as count FROM ab_test_results WHERE user_id = ?", (user_id,))
                stats['ab_tests_count'] = cursor.fetchone()['count']
                
                # Search count
                cursor.execute("SELECT COUNT(*) as count FROM search_history WHERE user_id = ?", (user_id,))
                stats['search_count'] = cursor.fetchone()['count']
                
                # Reading list by status
                cursor.execute("""
                    SELECT status, COUNT(*) as count 
                    FROM reading_lists 
                    WHERE user_id = ? 
                    GROUP BY status
                """, (user_id,))
                stats['reading_list_by_status'] = {row['status']: row['count'] for row in cursor.fetchall()}
                
                return stats
        except Exception as e:
            print(f"Error getting user statistics: {e}")
            return {}
    
    def export_user_data(self, user_id: str) -> Dict:
        """Export all user data"""
        try:
            return {
                'reading_list': self.get_reading_list(user_id),
                'notes': self.get_all_notes(user_id),
                'custom_prompts': self.get_custom_prompts(user_id),
                'search_history': self.get_search_history(user_id, limit=100),
                'statistics': self.get_user_statistics(user_id),
                'export_date': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error exporting user data: {e}")
            return {}


# Global database manager instance
db_manager = DatabaseManager()