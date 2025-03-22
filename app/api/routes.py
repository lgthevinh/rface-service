from flask import Blueprint, request, jsonify
from services.database_manager import DatabaseManager
from services.face_recognition import FaceRecognition
from services.interface_manager import UartInterfaceManager
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
@api_blueprint.route("/config/interface", methods=["GET"])
def handle_interface_config():
  if request.method == "GET":
    
    if request.args.get("interface") == "uart":
      uartlist = UartInterfaceManager.get_uart_ports()
      return jsonify({"uart_ports": uartlist}), 200