import os
import cv2
from services.database_manager import DatabaseManager
from services.worker import WorkerManager
from services.face_recognition import FaceRecognition
from config import DATAPATH, DATAJSON_PATH

class AppConfig():
  def __new___(cls): 
    if cls._instance is None:
      cls._instance = super(AppConfig, cls).__new__(cls)
      cls._instance.workers = []
      cls._instance.db = DatabaseManager()
    return cls._instance
  
  def init(self):
    if not os.path.exists(DATAPATH):
      os.makedirs(DATAPATH)
        
    # Check DEEPFACE_HOME environment variable
    if "DEEPFACE_HOME" not in os.environ:
      os.makedirs("./data/.deepface/weights", exist_ok=True)
      os.environ["DEEPFACE_HOME"] = DATAPATH
    
    if not os.path.exists(DATAJSON_PATH):
      with open(DATAJSON_PATH, 'w') as f:
        f.write('{"workers":[]}')
      
    FaceRecognition().set_model("Dlib")  
    FaceRecognition().set_threshold(0.06)
    
    wm = WorkerManager()
    wm.init()
    
    # print(cv2.getBuildInformation())
    try: 
      cv2.ocl.setUseOpenCL(True)
    except Exception:
      print("OpenCV cannot use OpenCL")
    
    # Debugging
    # for index, worker in enumerate(wm.worker_storage):
    #   print(f"Worker {index}: {worker.to_dict()}")