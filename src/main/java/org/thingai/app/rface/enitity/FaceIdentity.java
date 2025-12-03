package org.thingai.app.rface.enitity;

import org.thingai.base.dao.annotations.DaoColumn;
import org.thingai.base.dao.annotations.DaoTable;

@DaoTable(name = "face_identity")
public class FaceIdentity {
    @DaoColumn(name = "id", primaryKey = true)
    private String id;

    @DaoColumn(name = "name")
    private String name;

    @DaoColumn(name = "metadata")
    private String metadata;

    @DaoColumn(name = "timestamp")
    private long timestamp; // Unix timestamp of when the identity was created or last updated
}
