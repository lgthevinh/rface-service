class Log:
  def __init__(self, id: int, timestamp: str | None, camera_id: int, detected_face_id: int):
    self.id = id
    self.timestamp = timestamp
    self.camera_id = camera_id
    self.detected_face_id = detected_face_id
    
  def __str__(self):
    return f"Log: {self.id}, {self.timestamp}, {self.camera_id}, {self.detected_face_id}"