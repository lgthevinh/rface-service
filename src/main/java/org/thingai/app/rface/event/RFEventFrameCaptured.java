package org.thingai.app.rface.event;

public class RFEventFrameCaptured {
    private byte[] frameData;
    private String rtspUrl;

    public RFEventFrameCaptured(byte[] frameData, String rtspUrl) {
        this.frameData = frameData;
        this.rtspUrl = rtspUrl;
    }

    public byte[] getFrameData() {
        return frameData;
    }

    public void setFrameData(byte[] frameData) {
        this.frameData = frameData;
    }

    public String getRtspUrl() {
        return rtspUrl;
    }

    public void setRtspUrl(String rtspUrl) {
        this.rtspUrl = rtspUrl;
    }
}
