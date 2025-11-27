package org.thingai.app;

import org.thingai.base.Service;
import org.thingai.base.dao.Dao;
import org.thingai.base.dao.DaoFile;
import org.thingai.base.dao.DaoSqlite;

public class RFaceService extends Service {
    private Dao dao;
    private DaoFile daoFile;

    @Override
    protected void onServiceInit() {
        dao = new DaoSqlite(appDir + "/rface.db");
        daoFile = new DaoFile(appDir + "/files");
    }
}
