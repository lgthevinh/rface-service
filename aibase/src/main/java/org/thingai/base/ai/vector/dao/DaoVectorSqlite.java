package org.thingai.base.ai.vector.dao;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import org.sqlite.SQLiteConfig;
import org.thingai.base.log.ILog;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DaoVectorSqlite {
    private static final String TAG = "DaoVectorSqlite";
    private final String dbPath;
    private final String extPath; // vector extension library path
    private Connection connection;

    public DaoVectorSqlite(String dbPath, String extPath) {
        this.dbPath = dbPath;
        this.extPath = extPath;

        SQLiteConfig config = new SQLiteConfig();
        config.enableLoadExtension(true);
        config.setJournalMode(SQLiteConfig.JournalMode.WAL);

        try {
            this.connection = DriverManager.getConnection("jdbc:sqlite:" + dbPath, config.toProperties());
            configExt();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    public void configExt() throws SQLException {
        ILog.d(TAG, "onConfigure: dbPath=" + dbPath + ", extPath=" + extPath);
        this.connection.createStatement().execute("PRAGMA enable_load_extension = 1;");
        this.connection.createStatement().execute("SELECT load_extension('" + extPath + "');");
    }

    public void initDao(Class[] classes) {
        ILog.d(TAG, "initDao: dbPath=" + dbPath + ", extPath=" + extPath);
    }
}
