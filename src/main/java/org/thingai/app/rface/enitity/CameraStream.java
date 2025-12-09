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

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getRtspUrl() {
        return rtspUrl;
    }

    public void setRtspUrl(String rtspUrl) {
        this.rtspUrl = rtspUrl;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
