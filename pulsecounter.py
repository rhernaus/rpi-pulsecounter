import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

# Sleep time (in seconds)
sleeptime = 10

# Define globals
global meter1_impkwh
global meter2_impkwh
global meter3_impkwh
global meter1_t0
global meter2_t0
global meter3_t0
global meter1_avgkW
global meter2_avgkW
global meter3_avgkW

meter1_impkwh = 100  # ABB C13 110-100
meter2_impkwh = 1000 # ABB C13 110-101
meter3_impkwh = 100  # ABB C13 110-100

meter1_t0 = float(time.time())
meter2_t0 = float(time.time())
meter3_t0 = float(time.time())

meter1_avgkW = float(0)
meter2_avgkW = float(0)
meter3_avgkW = float(0)

# Configure GPIO pins
meter1_gpio = 11 # GPIO17 is pin 11
meter2_gpio = 13 # GPIO27 is pin 13
meter3_gpio = 15 # GPIO22 is pin 15

# Configure mqtt
mqtt_server = '10.128.0.19'
mqtt_port = 1883
mqtt_timeout = 60
mqtt_username = 'sonoff'
mqtt_password = 'sonoff'

# Meter mqtt topicnames
meter1_topicname = 'hass/power/meter1/kw'
meter2_topicname = 'hass/power/meter2/kw'
meter3_topicname = 'hass/power/meter3/kw'

# Set GPIO mode
GPIO.setmode(GPIO.BOARD)
GPIO.setup(meter1_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(meter2_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(meter3_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Connect to mqtt server
client = mqtt.Client()
client.username_pw_set(mqtt_username,mqtt_password)
client.connect(mqtt_server,mqtt_port,mqtt_timeout)
client.loop_start()

def meter1_status(channel):
  global meter1_impkwh
  global meter1_t0
  global meter1_avgkW
  meter1_timetaken = time.time() - meter1_t0
  meter1_avgkW = 3600 / meter1_timetaken / meter1_impkwh
  meter1_t0 = time.time()
  print 'Pulse! Meter1 secondsSinceLastPulse: ', meter1_timetaken

def meter2_status(channel):
  global meter2_impkwh
  global meter2_t0
  global meter2_avgkW
  meter2_timetaken = time.time() - meter2_t0
  meter2_avgkW = 3600 / meter2_timetaken / meter2_impkwh
  meter2_t0 = time.time()
  print 'Pulse! Meter2 secondsSinceLastPulse: ', meter2_timetaken

def meter3_status(channel):
  global meter3_impkwh
  global meter3_t0
  global meter3_avgkW
  meter3_timetaken = time.time() - meter3_t0
  meter3_avgkW = 3600 / meter3_timetaken / meter3_impkwh
  meter3_t0 = time.time()
  print 'Pulse! Meter3 secondsSinceLastPulse: ', meter3_timetaken

GPIO.add_event_detect(meter1_gpio, GPIO.RISING, callback=meter1_status, bouncetime=210)
GPIO.add_event_detect(meter2_gpio, GPIO.RISING, callback=meter2_status, bouncetime=210)
GPIO.add_event_detect(meter3_gpio, GPIO.RISING, callback=meter3_status, bouncetime=210)

while True:
  time.sleep(sleeptime)

  # Lower avgkW if no pulse has been received for a while
  if meter1_avgkW > 3600 / (time.time() - meter1_t0) / meter1_impkwh:
    meter1_avgkW = 3600 / (time.time() - meter1_t0) / meter1_impkwh
  if meter2_avgkW > 3600 / (time.time() - meter2_t0) / meter2_impkwh:
    meter2_avgkW = 3600 / (time.time() - meter2_t0) / meter2_impkwh
  if meter3_avgkW > 3600 / (time.time() - meter3_t0) / meter3_impkwh:
    meter3_avgkW = 3600 / (time.time() - meter3_t0) / meter3_impkwh

  print 'Meter 1:', '{:.3f}'.format(meter1_avgkW),'kW SecondsSinceLastPulse:', int(time.time() - meter1_t0)
  print 'Meter 2:', '{:.3f}'.format(meter2_avgkW),'kW SecondsSinceLastPulse:', int(time.time() - meter2_t0)
  print 'Meter 3:', '{:.3f}'.format(meter3_avgkW),'kW SecondsSinceLastPulse:', int(time.time() - meter3_t0)
  print

  client.publish(meter1_topicname, round(float(meter1_avgkW),3))
  client.publish(meter2_topicname, round(float(meter2_avgkW),3))
  client.publish(meter3_topicname, round(float(meter3_avgkW),3))

GPIO.cleanup() 
