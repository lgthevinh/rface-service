package org.thingai.app;

import org.thingai.base.Service;
import org.thingai.base.dao.Dao;
import org.thingai.base.dao.DaoFile;
import org.thingai.base.dao.DaoSqlite;
import org.thingai.base.log.ILog;

public class RFaceService extends Service {
    private Dao dao;
    private DaoFile daoFile;

    @Override
    protected void onServiceInit() {
        dao = new DaoSqlite(appDir + "/rface.db");
        daoFile = new DaoFile(appDir + "/files");

        ILog.d("RFaceService", "Service initialized with DAO and file storage.");
    }
}
