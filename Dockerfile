# Use OpenJDK as the base image
FROM openjdk:17-jdk-slim-

# Set the working directory
WORKDIR /app

# Copy the jar file into the container
COPY target/*.jar app.jar

# Expose the application port
EXPOSE 8080

# Set the entrypoint to run the jar
ENTRYPOINT ["java", "-jar", "app.jar"]