# RFace Service for Attendance System

## Architecture Overview

Web API (Flask):
  - Provides API for monitoring
  - Config service through API
  - Send/receive data from the client
Background worker:
  - Captures frames from RTSP URLs
  - Detects faces in the frames from selected RTSP URLs
Face Recognition Module:
  - Extracts face embeddings
  - Matches with stored database
Interface Manager:
  - Sends results via UART (USB) 
  - Logs results to file/database 
Database Layer (SQLite): 
  - Stores RTSP URLs, Face Embeddings, Logs