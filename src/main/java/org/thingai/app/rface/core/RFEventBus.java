package org.thingai.app.rface.core;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class RFEventBus {
    private final Map<Class<?>, Object[]> subscribers;
    private final ExecutorService executor;

    public RFEventBus() {
        this.subscribers = new ConcurrentHashMap<>();
        this.executor = Executors.newFixedThreadPool(2);
    }

    public <T> void register(Class<T> eventType, RFEventBus.EventListener<T> listener) {
        this.subscribers.computeIfAbsent(eventType, k -> new Object[0]);
        Object[] currentListeners = this.subscribers.get(eventType);
        Object[] newListeners = new Object[currentListeners.length + 1];
        System.arraycopy(currentListeners, 0, newListeners, 0, currentListeners.length);
        newListeners[currentListeners.length] = listener;
        this.subscribers.put(eventType, newListeners);
    }

    public <T> void post(T event) {
        Object[] listeners = this.subscribers.get(event.getClass());
        if (listeners != null) {
            for (Object listener : listeners) {
                RFEventBus.EventListener<T> eventListener = (RFEventBus.EventListener<T>) listener;
                executor.submit(() -> eventListener.onEvent(event));
            }
        }
    }

    public interface EventListener<T> {
        void onEvent(T event);
    }
}
