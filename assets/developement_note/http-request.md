# HTTP Request interface for R-Face service

## Introduction

R-Face service provides facial recognition capabilities. It is built with deepface framework and mainly aim for edge devices (NanoPi R5C). The service provides multi interface for different purposes. The HTTP request interface is one of the interfaces that allows the user to interact with the service through HTTP requests.

### 1. Face registration

The face registration interface allows the user to register a face to the service. The user needs to provide the name of the person and the image of the person. The image should be encoded in base64 format. The following is the request format:

#### HTTP Request

- Method: `POST`
- URL: `http://192.168.1.2:5000/api/register_face`.
- Body:
```json
{
  "name": "John Doe",
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
  "message": "Face registered successfully",
  "embedding": [0.1, 0.2, ..., 0.9] // Face embedding
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
  "name": "John Doe",
  "distance": 0.1, // Distance between the input image and the registered face
  "verified": true // Whether the face is verified or not
}
```

### 3. Delete face from service's database

#### HTTP Request

- Method: `DELETE`
- URL: `http://192.168.100.59:5000/api/delete_face`
- Body:
```json
{
  "name": "John Doe"
}
```

#### Parameters

- `name` (string): The name of the person whose face needs to be deleted.

#### Response

- Status: `200 OK`
- Body:
```json
{
  "message": "Face deleted successfully"
}
```