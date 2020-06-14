# Pull base image
FROM registry.dev.virtunet.io/virtunet/rpi-python-serial-wiringpi/master:latest

# Install dependencies
RUN pip install wheel
RUN pip install paho-mqtt rpi.gpio

# Define default command
COPY . /app
WORKDIR /app
CMD python -u ./pulsecounter.py
