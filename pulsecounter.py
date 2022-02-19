import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
import os
import json
import logging

def on_pulse(pin):
  global config
  gpio = [gpio for gpio in config if gpio["pin"] == pin][0]
  gpio["kw"] = 3600 / (time.time() - gpio["t0"]) / gpio["impkwh"]
  gpio["t0"] = time.time()
  logging.info(f'Pin: {gpio["pin"]} | Power: {format(gpio["kw"], ".3f")} kW | Pulse!')

logging.basicConfig(
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.INFO,
  datefmt='%Y-%m-%d %H:%M:%S')

# Sleep time (in seconds)
sleeptime = 10

global config
config = json.loads(os.environ.get('config'))

# Set GPIO mode
GPIO.setmode(GPIO.BOARD)

for gpio in config:
  gpio["t0"] = float(time.time())
  gpio["kw"] = float(0)
  GPIO.setup(int(gpio["pin"]), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.add_event_detect(int(gpio["pin"]), GPIO.RISING, callback=on_pulse, bouncetime=210)

# Connect to mqtt server
client = mqtt.Client()
client.username_pw_set(  
  os.environ.get('mqtt_user'),
  os.environ.get('mqtt_pass')
)
client.reconnect_delay_set(
  min_delay=1,
  max_delay=60
)
client.connect(
  host=os.environ.get('mqtt_host'),
  port=int(os.environ.get('mqtt_port')),
  keepalive=60
)
client.loop_start()

while True:
  time.sleep(sleeptime)

  # Lower avgkW if no pulse has been received for a while
  for gpio in config:
    if gpio["kw"] > 3600 / (time.time() - gpio["t0"]) / gpio["impkwh"]:
      gpio["kw"] = 3600 / (time.time() - gpio["t0"]) / gpio["impkwh"]
    logging.info(f'Pin: {gpio["pin"]} | Power: {format(gpio["kw"], ".3f")} kW | Last pulse {int(time.time() - gpio["t0"])} seconds ago')
    client.publish(gpio["topic"], round(float(gpio["kw"]),3))