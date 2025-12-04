package org.thingai.app;

import org.thingai.base.Service;
import org.thingai.base.ai.vector.dao.DaoVectorSqlite;
import org.thingai.base.dao.Dao;
import org.thingai.base.dao.DaoFile;
import org.thingai.base.dao.DaoSqlite;
import org.thingai.base.log.ILog;

import java.nio.file.Paths;

public class RFaceService extends Service {
    private Dao dao;
    private DaoFile daoFile;
    private DaoVectorSqlite daoVector;

    @Override
    protected void onServiceInit() {
        dao = new DaoSqlite(appDir + "/rface.db");
        daoFile = new DaoFile(appDir + "/files");

        String osName = System.getProperty("os.name").toLowerCase();
        String arch = System.getProperty("os.arch").toLowerCase();
        String extPath = "";
        ILog.d("RFaceService", "Operating System: " + osName, ", Architecture: " + arch);

        if (osName.contains("win")) {
            ILog.d("RFaceService", "Running on Windows OS.");
            extPath = Paths.get("extlibs").toAbsolutePath() + "/vector-windows/vector.dll";
        } else if (osName.contains("nix") || osName.contains("nux") || osName.contains("aix")) {
            ILog.d("RFaceService", "Running on Linux/Unix OS.");
            if (arch.contains("arm") || arch.contains("aarch64")) {
                ILog.d("RFaceService", "Detected ARM architecture.");
                extPath = Paths.get("extlibs").toAbsolutePath() + "/vector-linux-arm/vector.so";
            }
        } else if (osName.contains("mac")) {
            ILog.d("RFaceService", "Running on macOS.");
            extPath = Paths.get("extlibs").toAbsolutePath() + "/vector-macos-arm/vector.dylib";
        } else {
            ILog.w("RFaceService", "Unsupported operating system: " + osName);
            throw new UnsupportedOperationException("Unsupported OS: " + osName);
        }
        daoVector = new DaoVectorSqlite(appDir + "/rface.db", extPath);

        ILog.d("RFaceService", "Service initialized with DAO and file storage.");
    }
}
