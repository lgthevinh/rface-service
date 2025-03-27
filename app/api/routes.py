from flask import Blueprint, request, jsonify
from services.database_manager import DatabaseManager
from services.face_recognition import FaceRecognition
from services.interface_manager import UartInterfaceManager
from services.worker import WorkerManager, BackgroundWorker
from models.camera import Camera
import numpy as np
import base64
import cv2

api_blueprint = Blueprint("api", __name__, url_prefix="/api")
db = DatabaseManager()
face_recognition = FaceRecognition()

@api_blueprint.route("/register_face", methods=["POST"])
def register_face():
  data = request.get_json()
  name = data.get("name")
  image_data = data.get("image")
  
  if not name or not image_data:
    return jsonify({"message": "Name and image data are required"}), 400
  
  # Check if the image data contain metadata (data:image)
  if "data:image" in image_data:
    image_bytes = base64.b64decode(image_data.split(",")[1])
  else:
    image_bytes = base64.b64decode(image_data)
    
  np_arr = np.frombuffer(image_bytes, np.uint8)
  img_array = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
  
  face_recognition.register(name, img_array)
  return jsonify({"message": "Face registered successfully"}), 200

@api_blueprint.route("/recognize_face", methods=["POST"])
def recognize_face():
  data = request.get_json()
  image_data = data.get("image")
  
  if not image_data:
    return jsonify({"error": "Image is required"}), 400
  # Check if the image data contain metadata (data:image)
  if "data:image" in image_data:
    image_bytes = base64.b64decode(image_data.split(",")[1])
  else:
    image_bytes = base64.b64decode(image_data)
    
  np_arr = np.frombuffer(image_bytes, np.uint8)
  img_array = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
  
  # Recognize the face
  face, result = face_recognition.recognize(img_array)
  if face is None:
    return jsonify({"message": "Face not recognized"}), 404
  return jsonify({"face": face.to_dict(), "result": result}), 200

@api_blueprint.route("/list_faces", methods=["GET"])
def list_faces():
  faces = db.get_all_faces()
  return jsonify([face.to_dict() for face in faces]), 200

# Face API v2
@api_blueprint.route("/v2/faces", methods=["GET", "DELETE"])
def handle_face():
  if request.method == "GET":
    faces = db.get_all_faces()
    return jsonify([face.to_dict() for face in faces]), 200
  
  if request.method == "DELETE":
    # Get face ID from params
    face_id = request.args.get("id")
    if not face_id:
      return jsonify({"error": "Face ID is required"}), 400
    
    db.delete_face(int(face_id))
    return jsonify({"message": "Face deleted successfully"}), 200
  
  return jsonify({"error": "Method not allowed"}), 405

# Configurations API
@api_blueprint.route("/config", methods=["GET"])
def handle_interface_config():
  if request.method == "GET":
    
    if request.args.get("interface") == "uart":
      uartlist = UartInterfaceManager.get_uart_ports()
      return jsonify({"uart_ports": uartlist}), 200
    
@api_blueprint.route("/config/cameras", methods=["GET", "POST", "DELETE"])
def handle_cameras():
  if request.method == "GET":
    cameras = db.get_all_cameras()
    return jsonify([camera.to_dict() for camera in cameras]), 200
  
  if request.method == "POST":
    data = request.get_json()
    name = data.get("name")
    rtsp_url = data.get("rtsp_url")
    
    if not name or not rtsp_url:
      return jsonify({"error": "Name and RTSP URL are required"}), 400
    
    db.store_camera(Camera(name, rtsp_url))
    return jsonify({"message": "Camera stored successfully"}), 200
  
  if request.method == "DELETE":
    camera_id = request.args.get("id")
    if not camera_id:
      return jsonify({"error": "Camera ID is required"}), 400
    
    db.delete_camera(int(camera_id))
    return jsonify({"message": "Camera deleted successfully"}), 200
    
@api_blueprint.route("/workers", methods=["GET", "POST", "DELETE"])
def workers_handler():
  if request.method == "GET":
    return jsonify([worker.to_dict() for worker in WorkerManager().worker_storage]), 200
  if request.method == "POST":
    data = request.get_json()
    
    camera_id = data.get("camera_id")
    worker_name = data.get("name")
    
    # Get RTSP URL from camera ID
    camera = db.get_camera(camera_id)
    rtsp_url = camera.rtsp_url
    
    bg_worker = BackgroundWorker(worker_name, rtsp_url)
    
    interfaces = data.get("interfaces")
    for interface in interfaces:
      if interface["type"] == "uart":
        interface_name = interface["name"]
        port = interface["port"]
        baudrate = interface["baudrate"]
        timeout = interface["timeout"]
        interface_manager = UartInterfaceManager(interface_name, port, baudrate, timeout)
        bg_worker.add_output_interface(interface_manager)

    try:
      WorkerManager().add_worker(bg_worker)
    except Exception as e:
      return jsonify({"error": str(e)}), 400
    
    return jsonify({"message": "Worker created successfully", "worker": bg_worker.to_dict()}), 200
  if request.method == "DELETE":
    data = request.get_json()
    worker_name = data.get("name")
    if not worker_name:
      return jsonify({"error": "Worker name is required"}), 400
    
    WorkerManager().remove_worker(worker_name)
    return jsonify({"message": "Worker deleted successfully"}), 200