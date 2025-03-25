# RFace Service for Attendance System

## Introduction

RFace is a service that provides facial recognition capabilities. It is built with deepface framework and mainly aim for edge devices (NanoPi R5C)

## Installation

Before installing the service, you need to have python3 installed on your device, and the recommended version is 3.12 and above. You can install python3 by running the following command.:

```bash
sudo apt-get install python3>=3.12
```

Installing dependencies:
```bash
pip install -r requirements.txt
```

The installation process on NanoPi may take a lot of time, so please be patient.

## Test
To test the service, please navigate to the test folder and run the following command:
```bash
python test_background_worker.py
```

## Run
To run the service, run the main.py file:
```bash
python app/main.py
```

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