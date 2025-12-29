package org.thingai.base.ai.vector.dao;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import org.thingai.base.ai.vector.define.DistanceMetric;
import org.thingai.platform.dao.DaoSqlite;
import org.thingai.base.dao.annotations.DaoColumn;
import org.thingai.base.dao.annotations.DaoTable;
import org.thingai.base.log.ILog;

import java.lang.reflect.Field;
import java.sql.Connection;
import java.sql.PreparedStatement;

public class DaoVectorSqlite extends DaoSqlite {
    private static final String TAG = "DaoVectorSqlite";
    private final String dbPath;
    private final String extPath; // vector extension library path
    private final HikariDataSource dataSource;

    public DaoVectorSqlite(String dbPath, String extPath) {
        super(dbPath);
        this.dbPath = dbPath;

        // Convert extPath characters if necessary (e.g., for Windows paths)
        this.extPath = extPath.replace("\\", "/");

        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:sqlite:" + dbPath);
        config.setDriverClassName("org.sqlite.JDBC");
        config.setMaximumPoolSize(10);
        config.setConnectionTimeout(30000L);
        config.setIdleTimeout(600000L);
        config.setMaxLifetime(1800000L);
        config.addDataSourceProperty("enable_load_extension", "true");
        config.setConnectionInitSql("SELECT load_extension('" + this.extPath + "');");

        this.dataSource = new HikariDataSource(config);
    }

    @Override
    public <T> void insertOrUpdate(T t) {
        if (t == null) {
            return;
        }
        Class<?> clazz = t.getClass();

        String query = "INSERT OR REPLACE INTO " + clazz.getAnnotation(DaoTable.class).name() + " (";
        StringBuilder columns = new StringBuilder();
        StringBuilder placeholders = new StringBuilder();
        Field[] fields = getAllFields(clazz);

        for(Field field : fields) {
            DaoColumn daoColumn = (DaoColumn)field.getAnnotation(DaoColumn.class);
            if (daoColumn != null) {
                columns.append(daoColumn.name().isEmpty() ? field.getName() : daoColumn.name()).append(", ");

                placeholders.append("?, ");
            }
        }

        if (columns.length() > 0) {
            columns.setLength(columns.length() - 2);
            placeholders.setLength(placeholders.length() - 2);
        }

        query = query + (columns) + ") VALUES (" + (placeholders) + ");";
        try (Connection connection = this.dataSource.getConnection()) {
            connection.createStatement().execute("SELECT load_extension('" + extPath + "');");
            PreparedStatement preparedStatement = connection.prepareStatement(query);
            int index = 1;

            for(Field field : fields) {
                DaoColumn daoColumn = field.getAnnotation(DaoColumn.class);
                DaoEmbedding daoEmbedding = field.getAnnotation(DaoEmbedding.class);

                if (daoColumn != null) {
                    field.setAccessible(true);
                    if (daoEmbedding != null) {
                        float[] vector = (float[]) field.get(t);
                        byte[] vectorBytes = convertFloatsToBytes(vector);
                        preparedStatement.setBytes(index++, vectorBytes);
                    } else  {
                        Object value = field.get(t);
                        preparedStatement.setObject(index++, value);
                    }
                }
            }

            ILog.d("DaoSqlite", new String[]{"Executing query: ", preparedStatement.toString()});
            preparedStatement.executeUpdate();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private byte[] convertFloatsToBytes(float[] values) {
        byte[] bytes = new byte[values.length * 4];
        for (int i = 0; i < values.length; i++) {
            int intBits = Float.floatToIntBits(values[i]);
            bytes[i * 4] = (byte) (intBits & 0xFF);
            bytes[i * 4 + 1] = (byte) ((intBits >> 8) & 0xFF);
            bytes[i * 4 + 2] = (byte) ((intBits >> 16) & 0xFF);
            bytes[i * 4 + 3] = (byte) ((intBits >> 24) & 0xFF);
        }
        return bytes;
    }

    public <T> void initVectorSearch(Class<T> clazz, String columnName, int dimension, DistanceMetric distanceMetric) {
        // Implementation for initializing vector search capabilities
        String tableName = clazz.getAnnotation(DaoTable.class).name();

        if (distanceMetric == DistanceMetric.DEFAULT) {
            distanceMetric = DistanceMetric.L2;
        }
        String distance = "distance=" + distanceMetric.name();
        String type = "type=FLOAT32, dimension=" + dimension + "," + distance;
        String query = "SELECT vector_init('" + tableName + "', '" + columnName + "', '" + type + "');";

        try (Connection connection = this.dataSource.getConnection()) {
            ILog.d("DaoSqlite", "Executing vector init query: ", query);
            connection.createStatement().execute(query);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public <T> T[] searchVectors(Class<T> clazz, float[] queryVector, int topK) {
        // Implementation for searching similar vectors (KNN search)
        // This is a placeholder implementation and should be replaced with actual logic
        return null;
    }
}
