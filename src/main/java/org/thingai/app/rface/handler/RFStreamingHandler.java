package org.thingai.app.rface.handler;

import org.thingai.app.rface.core.RFEventBus;
import org.thingai.app.rface.define.RFVcodecType;
import org.thingai.app.rface.event.RFEventFrameCaptured;
import org.thingai.base.log.ILog;

import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.Arrays;

public class RFStreamingHandler implements Runnable {
    private static final String TAG = "RFStreamingHandler";
    private RFEventBus eventBus;
    private String rtspUrl; // current system only supports one streaming url
    private Process ffmpegProcess;
    private boolean isRunning = true;

    private final RFVcodecType vcodecType;

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
                    int[] dimensions = getJpegDimensions(jpegBytes); // extract height and width from jpegBytes header
                    ILog.d(TAG, "readStream " + jpegBytes.length + " " + dimensions[0] + " " + dimensions[1]);

                    eventBus.post(new RFEventFrameCaptured(jpegBytes, dimensions, rtspUrl));
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

    public void setEventBus(RFEventBus eventBus) {
        this.eventBus = eventBus;
    }

    public void setRtspUrl(String rtspUrl) {
        this.rtspUrl = rtspUrl;
    }

    private int[] getJpegDimensions(byte[] jpegBytes) {
        int i = 0;
        // Check for SOI (Start of Image)
        if (jpegBytes[i] != (byte) 0xFF || jpegBytes[i + 1] != (byte) 0xD8) {
            return new int[]{0, 0}; // Not a JPEG
        }
        i += 2;

        while (i < jpegBytes.length) {
            // Find next marker (0xFF followed by a non-0xFF byte)
            while (i < jpegBytes.length && jpegBytes[i] != (byte) 0xFF) {
                i++;
            }
            while (i < jpegBytes.length && jpegBytes[i] == (byte) 0xFF) {
                i++;
            }
            if (i >= jpegBytes.length) break;

            byte marker = jpegBytes[i];
            i++; // Move past marker

            // 0xC0 is SOF0 (Start of Frame 0 - Baseline)
            // 0xC2 is SOF2 (Start of Frame 2 - Progressive)
            if (marker == (byte) 0xC0 || marker == (byte) 0xC2) {
                // Structure: [Length (2)] [Precision (1)] [Height (2)] [Width (2)]
                // Skip Length (2 bytes) and Precision (1 byte) -> Total 3 bytes
                i += 3;

                // Read Height (Big Endian)
                int height = ((jpegBytes[i] & 0xFF) << 8) | (jpegBytes[i + 1] & 0xFF);

                // Read Width (Big Endian)
                int width = ((jpegBytes[i + 2] & 0xFF) << 8) | (jpegBytes[i + 3] & 0xFF);

                return new int[]{width, height};
            }
            // Handle other markers (skip their payload)
            else {
                // Read length of the segment (2 bytes, Big Endian)
                int length = ((jpegBytes[i] & 0xFF) << 8) | (jpegBytes[i + 1] & 0xFF);
                // Length includes the 2 bytes for the length field itself, so we subtract 2 to get payload
                i += (length - 2) + 2;
            }
        }
        return new int[]{0, 0};
    }
}
