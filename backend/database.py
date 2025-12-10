"""
Database module for AI Chat Application
Handles SQLite database operations for message persistence
"""

import sqlite3
from typing import List, Tuple
from pathlib import Path


class Database:
    """SQLite database manager for chat messages"""
    
    def __init__(self, db_path: str = "chat.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.connection = None
    
    def get_connection(self) -> sqlite3.Connection:
        """Get or create database connection"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        return self.connection
    
    def create_tables(self):
        """
        Create messages table if it doesn't exist
        
        Schema:
        - message_id: Auto-incrementing primary key
        - role: 'user' or 'assistant'
        - content: Message text content
        - timestamp: ISO format timestamp
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        
        conn.commit()
        print("✅ Database tables created/verified")
    
    def add_message(self, role: str, content: str, timestamp: str) -> int:
        """
        Add a new message to the database
        
        Args:
            role: 'user' or 'assistant'
            content: Message text
            timestamp: ISO format timestamp
        
        Returns:
            message_id of inserted message
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO messages (role, content, timestamp) VALUES (?, ?, ?)",
            (role, content, timestamp)
        )
        
        conn.commit()
        return cursor.lastrowid
    
    def get_all_messages(self) -> List[Tuple[int, str, str, str]]:
        """
        Retrieve all messages in chronological order
        
        Returns:
            List of tuples: (message_id, role, content, timestamp)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT message_id, role, content, timestamp FROM messages ORDER BY message_id ASC"
        )
        
        return cursor.fetchall()
    
    def get_recent_messages(self, limit: int = 50) -> List[Tuple[int, str, str, str]]:
        """
        Retrieve recent messages
        
        Args:
            limit: Maximum number of messages to retrieve
        
        Returns:
            List of tuples: (message_id, role, content, timestamp)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT message_id, role, content, timestamp FROM messages ORDER BY message_id DESC LIMIT ?",
            (limit,)
        )
        
        # Reverse to get chronological order
        return list(reversed(cursor.fetchall()))
    
    def clear_all_messages(self):
        """Delete all messages from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM messages")
        conn.commit()
        print("🗑️  All messages cleared from database")
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
