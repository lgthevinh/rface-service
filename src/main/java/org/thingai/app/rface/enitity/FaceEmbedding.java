package org.thingai.app.rface.enitity;

import org.thingai.base.ai.vector.dao.DaoEmbedding;
import org.thingai.base.dao.annotations.DaoColumn;
import org.thingai.base.dao.annotations.DaoTable;

@DaoTable(name = "face_embedding")
public class FaceEmbedding {

    @DaoColumn(name = "id", primaryKey = true)
    private String id;

    @DaoColumn(name = "embedding")
    @DaoEmbedding
    private float[] embedding;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public float[] getEmbedding() {
        return embedding;
    }

    public void setEmbedding(float[] embedding) {
        this.embedding = embedding;
    }
}
