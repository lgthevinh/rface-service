from typing import List, Dict, Any # Low level dependencies

from deepface import DeepFace
from services.database_manager import DatabaseManager
import numpy as np

from models.face import Face

class FaceRecognition:
  """
  Singleton class for face recognition, using DeepFace framework.\n
  
  The model using is set to Dlib as default, and threshold is set to 0.6.
  """
  _instance = None
  
  def __new__(cls):    
    if cls._instance is None:
      cls._instance = super(FaceRecognition, cls).__new__(cls)
      cls._instance.model = "Dlib"
      cls._instance.threshold = 0.06
    return cls._instance
  
  def set_model(self, model: str):
    self.model = model
    
  def set_threshold(self, threshold: float):
    self.threshold = threshold
  
  def _extract_embedding(self, img: np.ndarray | str) -> List[Dict[str, Any]]:
    return DeepFace.represent(img, model_name=self.model, enforce_detection=False, max_faces=1)
  
  def _compare_embedding(self, db_embedding, target_embedding) -> Dict[str, Any]:
    # Compare embeddings using cosine similarity
    # If similarity is above a certain threshold, return True
    # Otherwise, return False
    
    return DeepFace.verify(db_embedding, target_embedding, model_name=self.model, distance_metric='cosine', threshold=self.threshold)
  
  def detect_face(self, img: np.ndarray):
    """
    Detect face in the image array.\n
    Return the image array with the face detected.
    """
    result = DeepFace.extract_faces(img, enforce_detection=False)
    return result
  
  def register(self, name : str, img : np.ndarray):
    db_manager = DatabaseManager()
    
    data = self._extract_embedding(img)
    
    # If no face is detected or embedding is empty, don't store it in the database
    if not data[0]["embedding"]:
      return {"message": "No face detected"}
    
    # Store embedding in database and return it
    embedding = np.array(data[0]["embedding"], dtype=np.float32) 
    db_manager.store_embedding(name, embedding)

  def recognize(self, img_array: np.ndarray) -> tuple[Face, float]:
    """Recognize the face in the image array"""
    db_manager = DatabaseManager()
    db_faces = db_manager.get_all_embeddings()
    
    if not db_faces:
      return None, None
    
    target_embedding = self._extract_embedding(img_array)
    
    if target_embedding[0]["face_confidence"] == 0:
      return None, None
    
    for db_face in db_faces: 
      result = self._compare_embedding(db_face.embedding.tolist(), target_embedding[0]["embedding"])
      if result['verified']:
        return Face(db_face.id, db_face.name, None), result['distance']
      
    return None, 0