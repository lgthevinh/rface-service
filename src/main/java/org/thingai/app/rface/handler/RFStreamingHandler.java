package org.thingai.app.rface.handler;

import org.thingai.app.rface.define.RFVcodecType;
import org.thingai.app.rface.event.RFEventFrameCaptured;
import org.thingai.base.eda.EventBus;
import org.thingai.base.log.ILog;

import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.Arrays;

public class RFStreamingHandler implements Runnable {
    private static final String TAG = "RFStreamingHandler";
    private EventBus eventBus;
    private String rtspUrl; // current system only supports one streaming url
    private Process ffmpegProcess;
    private RFVcodecType vcodecType;
    private boolean isRunning = true;

    private static final int SOI_MARKER = 0xFFD8; // Start Of Image
    private static final int EOI_MARKER = 0xFFD9; // End Of Image

    public RFStreamingHandler(RFVcodecType vcodecType) {
        this.vcodecType = vcodecType;
    }

    @Override
    public void run() {
        if (rtspUrl == null || rtspUrl.isEmpty()) {
            ILog.e(TAG, "RTSP URL is not set.");
            throw new IllegalStateException("RTSP URL is not set.");
        }

        String[] command = {
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "error",
                "-rtsp_transport", "udp", // use UDP for RTSP transport, can be changed to tcp if needed for reliability
                "-i", rtspUrl,
                "-r", "5", // set frame rate to 10 fps
                "-an", // disable audio
                "-f", "image2pipe",
                "-vcodec", vcodecType.getCmdFlag(),
                "-q:v", "5",
                "-" // output to stdout
        };

        ProcessBuilder processBuilder = new ProcessBuilder(command);

        try {
            ILog.d(TAG, "Starting FFMPEG: " + Arrays.toString(command));
            ffmpegProcess = processBuilder.start();

            // Read FFMPEG's output stream
            try (BufferedInputStream in = new BufferedInputStream(ffmpegProcess.getInputStream())) {
                readStream(in);
            }

        } catch (IOException e) {
            ILog.e(TAG, "FFMPEG Error: " + e.getMessage());
        } finally {
            stop();
        }
    }

    private void readStream(BufferedInputStream in) throws IOException {
        // Buffer to build up the current JPEG image
        // 512KB is usually enough for a 1080p JPEG
        ByteArrayOutputStream imageBuffer = new ByteArrayOutputStream(512 * 1024);

        int prevByte = -1;
        int currByte;
        boolean isRecording = false;

        while (isRunning && (currByte = in.read()) != -1) {
            // Check for Start of Image (FF D8)
            if (prevByte == 0xFF && currByte == 0xD8) {
                imageBuffer.reset();
                imageBuffer.write(0xFF); // Write the FF we just missed
                imageBuffer.write(0xD8);
                isRecording = true;
                prevByte = currByte;
                continue;
            }

            if (isRecording) {
                imageBuffer.write(currByte);

                // Check for End of Image (FF D9)
                if (prevByte == 0xFF && currByte == 0xD9) {
                    isRecording = false;

                    // Convert to byte array
                    byte[] jpegBytes = imageBuffer.toByteArray();
                    ILog.d(TAG, "Captured JPEG frame of size: " + jpegBytes.length + " bytes");
                    eventBus.post(new RFEventFrameCaptured(jpegBytes, rtspUrl));
                }
            }
            prevByte = currByte;
        }
    }

    public void stop() {
        isRunning = false;
        if (ffmpegProcess != null && ffmpegProcess.isAlive()) {
            ffmpegProcess.destroy();
        }
    }

    public void setEventBus(EventBus eventBus) {
        this.eventBus = eventBus;
    }

    public void setRtspUrl(String rtspUrl) {
        this.rtspUrl = rtspUrl;
    }
}
