import threading
from services.rtsp_handler import RTSPHandler
from services.face_recognition import FaceRecognition
from services.interface_manager import InterfaceManager, UartInterfaceManager, CustomUartInterface, LogInterfaceManager
from config import DATAJSON_PATH
import json

class BackgroundWorker:
  def __init__(self, name: str, rtsp_url: str, camera_id: int = None):
    self.name = name
    self.camera_id = camera_id
    self.rtsp_stream = RTSPHandler(rtsp_url)
    self.is_running = False
    self.output_interface = []
    self.face_recognition = FaceRecognition()
    self.thread = None
    
  def add_interface(self, interface: InterfaceManager):
    """Add an output interface to send the recognition result"""
    self.output_interface.append(interface)
    
  def start(self):
    """Start the background worker for face recognition for each RTSP stream"""
    try:
      self.is_running = True
      self.rtsp_stream.start()
      for interface in self.output_interface:
        interface.open()
      self.thread = threading.Thread(target=self._run, daemon=True)
      self.thread.start()
    except Exception as e:
      self.is_running = False
      print(f"Error starting worker {self.name}: {e}")
      for interface in self.output_interface:
        interface.close()
      return
    
  def _run(self):
    self.rtsp_stream.start()
    for interface in self.output_interface:
      interface.open()
      
    while self.is_running:
      frame = self.rtsp_stream.get_current_frame()
      if frame is None:
        continue  # No frame yet, skip
        
      face, result = self.face_recognition.recognize(frame)
      
      if face:
        print(f"Face recognized: {face.name}")
        for interface in self.output_interface:
          interface.push_verified_result({"face": face.to_dict(), "result": result})
      elif result == 0:
        print(f"Face not recognized")
        for interface in self.output_interface:
          interface.push_unverified_result({"result": result})
      else:
        print("No face detected")

  def stop(self):
    """Stop the background worker"""
    self.is_running = False
    self.rtsp_stream.stop()
    if self.thread is not None:
      self.thread.join(timeout=5.0)
      self.thread = None
    
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
        
        if interface["type"] == "cuart":
          interface_name = interface["name"]
          interface_manager = CustomUartInterface(interface_name)
          bg_worker.add_interface(interface_manager)
          
        if interface["type"] == "log":
          interface_name = interface["name"]
          camera_id = interface["camera_id"]
          interface_manager = LogInterfaceManager(camera_id=camera_id, name=interface_name)
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
      try: 
        worker.start()
      except Exception as e:
        print(f"Error starting worker {worker.name}: {e}")
        worker.stop()
      
  def stop_all_workers(self):
    for worker in self.worker_storage:
      worker.stop()