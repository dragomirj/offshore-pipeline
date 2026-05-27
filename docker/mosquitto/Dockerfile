FROM eclipse-mosquitto:2.0

# Copy config
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# Create internal directories
RUN mkdir -p /mosquitto/data /mosquitto/log

# Expose port (will bind to localhost in docker-compose)
EXPOSE 1883

# Run Mosquitto in foreground
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf", "-v"]