package org.thingai.app.rface.enitity;

import org.thingai.base.dao.annotations.DaoColumn;
import org.thingai.base.dao.annotations.DaoTable;

@DaoTable(name = "face_identity")
public class RFFaceIdentity {
    @DaoColumn(name = "id", primaryKey = true)
    private String id;

    @DaoColumn(name = "name")
    private String name;

    @DaoColumn(name = "gender")
    private boolean gender;

    @DaoColumn(name = "age")
    private int age;

    @DaoColumn(name = "metadata")
    private String metadata;

    @DaoColumn(name = "timestamp")
    private long timestamp; // Unix timestamp of when the identity was created or last updated

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public boolean isGender() {
        return gender;
    }

    public void setGender(boolean gender) {
        this.gender = gender;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getMetadata() {
        return metadata;
    }

    public void setMetadata(String metadata) {
        this.metadata = metadata;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }
}
