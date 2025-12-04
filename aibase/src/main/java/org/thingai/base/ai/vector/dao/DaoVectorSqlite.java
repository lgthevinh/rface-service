package org.thingai.base.ai.vector.dao;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import org.thingai.base.log.ILog;

import java.sql.SQLException;

public class DaoVectorSqlite {
    private static final String TAG = "DaoVectorSqlite";
    private final String dbPath;
    private final String extPath; // vector extension library path
    private final HikariDataSource dataSource;

    public DaoVectorSqlite(String dbPath, String extPath) {
        this.dbPath = dbPath;
        this.extPath = extPath;

        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:sqlite:" + dbPath);
        config.setDriverClassName("org.sqlite.JDBC");
        config.setMaximumPoolSize(10);
        config.setConnectionTimeout(30000L);
        config.setIdleTimeout(600000L);
        config.setMaxLifetime(1800000L);
        config.addDataSourceProperty("journal_mode", "WAL");
        config.addDataSourceProperty("enable_load_extension", "true");

        this.dataSource = new HikariDataSource(config);

        try {
            configExt();
        } catch (SQLException e) {
            e.printStackTrace();
            ILog.e(TAG, "Failed to configure database");
        }
    }

    public void configExt() throws SQLException {
        ILog.d(TAG, "onConfigure: dbPath=" + dbPath + ", extPath=" + extPath);
        this.dataSource.getConnection().createStatement().execute("SELECT load_extension('" + extPath + "');");
    }

    public void initDao(Class[] classes) {
        ILog.d(TAG, "initDao: dbPath=" + dbPath + ", extPath=" + extPath);
    }
}
