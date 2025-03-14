import sqlite3
import numpy as np
from typing import Dict

class DatabaseManager:
  _instance = None
  
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(DatabaseManager, cls).__new__(cls)
    return cls._instance
  
  def _connect(self, db_path: str):
    self.conn = sqlite3.connect(db_path, check_same_thread=False)
    self.cursor = self.conn.cursor()
    self.cursor.execute(
      """
      CREATE TABLE IF NOT EXISTS faces(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        embedding BLOB NOT NULL
      )
      """
    )
    self.conn.commit()
  
  def store_embedding(self, name, embedding: np.ndarray):
    self.cursor.execute("INSERT INTO faces (name, embedding) VALUES (?, ?)", (name, embedding.tobytes())  ) # Convert np array to byte
    self.conn.commit()
  
  def get_all_embedding(self) -> Dict[str, np.ndarray]:
    self.cursor.execute("SELECT * FROM faces")
    rows = self.cursor.fetchall()
    return {row[1]: np.frombuffer(row[2], dtype=np.float32) for row in rows}
    
  def delete_embedding(self, name: str):
    self.cursor.execute("DELETE FROM faces WHERE name=?", (name,))
    self.conn.commit()