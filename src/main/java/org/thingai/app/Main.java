package org.thingai.app;

import org.thingai.base.log.ILog;

public class Main {
    public static void main(String[] args) {
        RFaceService service = new RFaceService();
        service.name = "RFace Service";
        service.version = "1.0.0";
        service.appDirName = "rface_app";

        ILog.ENABLE_LOGGING = true;
        ILog.logLevel = ILog.DEBUG;

        service.init();
    }
}