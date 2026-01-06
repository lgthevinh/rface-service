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
    self.thread = None
    
  def start(self):
    """Start the RTSP stream in a background thread"""
    try:
      if self.capture is not None:
        self.capture.release()
      self.running = True
      self.capture = cv2.VideoCapture(self.rtsp_url)
      self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
      self.thread = threading.Thread(target=self._capture_frames, daemon=True)
      self.thread.start()
    except Exception as e:
      self.running = False
      print(f"Error starting RTSP stream: {e}")
      if self.capture is not None:
        self.capture.release()
        self.capture = None
      return

  def _capture_frames(self):
    """Continuously capture frames from the RTSP stream"""
    while self.running:
      try: 
        ret, frame = self.capture.read()
        
        if not ret:
          self._reconnect()
          time.sleep(1) # Wait for 1 second before trying to reconnect
          continue
        
        with self.lock:
          self.frame = frame
      except Exception as e:
        print(f"Error capturing frame: {e}")
        self._reconnect()
        time.sleep(1)
        continue

  def _reconnect(self):
    """Reconnect to the RTSP stream if it disconnects"""
    if self.capture:
      self.capture.release()
    self._set_capture()

  def _set_capture(self):
    self.capture = cv2.VideoCapture(self.rtsp_url)
    self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

  def get_current_frame(self):
    """Retrieve the latest frame"""
    with self.lock:
      return self.frame.copy() if self.frame is not None else None

  def stop(self):
    """Stop the RTSP stream"""
    with self.lock:
      self.running = False
      if self.capture:
        self.capture.release()
      if self.thread is not None:
        self.thread.join(timeout=5.0)
        self.thread = None
