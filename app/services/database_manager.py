import sqlite3
import numpy as np

from models.face import Face
from models.camera import Camera
from models.log import Log

from config import DATABASE_PATH

class DatabaseManager:
  _instance = None
  
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(DatabaseManager, cls).__new__(cls)
      cls._instance._connect()
      cls._instance._create_table()
    return cls._instance
  
  def _connect(self):
    if not hasattr(self, 'conn'):
      self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
      self.cursor = self.conn.cursor()
    
  def _create_table(self):
    # Create table Face
    self.cursor.execute(
      """
      CREATE TABLE IF NOT EXISTS faces(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        embedding BLOB NOT NULL
      )
      """
    )
    
    # Create table Camera
    self.cursor.execute(
      """
      CREATE TABLE IF NOT EXISTS cameras(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rtsp_url TEXT NOT NULL
      )
      """
    )
    
    # Create table logs
    self.cursor.execute(
      """
      CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        camera_id INTEGER NOT NULL,
        detected_face_id INTEGER NOT NULL,
        FOREIGN KEY (camera_id) REFERENCES cameras(id)
        FOREIGN KEY (detected_face_id) REFERENCES faces(id)
      )
      """
    )
    
    self.conn.commit()
    
  def get_connection(self):
    if not hasattr(self, 'conn'):
      self._connect()
    return self.conn
  
  # Face CRUD operations
  def store_embedding(self, face: Face):
    try: 
      name = face.name
      embedding = face.embedding
      self.cursor.execute("INSERT INTO faces (name, embedding) VALUES (?, ?)", (name, embedding.tobytes())) # Convert np array to byte
      self.conn.commit()
    except Exception as e:
      self.conn.rollback()
      raise e
  
  def store_embedding(self, name: str, embedding: np.ndarray):
    try: 
      self.cursor.execute("INSERT INTO faces (name, embedding) VALUES (?, ?)", (name, embedding.tobytes())) # Convert np array to byte
      self.conn.commit()
    except Exception as e:
      self.conn.rollback()
      raise e
  
  # This function should be only used for computing, not for result publishing
  def get_all_embeddings(self) -> list[Face]:
    self.cursor.execute("SELECT id, name, embedding FROM faces")
    rows = self.cursor.fetchall()
    return [Face(id=row[0], name=row[1], embedding=np.frombuffer(row[2], dtype=np.float32)) for row in rows]
  
  def get_all_faces(self) -> list[Face]:
    self.cursor.execute("SELECT id, name FROM faces")
    rows = self.cursor.fetchall()
    return [Face(id=row[0], name=row[1], embedding=None) for row in rows]
    
  def delete_face(self, face: Face):
    try: 
      self.cursor.execute("DELETE FROM faces WHERE id=?", (face.id,))
      self.conn.commit()
    except Exception as e:
      self.conn.rollback()
      raise e
    
  def delete_face(self, id: int):
    try: 
      self.cursor.execute("DELETE FROM faces WHERE id=?", (id,))
      self.conn.commit()
    except Exception as e:
      self.conn.rollback()
      raise e
    
  # Camera CRUD operations
  def store_camera(self, name: str, rtsp_url: str):
    try: 
      self.cursor.execute("INSERT INTO cameras (name, rtsp_url) VALUES (?, ?)", (name, rtsp_url))
      self.conn.commit()
    except Exception as e:
      self.conn.rollback()
      raise e
  
  def delete_camera(self, id: str):
    try: 
      self.cursor.execute("DELETE FROM cameras WHERE id=?", (id,))
      self.conn.commit()
    except Exception as e:
      self.conn.rollback()
      raise e
    
  def store_camera(self, camera: Camera):
    try:
      self.cursor.execute("INSERT INTO cameras (name, rtsp_url) VALUES (?, ?)", (camera.name, camera.rtsp_url))
      self.conn.commit()
    except Exception as e:
      self.conn.rollback()
      raise e
    
  def get_camera(self, id: int) -> Camera:
    self.cursor.execute("SELECT id, name, rtsp_url FROM cameras WHERE id=?", (id,))
    row = self.cursor.fetchone()
    return Camera(id=row[0], name=row[1], rtsp_url=row[2])
  
  def get_all_cameras(self) -> list[Camera]:
    self.cursor.execute("SELECT id, name, rtsp_url FROM cameras")
    rows = self.cursor.fetchall()
    return [Camera(id=row[0], name=row[1], rtsp_url=row[2]) for row in rows]
  
  # Log operations
  def store_log(self, camera_id: int, detected_face_id: int):
    try:
      self.cursor.execute("INSERT INTO logs (camera_id, detected_face_id) VALUES (?, ?)", (camera_id, detected_face_id))
      self.conn.commit()
    except Exception as e:
      self.conn.rollback()
      raise e
  
  def store_log(self, log: Log):
    try:
      self.cursor.execute("INSERT INTO logs (camera_id, detected_face_id) VALUES (?, ?)", (log.camera_id, log.detected_face_id))
      self.conn.commit()
    except Exception as e:
      self.conn.rollback()
      raise e    
  
  def get_all_logs(self) -> list[Log]:
    self.cursor.execute("SELECT id, timestamp, camera_id, detected_face_id FROM logs")
    rows = self.cursor.fetchall()
    return [Log(id=row[0], timestamp=row[1], camera_id=row[2], detected_face_id=row[3]) for row in rows]
  
  def clear_logs(self):
    try: 
      self.cursor.execute("DELETE FROM logs")
      self.conn.commit()
    except Exception as e:
      self.conn.rollback()
      raise e