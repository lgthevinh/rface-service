package org.thingai.base.ai.vector;

import org.thingai.base.dao.Dao;

import java.util.Map;

public class DaoVectorSqlite extends Dao {
    @Override
    public void initDao(Class[] classes) {

    }

    @Override
    public <T> T[] readAll(Class<T> aClass) {
        return null;
    }

    @Override
    public <T> void insertOrUpdate(T t) {

    }

    @Override
    public <T> void insertOrUpdate(Class<T> aClass, T t) {

    }

    @Override
    public <T> void insertBatch(T[] ts) {

    }

    @Override
    public <T, K> void delete(Class<T> aClass, K k) {

    }

    @Override
    public <T> void delete(T t) {

    }

    @Override
    public <T> void deleteByColumn(Class<T> aClass, String s, String s1) {

    }

    @Override
    public <T> void deleteAll(Class<T> aClass) {

    }

    @Override
    public <T> T[] query(Class<T> aClass, String s, String s1) {
        return null;
    }

    @Override
    public <T> T[] query(Class<T> aClass, String[] strings, String[] strings1) {
        return null;
    }

    @Override
    public <T> T[] query(Class<T> aClass, String s) {
        return null;
    }

    @Override
    public Map<String, Object>[] queryRaw(String s) {
        return new Map[0];
    }
}
