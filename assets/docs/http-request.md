# HTTP Request interface for R-Face service

## Introduction

R-Face service provides facial recognition capabilities. It is built with deepface framework and mainly aim for edge devices (NanoPi R5C). The service provides multi interface for different purposes. The HTTP request interface is one of the interfaces that allows the user to interact with the service through HTTP requests.

## Basic Face API

### 0. Ping for service availability

The ping interface allows the user to check the availability of the service. The following is the request format:

#### HTTP Request

- Method: `GET`
- URL: `http://192.168.1.2:5000/ping`.
- Body: None

#### Response

- Status: `200 OK`
- Body:
```json
{
  "message": "Pong! RFace Service is here!"
}
```

### 1. Face registration

The face registration interface allows the user to register a face to the service. The user needs to provide the name of the person and the image of the person. The image should be encoded in base64 format. The following is the request format:

#### HTTP Request

- Method: `POST`
- URL: `http://192.168.1.2:5000/api/register_face`.
- Body:
```json
{
  "name": "john_doe",
  "image": "base64_encoded_image"
}
```

#### Parameters

- `name` (string): The name of the person.
- `image` (string): The image of the person encoded in base64 format.

#### Response

- Status: `200 OK`
- Body:
```json
{
  "data": {
    "embedding": [...], // Face embedding
    "name": "john_doe"
  },
  "message": "Face registered successfully"
}
```

### 2. Face recognition

The face recognition interface allows the user to recognize a face from the service. The user needs to provide the image of the person. The image should be encoded in base64 format. The following is the request format:

#### HTTP Request

- Method: `POST`
- URL: `http://192.168.1.2:5000/api/recognize_face`.
- Body:
```json
{
  "image": "base64_encoded_image"
}
```

#### Parameters

- `image` (string): The image of the person encoded in base64 format.

#### Response

- Status: `200 OK`
- Body:
```json
{
  "name": "john_doe", // Name/ID of the recognized face
  "distance": 0.1, // Distance between the input image and the registered face
  "verified": true // Whether the face is verified or not
}
```

### 3. Delete face from service's database (deprecated, removed in v1)

#### HTTP Request

- Method: `DELETE`
- URL: `http://192.168.100.59:5000/api/delete_face`
- Body:
```json
{
  "name": "john_doe"
}
```

#### Parameters

- `name` (string): The name of the person whose face needs to be deleted.

#### Response

- Status: `200 OK`
- Body:
```json
{
    "message": "Face deleted with name: jjohn_doe"
}
```

### 3.1 Delete face from service's database (v1)

#### HTTP Request

- Method: `DELETE`
- URL: `http://192.168.100.59:2248/api/v2/faces?id=6`
- Body: None
- Parameters:
  - `id` (int): The ID of the face to be deleted. (For example, `id=6`)

#### Response

- Status: `200 OK`
- Body:
```json
{
  "message": "Face deleted successfully"
}
```

### 4. List all registered faces

#### HTTP Request

- Method: `GET`
- URL: `http://192.168.1.51:2248/api/list_faces`
- Body: None

#### Response

- Status: `200 OK`
- Body:
```json
{
  "data": [
    {
      "id": 1,
      "name": "john_doe",
    }
  ],
  "message": "success"
}
```

### 4.1 List all registered faces (v1, v2 API)

#### HTTP Request

- Method: `GET`
- URL: `http://192.168.100.59:2248/api/v2/faces`
- Body: None

#### Response

- Status: `200 OK`
- Body:
```json
{
  "data": [
    {
      "id": 1,
      "name": "john_doe",
    }
  ],
  "message": "success"
}
```

## Workers

### 1. List all registered workers

#### HTTP Request

- Method: `GET`
- URL: `http://192.168.100.59:2248/api/workers`
- Body: None

#### Response

- Status: `200 OK`
- Return an array list of workers
- Body:
```json
[
  {
    "interfaces": [
      {
        "baudrate": 115200,
        "name": "UartInterface",
        "port": "COM4",
        "timeout": 1000,
        "type": "uart"
      }
    ],
    "name": "RTSP Stream",
    "rtsp_url": "rtsp://192.168.100.129:8080/h264.sdp"
  }
]
```

### 2. Add a new worker

#### HTTP Request

- Method: `POST`
- URL: `http://192.168.100.59:2248/api/workers`
- Example body:
```json
{
  "name": "RTSP Stream",
  "camera_id": 1,
  "interfaces": [
    {
      "type": "uart",
      "name": "UartInterface",
      "port": "COM4",
      "baudrate": 9600,
      "timeout": 1000
    }
  ]
}
```

#### Response

- Status: `200 OK`
- Body:
```json
{
  "message": "Worker created successfully",
  "worker": {
    "interfaces": [
      {
        "baudrate": 115200,
        "name": "UartInterface",
        "port": "COM4",
        "timeout": 1000,
        "type": "uart"
      }
    ],
    "name": "RTSP Stream",
    "rtsp_url": "rtsp://192.168.100.129:8080/h264.sdp"
  }
}
```

### 3. Delete a worker

- Method: `DELETE`
- URL: `http://192.168.1.53:2248/api/workers`
- Example body:
```json
{
  "name": "RTSP Stream"
}
```

#### Response

- Status: `200 OK`
- Body:
```json
{
  "message": "Worker deleted successfully"
}
```

