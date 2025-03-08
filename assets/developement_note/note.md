# Development Note

### 1. Error: img must be numpy array or str but it is <class 'NoneType'> (05/03/2025)
- Problem: This error occurs when the image is not loaded or decode properly. Another reason is that in the base64 encoding content include the metadata of the image (e.g, data:image/jpeg;base64, ...). The image should be decoded properly before passing to the model.
- Solution: To solve this issue, we need to decode the image properly by removing the metadata of the image. The following code snippet shows how to decode the image properly:
```python
import base64
import cv2

def decode_image(base64_string):
    base64_string = base64_string.split(",")[1]
    imgdata = base64.b64decode(base64_string)
    image = cv2.imdecode(np.frombuffer(imgdata, np.uint8), cv2.IMREAD_COLOR)
    return image
```

### 2. AI Camera event HTTP request (08/03/2025)

AI Camera is a third-party camera that RFace AI Box has to integrate with. The AI Camera sends an HTTP request to the RFace AI Box when an event is triggered. The device provides 2 types of events: `alarm` and `notify`. The following is the request format:

#### Alarm HTTP Response 

- Status: `200 OK`
- Event config UI:

![AI Camera Platform Settings](/assets/images/note_img_1.png)

#### Event response parameters

| Parameters    | Type    | Reg.                | Notes                       |
|---------------|---------|---------------------|-----------------------------|
| device_id     | string  | `((DEVICE_ID))`     | DeviceCode                  |
| device_version| string  | `((DEVICE_VERSION))`| DeviceVersion               |
| date          | string  | `((DATE_FORMAT))`   | Datetime of the alarm       |
| timestamp     | integer | `((TIMESTAMP))`     | Utc timestamp of the alarm  |
| label         | string  | `((LABEL))`         | Classes of the alarm        |
| alias         | string  | `((ALIAS))`         | Classes alias               |
| count         | integer | `((COUNT))`         | Detection count             |
| img_base64    | string  | `((BASE64_IMAGE))`  | Snapshot of the alarm       |
| extend        | object  | `((EXTEND))`        | Extension info of the alarm |