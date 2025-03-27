import cv2
import threading
import time

class RTSPHandler:
  def __init__(self, rtsp_url):
    self.rtsp_url = rtsp_url
    self.capture = None
    self.frame = None
    self.running = False
    self.lock = threading.Lock()
    self.processing_done = False
    
  def start(self):
    """Start the RTSP stream in a background thread"""
    self.running = True
    self._set_capture()
    threading.Thread(target=self._capture_frames, daemon=True).start()

  def _capture_frames(self):
    """Continuously capture frames from the RTSP stream"""
    while self.running:
      ret, frame = self.capture.read()
      
      if not ret:
        self._reconnect()
        time.sleep(1) # Wait for 1 second before trying to reconnect
        continue
      
      with self.lock:
        self.frame = frame
        
      time.sleep(0.1)

  def _reconnect(self):
    """Reconnect to the RTSP stream if it disconnects"""
    if self.capture:
      self.capture.release()
    self._set_capture()

  def _set_capture(self):
    self.capture = cv2.VideoCapture(self.rtsp_url)
    self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    self.capture.set(cv2.CAP_PROP_FPS, 10)  # Reduce FPS for low-power devices

  def get_current_frame(self):
    """Retrieve the latest frame"""
    with self.lock:
      return self.frame.copy() if self.frame is not None else None

  def stop(self):
    """Stop the RTSP stream"""
    self.running = False
    if self.capture:
      self.capture.release()
