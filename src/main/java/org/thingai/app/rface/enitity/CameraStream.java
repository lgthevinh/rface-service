package org.thingai.app.rface.enitity;

import org.thingai.base.dao.annotations.DaoColumn;
import org.thingai.base.dao.annotations.DaoTable;

@DaoTable(name = "camera_stream")
public class CameraStream {
    @DaoColumn(name = "id", primaryKey = true)
    private String id;

    @DaoColumn(name = "rtsp_url")
    private String rtspUrl;

    @DaoColumn(name = "name")
    private String name;
}
