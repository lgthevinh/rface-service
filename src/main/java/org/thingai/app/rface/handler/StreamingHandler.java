package org.thingai.app.rface.handler;

import org.thingai.base.eda.EventBus;

public class StreamingHandler implements Runnable {
    private final String TAG = "StreamingHandler";
    private EventBus eventBus;

    public StreamingHandler() {

    }

    @Override
    public void run() {
        // Streaming handling logic goes here
    }

    public void setEventBus(EventBus eventBus) {
        this.eventBus = eventBus;
    }
}
