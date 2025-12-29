package org.thingai.app;

import org.thingai.app.rface.core.RFEventBus;
import org.thingai.app.rface.define.RFVcodecType;
import org.thingai.app.rface.entity.RFFaceEmbedding;
import org.thingai.app.rface.entity.RFFaceIdentity;
import org.thingai.app.rface.entity.RFKeyValue;
import org.thingai.app.rface.event.RFEventFaceRecognized;
import org.thingai.app.rface.event.RFEventFrameCaptured;
import org.thingai.app.rface.handler.RFEventHandler;
import org.thingai.app.rface.handler.RFRecognitionHandler;
import org.thingai.app.rface.handler.RFStreamingHandler;
import org.thingai.base.Service;
import org.thingai.base.ai.vector.dao.DaoVectorSqlite;
import org.thingai.base.ai.vector.define.DistanceMetric;
import org.thingai.base.dao.Dao;
import org.thingai.base.log.ILog;
import org.thingai.platform.dao.DaoFile;
import org.thingai.platform.dao.DaoSqlite;

import java.nio.file.Paths;

public class RFaceService extends Service {
    private Dao dao;
    private DaoFile daoFile;
    private DaoVectorSqlite daoVector;

    private RFStreamingHandler streamingHandler;
    private RFRecognitionHandler recognitionHandler;
    private RFEventHandler eventHandler;

    private RFEventBus eventBus;

    public RFaceService() {
        super();
    }

    @Override
    protected void onServiceInit() {
        // Initialize DAOs
        dao = new DaoSqlite(appDir + "/rface.db");
        daoFile = new DaoFile(appDir + "/files");

        // Detect OS and architecture for loading appropriate vector library
        String osName = System.getProperty("os.name").toLowerCase();
        String arch = System.getProperty("os.arch").toLowerCase();
        String extPath = "";
        ILog.d("RFaceService", "Operating System: " + osName, ", Architecture: " + arch);
        ILog.d("RFaceService", "Application Directory: " + appDir);

        if (osName.contains("win")) {
            ILog.d("RFaceService", "Running on Windows OS.");
            extPath = Paths.get("extlibs").toAbsolutePath() + "/vector-windows/vector.dll";
        } else if (osName.contains("nix") || osName.contains("nux") || osName.contains("aix")) {
            ILog.d("RFaceService", "Running on Linux/Unix OS.");
            if (arch.contains("arm") || arch.contains("aarch64")) {
                ILog.d("RFaceService", "Detected ARM architecture.");
                extPath = appDir + "/plugin/vector";
            }
        } else if (osName.contains("mac")) {
            ILog.d("RFaceService", "Running on macOS.");
            extPath = Paths.get("extlibs").toAbsolutePath() + "/vector-macos-arm/vector.dylib";
        } else {
            ILog.w("RFaceService", "Unsupported operating system: " + osName);
            throw new UnsupportedOperationException("Unsupported OS: " + osName);
        }

        // Initialize vector DAO and set up tables
        daoVector = new DaoVectorSqlite(appDir + "/rface.db", extPath);
        daoVector.initDao(new Class[]{
                RFFaceEmbedding.class
        });
        daoVector.initVectorSearch(RFFaceEmbedding.class, "embedding", 128, DistanceMetric.DEFAULT);

        dao.initDao(new Class[]{
                RFFaceIdentity.class,
                RFKeyValue.class
        });

        ILog.d("RFaceService", "Service initialized with DAO and file storage.");

        try {
            RFKeyValue kvCurrentRtspUrl;
            kvCurrentRtspUrl = dao.query(RFKeyValue.class, "key", "current_rtsp_url")[0];

            // Initialize EventBus and Handlers
            eventBus = new RFEventBus();
            eventHandler = new RFEventHandler();
            recognitionHandler = new RFRecognitionHandler();
            streamingHandler = new RFStreamingHandler(RFVcodecType.MJPEG);
            streamingHandler.setRtspUrl(kvCurrentRtspUrl.getValue());

            // Register handlers with the event bus
            eventBus.register(RFEventFrameCaptured.class, eventFrameCaptured -> {

            });

            eventBus.register(RFEventFaceRecognized.class, eventFaceRecognized -> {

            });

            streamingHandler.setEventBus(eventBus);
        } catch (Exception e) {
            ILog.e("RFaceService", "Error during service initialization: " + e.getMessage());
            throw new RuntimeException(e);
        }

    }

    public void start() {
        new Thread(() -> {
            ILog.d("RFaceService", "Service started.");
            // Service main loop or logic can be implemented here
            streamingHandler.run();
        }).start();
    }
}
