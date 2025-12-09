package org.thingai.base.ai.vector.define;

public enum DistanceMetric {
    L1,
    COSINE,
    DOT,
    L2, // This as default for sqlite-vector
    SQUARED_L2,

    DEFAULT
}
