import threading
from services.rtsp_handler import RTSPHandler
from services.face_recognition import FaceRecognition
from services.interface_manager import InterfaceManager, UartInterfaceManager
from config import DATAJSON_PATH
import json

class BackgroundWorker:
  def __init__(self, name: str, rtsp_url: str):
    self.name = name
    self.rtsp_stream = RTSPHandler(rtsp_url)
    self.is_running = False
    self.output_interface = []
    self.face_recognition = FaceRecognition()
    
  def add_interface(self, interface: InterfaceManager):
    """Add an output interface to send the recognition result"""
    self.output_interface.append(interface)
    
  def start(self):
    """Start the background worker for face recognition for each RTSP stream"""
    self.is_running = True
    self.rtsp_stream.start()
    for interface in self.output_interface:
      interface.open()
    threading.Thread(target=self._run, daemon=True).start()
    
  def _run(self):
    while self.is_running:
      frame = self.rtsp_stream.get_current_frame()
      if frame is None:
        continue  # No frame yet, skip
        
      face, result = self.face_recognition.recognize(frame)
      
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

  def stop(self):
    """Stop the background worker"""
    self.is_running = False
    self.rtsp_stream.stop()
    
    for interface in self.output_interface:
      interface.close()
  
  def to_dict(self):
    return {
      "name": self.name,
      "rtsp_url": self.rtsp_stream.rtsp_url,
      "interfaces": [interface.to_dict() for interface in self.output_interface]
    }
  
  def add_output_interface(self, interface: InterfaceManager):
    self.output_interface.append(interface)
      
class WorkerManager:
  _instance = None
  worker_storage: list[BackgroundWorker] = []
  
  def __new___(cls): 
    if cls._instance is None:
      cls._instance = super(WorkerManager, cls).__new__(cls)
    return cls._instance

  def init(self):
    with open(DATAJSON_PATH, 'r') as f:
      data = json.load(f)

    for worker in data["workers"]:
      rtsp_url = worker["rtsp_url"]
      worker_name = worker["name"]
      bg_worker = BackgroundWorker(worker_name, rtsp_url)
      
      for interface in worker["interfaces"]:
        if interface["type"] == "uart":
          interface_name = interface["name"]
          port = interface["port"]
          baudrate = interface["baudrate"]
          timeout = interface["timeout"]
          interface_manager = UartInterfaceManager(interface_name, port, baudrate, timeout)
          bg_worker.add_interface(interface_manager)
      
      self.worker_storage.append(bg_worker)
    
  def save(self):
    data = {
      "workers": [worker.to_dict() for worker in self.worker_storage]
    }
    
    with open(DATAJSON_PATH, 'w') as f:
      json.dump(data, f, indent=2)
  
  def add_worker(self, worker: BackgroundWorker):
    for w in self.worker_storage:
      if w.name == worker.name:
        raise ValueError(f"Worker with name {worker.name} already exists")
    self.worker_storage.append(worker)
    self.save()
    
  def remove_worker(self, worker_name: str):
    for worker in self.worker_storage:
      if worker.name == worker_name:
        self.worker_storage.remove(worker)
        self.save()
        return
  
  def start_all_workers(self):
    for worker in self.worker_storage:
      worker.start()
      
  def stop_all_workers(self):
    for worker in self.worker_storage:
      worker.stop()