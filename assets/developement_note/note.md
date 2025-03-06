# Development Note

1. Error: img must be numpy array or str but it is <class 'NoneType'>
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