## Interface

### Scan for UART interfaces (port)

#### HTTP Request

- Method: `GET`
- URL: `http://192.168.100.59:2248/api/config?interface=uart`
- Body: None

#### Response

- Status: `200 OK`
- Body:
```json
{
  "uart_ports": [
    "COM5",
    "COM8"
  ]
}
```

## Camera

### 1. List all registered cameras

#### HTTP Request

- Method: `GET`
- URL: `http://{{url}}/api/config/cameras`
- Body: None

#### Response

- Status: `200 OK`
- Body:
```json
[
  {
    "id": 6,
    "name": "Wyze Cam 1",
    "rtsp_url": "rtsp://vinh:030805@192.168.100.152/live"
  },
  {
    "id": 7,
    "name": "Bova Cam",
    "rtsp_url": "rtsp://192.168.1.188/0"
  }
]
```

### 2. Add a new camera

#### HTTP Request

- Method: `POST`
- URL: `http://{{url}}/api/config/cameras`
- Body:
```json
{
  "name": "Bova Cam",
  "rtsp_url": "rtsp://192.168.1.188/0"
}
```

#### Response

- Status: `200 OK`
- Body: 
```json
{
  "message": "Camera stored successfully"
}
```

### 3. Delete a camera

#### HTTP Request

- Method: `DELETE`
- URL: `http://{{url}}/api/config/cameras?id=6`
- Parameters:
  - `id` (int): The ID of the camera to be deleted. (For example, `id=6`)
- Body: None

#### Response

- Status: `200 OK`
- Body:
```json
{
  "message": "Camera deleted successfully"
}
```

## Background worker

### 1. List all workers

#### HTTP Request

- Method: `GET`
- URL: `http://{{url}}/api/workers`
- Body: None

#### Response

- Status: `200 OK`
- Body:
```json
[
    {
        "interfaces": [
            {
                "name": "CUartInterface",
                "timeout": 1,
                "type": "cuart"
            },
            {
                "camera_id": 6,
                "name": "LogInterface",
                "type": "log"
            }
        ],
        "name": "RTSP Stream",
        "rtsp_url": "rtsp://vinh:030805@192.168.100.152/live"
    },
    {
        "interfaces": [
            {
                "name": "CUartInterface",
                "timeout": 1,
                "type": "cuart"
            },
            {
                "camera_id": 7,
                "name": "LogInterface",
                "type": "log"
            }
        ],
        "name": "RTSP Stream 1",
        "rtsp_url": "rtsp://192.168.1.188/0"
    }
]
```

### 2. Add a new worker

#### HTTP Request

- Method: `POST`
- URL: `http://{{url}}/api/workers`

- Body:
```json
{
  "name": "RTSP Stream",
  "camera_id": 1,
  "interfaces": [
    {
      "type": "uart",
      "name": "UartInterface",
      "port": "COM4",
      "baudrate": 9600,
      "timeout": 1000
    }
  ]
}
```

#### Response

- Status: `200 OK`
- Body: 
```json
{
  "message": "Worker created successfully",
  "worker": {
    "interfaces": [
      {
        "name": "CUartInterface",
        "timeout": 1,
        "type": "cuart"
      },
      {
        "camera_id": 7,
        "name": "LogInterface",
        "type": "log"
      }
    ],
    "name": "RTSP Stream 1",
    "rtsp_url": "rtsp://192.168.1.188/0"
  }
}
```

### 3. Delete a worker

#### HTTP Request

- Method: `DELETE`
- URL: `http://{{url}}/api/workers`
- Post body: 
```json
{
  "name": "RTSP Stream" // Name of the worker to be deleted
}
```

#### Response

- Status: `200 OK`
- Body:
```json
{
  "message": "Worker deleted successfully"
}
```

### 4. Start a worker

#### HTTP Request

- Method: `POST`
- URL: `http://{{url}}/api/workers/start?name=RTSP Stream 1`
- Parameters:
  - `name` (string): The name of the worker to be started. (For example, `name=RTSP Stream 1`). Or to start all workers, use `name=all`.
- Body: None

#### Response

- Status: `200 OK`
- Body:
```json
{
  "message": "Worker started successfully"
}
```

### 5. Stop a worker

#### HTTP Request

- Method: `POST`
- URL: `http://{{url}}/api/workers/stop?name=RTSP Stream 1`
- Parameters:
  - `name` (string): The name of the worker to be stopped. (For example, `name=RTSP Stream 1`). Or to stop all workers, use `name=all`.
- Body: None

#### Response

- Status: `200 OK`
- Body:
```json
{
  "message": "Worker stopped successfully"
}
```

### 6. Get logs

#### HTTP Request

- Method: `GET`
- URL: `http://{{url}}/api/logs`
- Body: None

#### Response

- Status: `200 OK`
- Body:
```json
[
    {
        "camera_id": 6,
        "detected_face_id": 3,
        "id": 10,
        "timestamp": "2025-04-09 17:49:37"
    },
    {
        "camera_id": 6,
        "detected_face_id": 3,
        "id": 11,
        "timestamp": "2025-04-09 17:49:38"
    },
    {
        "camera_id": 7,
        "detected_face_id": null,
        "id": 30,
        "timestamp": "2025-04-11 08:20:09"
    }
  ]
```