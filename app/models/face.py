from typing import Dict
import numpy as np

class Face:
  def __init__(self):
    self.id:int  = None
    self.name: str = None
    self.embedding: np.ndarray = None
    
  def __init__(self, id: int | None, name: str | None, embedding: np.ndarray | None):
    self.id = id
    self.name = name
    self.embedding = embedding
  
  def to_dict(self) -> Dict:
    if self.embedding is None:
      return {
        'id': self.id if self.id else None,
        'name': self.name
      }
    
    return {
      'id': self.id if self.id else None,
      'name': self.name,
      'embedding': self.embedding.tolist()
    }
  
  @staticmethod
  def from_dict(data: Dict):
    return Face(data['name'], np.array(data['embedding']))