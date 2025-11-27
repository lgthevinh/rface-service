package org.thingai.app;

// TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
    public static void main(String[] args) {
        RFaceService service = new RFaceService();
        service.name = "RFace Service";
        service.version = "1.0.0";
        service.appDirName = "rface_app";

        service.init();
    }
}