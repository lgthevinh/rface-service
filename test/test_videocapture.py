from flask import Flask, request, Response
import numpy as np
import cv2
import os
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Create output directory
OUTPUT_DIR = "received_frames"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class IPCamera:
    def __init__(self, url):
        self.url = url
        self.frame = None
        self.running = False
        self.lock = threading.Lock()
        

    def start(self):
        self.running = True
        thread = threading.Thread(target=self._capture_loop)
        thread.daemon = True
        thread.start()

    def _capture_loop(self):
        cap = cv2.VideoCapture(self.url)
        
        if not cap.isOpened():
            print(f"Error: Could not open camera stream: {self.url}")
            return

        while self.running:
            ret, frame = cap.read()
            print(ret)
            if frame is not None:
                print(frame.shape)  # This will print (height, width, channels)
            if not ret:
                print("Error: Can't receive frame")
                time.sleep(1)  # Wait before retrying
                cap = cv2.VideoCapture(self.url)  # Try to reconnect
                continue

            with self.lock:
                self.frame = frame
                # Save the frame
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = os.path.join(OUTPUT_DIR, f"frame_{timestamp}.jpg")
                cv2.imwrite(filename, frame)
                # print(f"Saved frame: {filename}")
            
            # Add a small delay to not overwhelm the camera
            time.sleep(0.1)

        cap.release()

    def stop(self):
        self.running = False

    def get_frame(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

# Example 1: Using an MJPEG stream from a traffic camera
camera = IPCamera('rtsp://admin:admin@192.168.1.29:554/stream1')


# Example 2: If you have a local IP camera (uncomment and modify as needed)
# For Hikvision:
# camera = IPCamera('rtsp://admin:password123@192.168.1.64:554/Streaming/Channels/1')
# For Dahua:
# camera = IPCamera('rtsp://admin:password123@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0')
# For generic ONVIF camera:
# camera = IPCamera('rtsp://admin:password123@192.168.1.100:554/onvif1')

@app.route('/start', methods=['GET'])
def start_stream():
    camera.start()
    print("start stream")
    return "Stream started", 200

@app.route('/stop', methods=['GET'])

def stop_stream():
    print("stop stream")
    camera.stop()
    return "Stream stopped", 200

if __name__ == "__main__":
    camera.start()
    app.run(host='0.0.0.0', port=5000)
