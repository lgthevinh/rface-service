class Camera:
  def __init__(self, name: str, rtsp_url: str, id: int = None):
    self.name = name
    self.rtsp_url = rtsp_url
    self.id = id
  
  def __str__(self):
    return f"Camera({self.name}, {self.rtsp_url})"
  
  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "rtsp_url": self.rtsp_url
    }