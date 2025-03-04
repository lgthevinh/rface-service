import os

from rface.face_recognition.FaceRecognition import FaceRecognition
from rface.DatabaseManager import DatabaseManager
import numpy as np

class RFace:
  _instance = None
  data_path = None
  
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(RFace, cls).__new__(cls)

    return cls._instance
  
  def init(self):
    """
    Initialize RFace instance by creating the data path and connecting to the database.
    """
    # Initialize face recognition model
    print("RFace start initializing...")
    
    # Check if data path exists, if not, create it.
    if not os.path.exists(self.data_path):
      os.makedirs(self.data_path)
    
    # Check DEEPFACE_HOME environment variable
    if "DEEPFACE_HOME" not in os.environ:
      os.makedirs("./data/.deepface/weights", exist_ok=True)
      os.environ["DEEPFACE_HOME"] = self.data_path
      
    self.db = DatabaseManager()
    self.db._connect(os.path.join(self.data_path, "rface.db"))
    
    self.face_reg = FaceRecognition()
  
  def register_face(self, img_array: np.ndarray, name: str):
    """
    Register a face in the database by storing its embedding.
    Parameters:
      img_array: np.ndarray - Image array of the face to be registered.
      name: str - Name of the person.
    Returns:
      np.ndarray: The embedding of the registered face.
    """
    try: 
      # Extract embedding from image/frame
      data = self.face_reg.extract_embeddings(img_array)
      
      # If no face is detected or embedding is empty, don't store it in the database
      if not data[0]["embedding"]:
        return None
      
      # Store embedding in database and return it
      embedding = np.array(data[0]["embedding"], dtype=np.float32) 
      self.db.store_embedding(name, embedding)
      return embedding
    
    except Exception as e:
      print(f"Error: {e}")
      return None
  
  def recognize_face(self, img_array: np.ndarray):
    """
    Recognize a face by comparing its embedding with the embeddings in the database.
    Parameters:
      img_array: np.ndarray - Image array of the face to be recognized.
    Returns:
      str: Name of the recognized person.
    """
    try: 
      # Extract embedding from image/frame
      data = self.face_reg.extract_embeddings(img_array)
      if not data[0]["embedding"]:
        return None

      # Get all embeddings from the database
      db_embeddings = self.db.get_all_embedding()
      
      # Compare the extracted embedding with the embeddings in the database
      for name, embedding in db_embeddings.items():
        result = self.face_reg.compare_embeddings(data[0]["embedding"], embedding.tolist())
        if result["verified"]:
          return {"name": name, "distance": round(result["distance"], 10), "verified": result["verified"]}
      return None
    
    except Exception as e:
      print(f"Error: {e}")
      return None
    
  def __str__(self):
    return "RFace instance"