import threading
from services.rtsp_handler import RTSPHandler
from services.face_recognition import FaceRecognition
from services.interface_manager import InterfaceManager

class BackgroundWorker:
  def __init__(self, name: str, rtsp_url: str):
    self.name = name
    self.rtsp_stream = RTSPHandler(rtsp_url)
    self.is_running = False
    self.output_interface = []
    
  def add_interface(self, interface: InterfaceManager):
    """Add an output interface to send the recognition result"""
    self.output_interface.append(interface)
    
  def start(self):
    """Start the background worker for face recognition for each RTSP stream"""
    self.is_running = True
    self.rtsp_stream.start()
    threading.Thread(target=self._run, daemon=True).start()
    
  def _run(self):
    while self.is_running:
      frame = self.rtsp_stream.get_current_frame()
      if frame is None:
        continue  # No frame yet, skip
        
      face, result = FaceRecognition().recognize(frame)
      
      if face is not None:
        print(f"Face recognized: {face.name}")
        for interface in self.output_interface:
          interface.push_verified_result({"face": face.to_dict(), "result": result})
      
      if face is None and result == 0:
        print(f"Face not recognized")
        for interface in self.output_interface:
          interface.push_unverified_result({"result": result})
              
      if face is None and result is None:
        print("No face detected")

      # skip the previous frame just get the latest frame
      self.rtsp_stream.processing_done()

  def stop(self):
    """Stop the background worker"""
    self.is_running = False
    self.rtsp_stream.stop()
    
    for interface in self.output_interface:
      interface.close()