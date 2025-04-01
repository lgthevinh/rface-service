import sys
import os
import threading

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from services.rtsp_handler import RTSPHandler
from services.face_recognition import FaceRecognition
import cv2
from datetime import datetime

rtsp_stream = RTSPHandler("rtsp://192.168.1.175:8080/h264.sdp")

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

def write_frame_to_file_worker(frame):
  """Writes the latest frame to a file"""
  while True:
    # Write to file only if the frame is not None and evcery 5 seconds with timestamp
    if frame is not None:
      timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
      cv2.imwrite(f"frame_{timestamp}.jpg", frame)

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
      
      # Debugging: Output the frame to a file
      # cv2.imwrite("frame.jpg", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    
  rtsp_stream.stop()
  cv2.destroyAllWindows()