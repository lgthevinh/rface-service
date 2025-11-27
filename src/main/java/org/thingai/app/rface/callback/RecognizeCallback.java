package org.thingai.app.rface.callback;

public interface RecognizeCallback {
    void onRecognize(String cameraId, String faceId, float confidence);
    void onUnrecognized(String cameraId, float confidence);
}
