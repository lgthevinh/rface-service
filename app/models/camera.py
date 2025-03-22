class Camera:
  def __init__(self, name: str, rtsp_url: str):
    self.name = name
    self.rtsp_url = rtsp_url
    self._id = None
  
  def __str__(self):
    return f"Camera({self.name}, {self.rtsp_url})"