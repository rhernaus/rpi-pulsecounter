FROM rhernaus/rpi-python-serial-wiringpi:1642943603

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD python -u ./pulsecounter.py