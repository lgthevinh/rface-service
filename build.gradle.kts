import org.gradle.kotlin.dsl.implementation

plugins {
    id("java")
}

group = "org.thingai.app"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.10.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")

    implementation("org.xerial:sqlite-jdbc:3.43.2.0")
    implementation("com.zaxxer:HikariCP:5.1.0")
    implementation("org.slf4j:slf4j-api:2.0.9")
    implementation("com.google.code.gson:gson:2.13.2")

    implementation(files("libs/applicationbase.jar"))
    implementation(files("libs/desktopplatform.jar"))
    implementation(files("aibase/build/libs/aibase.jar"))


}

tasks.test {
    useJUnitPlatform()
}