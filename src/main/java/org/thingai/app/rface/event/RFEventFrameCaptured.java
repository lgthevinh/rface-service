package org.thingai.app.rface.event;

public class RFEventFrameCaptured {
    private byte[] frameData;
    private int[] dimensions;
    private String rtspUrl;

    public RFEventFrameCaptured(byte[] frameData, int[] dimensions, String rtspUrl) {
        this.frameData = frameData;
        this.dimensions = dimensions;
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

    public int[] getDimensions() {
        return dimensions;
    }

    public void setDimensions(int[] dimensions) {
        this.dimensions = dimensions;
    }
}
