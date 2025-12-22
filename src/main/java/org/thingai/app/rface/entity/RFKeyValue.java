package org.thingai.app.rface.entity;

import org.thingai.base.dao.annotations.DaoColumn;
import org.thingai.base.dao.annotations.DaoTable;

@DaoTable(name = "rface_key_value")
public class RFKeyValue {
    @DaoColumn(name = "key", primaryKey = true)
    private String key;

    @DaoColumn(name = "value")
    private String value;

    public RFKeyValue(String key, String value) {
        this.key = key;
        this.value = value;
    }

    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
}
