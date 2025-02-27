from flask import Flask, request, jsonify
from PIL import Image
import io
import base64

app = Flask(__name__)

# Define the POST endpoint
@app.route('/ipcamera', methods=['POST'])
def handle_ipcamera_post():
    try:
        # Get the JSON data from the request
        json_data = request.get_json()

        # Validate the JSON data
        if not json_data:
            return jsonify({'error': 'Invalid JSON data'}), 400

        # Process the JSON data
        # For example, you can save it to a database or send an alert
        image_bytes = base64.b64decode(json_data["img_base64"])
        image = Image.open(io.BytesIO(image_bytes))
        
        image.show()

        # Return a success response
        return jsonify({'message': 'JSON data received successfully'}), 200

    except Exception as e:
        # Return an error response
        return jsonify({'error': str(e)}), 500
      
# Define the POST endpoint for notifications
@app.route('/notify', methods=['POST'])
def handle_notify_post():
    try:
        # Get the JSON data from the request
        json_data = request.get_json()

        # Validate the JSON data
        if not json_data:
            return jsonify({'error': 'Invalid JSON data'}), 400

        # Process the notification data
        # For example, you can save it to a database or send an alert
        print('Received notification:', json_data)

        # Return a success response
        return jsonify({'message': 'Notification received successfully'}), 200

    except Exception as e:
        # Return an error response
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")