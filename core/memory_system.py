import redis
import sqlite3
import pickle
import json
from datetime import datetime
from config.settings import REDIS_HOST, REDIS_PORT, REDIS_DB, DATABASE_PATH

class MemorySystem:
    def __init__(self):
        # Short-term memory (Redis)
        self.stm = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB
        )
        
        # Long-term memory (SQLite)
        self.init_ltm()
        
    def init_ltm(self):
        """Initialize long-term memory database"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Create memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                type TEXT,
                content TEXT,
                emotional_value REAL,
                importance_score REAL
            )
        ''')
        
        # Create associations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS associations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id INTEGER,
                associated_with INTEGER,
                strength REAL,
                FOREIGN KEY (memory_id) REFERENCES memories(id),
                FOREIGN KEY (associated_with) REFERENCES memories(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_short_term(self, key, value, ttl=3600):
        """Store information in short-term memory"""
        serialized = pickle.dumps(value)
        self.stm.set(key, serialized, ex=ttl)
    
    def recall_short_term(self, key):
        """Recall information from short-term memory"""
        value = self.stm.get(key)
        if value:
            return pickle.loads(value)
        return None
    
    def store_long_term(self, memory_type, content, emotional_value=0.0, importance=0.5):
        """Store information in long-term memory"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memories (timestamp, type, content, emotional_value, importance_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            memory_type,
            json.dumps(content),
            emotional_value,
            importance
        ))
        
        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return memory_id
    
    def create_association(self, memory_id1, memory_id2, strength=0.5):
        """Create association between two memories"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO associations (memory_id, associated_with, strength)
            VALUES (?, ?, ?)
        ''', (memory_id1, memory_id2, strength))
        
        conn.commit()
        conn.close()
    
    def recall_by_type(self, memory_type, limit=10):
        """Recall memories of specific type"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM memories 
            WHERE type = ?
            ORDER BY importance_score DESC
            LIMIT ?
        ''', (memory_type, limit))
        
        memories = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': m[0],
                'timestamp': m[1],
                'content': json.loads(m[3]),
                'emotional_value': m[4],
                'importance': m[5]
            }
            for m in memories
        ]
    
    def get_associated_memories(self, memory_id):
        """Get memories associated with given memory"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.*, a.strength
            FROM memories m
            JOIN associations a ON m.id = a.associated_with
            WHERE a.memory_id = ?
            ORDER BY a.strength DESC
        ''', (memory_id,))
        
        associated = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': m[0],
                'timestamp': m[1],
                'content': json.loads(m[3]),
                'emotional_value': m[4],
                'importance': m[5],
                'association_strength': m[6]
            }
            for m in associated
        ]
