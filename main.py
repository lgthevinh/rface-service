from rface.RFace import RFace
from flask import request, jsonify
import numpy as np
import base64
import cv2

rface = RFace()

rface.data_path = "./data/"
rface.init()

rface.face_reg.set_model("Dlib")
rface.face_reg.set_threshold(0.06)

app = rface.result_publisher.app

@app.route("/ping", methods=["GET"])
def ping():
  return "Pong!"

@app.route("/api/register_face", methods=["POST"])
def register_face():
  data = request.get_json()
  name = data.get("name")
  image_data = data.get("image")
  
  if not name or not image_data:
    return jsonify({"error": "Name and image are required"}), 400
  
  # Decode the base64 image
  image_bytes = base64.b64decode(image_data.split(",")[1])
  np_arr = np.frombuffer(image_bytes, np.uint8)
  img_array = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
  
  # Register the face
  embedding = rface.register_face(img_array, name)
  
  if embedding is None:
    return jsonify({"error": "Face registration failed"}), 500
  
  return jsonify({"message": "Face registered successfully", "embedding": embedding.tolist()}), 200

@app.route("/api/recognize_face", methods=["POST"])
def recognize_face():
  data = request.get_json()
  image_data = data.get("image")
  
  if not image_data:
    return jsonify({"error": "Image is required"}), 400
  
  # Decode the base64 image
  image_bytes = base64.b64decode(image_data.split(",")[1])
  np_arr = np.frombuffer(image_bytes, np.uint8)
  img_array = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
  
  # Recognize the face
  result = rface.recognize_face(img_array)
  
  return jsonify(result), 200

@app.route("/api/delete_face", methods=["DELETE"])
def delete_face():
  data = request.get_json()
  name = data.get("name")
  
  if not name:
    return jsonify({"error": "Name is required"}), 400
  
  # Delete the face
  rface.db.delete_embedding(name)
  
  return jsonify({"message": "Face deleted successfully"}), 200

if __name__ == "__main__":
  rface.run_result_publisher(debug=True)