package org.thingai.app.rface.callback;

public interface RequestCallback<T> {
    void onSuccess(T responseObject, String response);
    void onFailure(int errorCode, String errorMessage);
}
