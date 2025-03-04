from typing import List, Dict, Any # Low level dependencies

from deepface import DeepFace
import numpy as np

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
  
  def extract_embeddings(self, img: np.ndarray | str) -> List[Dict[str, Any]]:
    return DeepFace.represent(img, model_name=self.model, enforce_detection=False)
  
  def compare_embeddings(self, db_embedding, target_embedding) -> Dict[str, Any]:
    # Compare embeddings using cosine similarity
    # If similarity is above a certain threshold, return True
    # Otherwise, return False
    
    # 1st approach: Fetch all embeddings from the database and compare them one by one (using DeepFace.verify)
    # 2nd approach: Use a more efficient method to compare embeddings (e.g., KNN, ANN) (tech debt)
    
    return DeepFace.verify(db_embedding, target_embedding, model_name=self.model, distance_metric='cosine', threshold=self.threshold)
    