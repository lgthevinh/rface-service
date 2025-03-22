import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from services.worker import BackgroundWorker
from services.face_recognition import FaceRecognition
from services.interface_manager import UartInterfaceManager

if __name__ == "__main__":
  
  data_path = "./data/"
  
  if not os.path.exists(data_path):
      os.makedirs(data_path)
    
  # Check DEEPFACE_HOME environment variable
  if "DEEPFACE_HOME" not in os.environ:
    os.makedirs("./data/.deepface/weights", exist_ok=True)
    os.environ["DEEPFACE_HOME"] = data_path
  
  FaceRecognition().set_model("Dlib")  
  FaceRecognition().set_threshold(0.06)
  
  worker = BackgroundWorker("RTSP Stream", "rtsp://192.168.100.129:8080/h264.sdp")
  worker.add_interface(UartInterfaceManager("UartInterface", "COM4", 115200))
  worker.start()
  
  print("Press 'q' to quit")
  
  while True:
    if input() == "q":
      worker.stop()
      break