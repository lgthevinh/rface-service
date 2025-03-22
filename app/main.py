from flask import Flask, jsonify
from api.routes import api_blueprint
from app_config import AppConfig

app = Flask(__name__)
app.register_blueprint(api_blueprint)

@app.route("/ping", methods=["GET"])
def ping():
  return jsonify({"message": "Pong! RFace Service is here!"}), 200

if __name__ == "__main__":
  AppConfig().init()
  app.run(host="0.0.0.0", port="2248", debug=True)
