import os

from flask import Flask, jsonify
from api.routes import api_blueprint
from services.face_recognition import FaceRecognition

data_path = "./data/"
if not os.path.exists(data_path):
  os.makedirs(data_path)
    
# Check DEEPFACE_HOME environment variable
if "DEEPFACE_HOME" not in os.environ:
  os.makedirs("./data/.deepface/weights", exist_ok=True)
  os.environ["DEEPFACE_HOME"] = data_path

app = Flask(__name__)
app.register_blueprint(api_blueprint)

@app.route("/ping", methods=["GET"])
def ping():
  return jsonify({"message": "Pong! RFace Service is here!"}), 200

if __name__ == "__main__":  
  FaceRecognition().set_model("Dlib")  
  FaceRecognition().set_threshold(0.04)
  
  app.run(host="0.0.0.0", port="2248", debug=True)
