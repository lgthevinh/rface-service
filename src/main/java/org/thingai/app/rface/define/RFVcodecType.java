package org.thingai.app.rface.define;

public enum RFVcodecType {
    H264_RKMPP,
    MJPEG;

    public String getCmdFlag() {
        switch (this) {
            case H264_RKMPP:
                return "h264_rkmpp";
            case MJPEG:
                return "mjpeg";
            default:
                return "unknown";
        }
    }
}
