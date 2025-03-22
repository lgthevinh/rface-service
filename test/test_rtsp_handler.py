import sys
import os
import threading

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from services.rtsp_handler import RTSPHandler
from services.face_recognition import FaceRecognition
import cv2

rtsp_stream = RTSPHandler("rtsp://192.168.100.129:8080/h264.sdp")

def recognition_worker():
  """Runs the recognition task only on the latest frame"""
  while True:
    frame = rtsp_stream.get_current_frame()
    if frame is None:
      continue  # No frame yet, skip
    
    face, result = FaceRecognition().recognize(frame)
  
    if face is not None:
      print(f"Face recognized: {face.name}, distance: {result}")
      
    if face is None and result == 0:
      print(f"Face not recognized")
            
    if face is None and result is None:
      print("No face detected")


if __name__ == "__main__":
  
  FaceRecognition().set_model("Dlib")
  FaceRecognition().set_threshold(0.06)
  
  # Start recognition in a separate thread
  rtsp_stream.start()
  threading.Thread(target=recognition_worker, daemon=True).start()
  
  print("Press 'q' to quit")
  
  while True:   
    frame = rtsp_stream.get_current_frame()
    if frame is not None:
      cv2.imshow("RTSP Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    
  rtsp_stream.stop()
  cv2.destroyAllWindows()