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
    
  def start(self):
    """Start the RTSP stream in a background thread"""
    self.running = True
    threading.Thread(target=self._capture_frames, daemon=True).start()

  def _capture_frames(self):
    """Continuously capture frames from the RTSP stream"""
    self.capture = cv2.VideoCapture(self.rtsp_url)
    self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    while self.running:
      ret, frame = self.capture.read()
      
      if not ret:
        self._reconnect()
        time.sleep(1) # Wait for 1 second before trying to reconnect
        continue
      
      with self.lock:
        self.frame = frame

  def _reconnect(self):
    """Reconnect to the RTSP stream if it disconnects"""
    if self.capture:
      self.capture.release()
    self.capture = cv2.VideoCapture(self.rtsp_url)
    self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

  def get_current_frame(self):
    """Retrieve the latest frame"""
    with self.lock:
      self.processing = True
      return self.frame.copy() if self.frame is not None else None
  
  def processing_done(self):
    """Set processing to False after processing the frame"""
    with self.lock:
      self.processing = False

  def stop(self):
    """Stop the RTSP stream"""
    self.running = False
    if self.capture:
      self.capture.release()
