plugins {
    id("java")
}

group = "org.thingai.base.ai"
version = ""

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.10.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")

    implementation("org.xerial:sqlite-jdbc:3.43.2.0")
    implementation("com.zaxxer:HikariCP:5.1.0")

    implementation(files("../libs/applicationbase.jar"))
    implementation(files("../libs/desktopplatform.jar"))
}

tasks.test {
    useJUnitPlatform()
}