# Pull base image
FROM rhernaus/rpi-python-serial-wiringpi:1642943603

# Install dependencies
RUN pip install -r requirements.txt

# Define default command
COPY . /app
WORKDIR /app
CMD python -u ./pulsecounter.py
