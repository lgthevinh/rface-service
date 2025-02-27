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
    # Extract embedding from image/frame
    data = self.face_reg.extract_embeddings(img_array)
    
    # If no face is detected or embedding is empty, don't store it in the database
    if not data[0]["embedding"]:
      return None
    
    # Store embedding in database and return it
    embedding = np.array(data[0]["embedding"], dtype=np.float32) 
    self.db.store_embedding(name, embedding)
    return embedding
  
  def recognize_face(self, img_array: np.ndarray):
    """
    Recognize a face by comparing its embedding with the embeddings in the database.
    Parameters:
      img_array: np.ndarray - Image array of the face to be recognized.
    Returns:
      str: Name of the recognized person.
    """
    # Extract embedding from image/frame
    # Get all embeddings from database
    # Compare embeddings
    # Return result (publish to API)
    pass
  
  def __str__(self):
    return "RFace instance"