# rpi-pulsecounter

## Introduction

I use this to monitor GPIO pins on a Raspberry Pi for pulses from my power meters and publish the power usage to mqtt.

```text
Meter              Pulses per kWh
-----------------------------------
ABB C13 110-100    100
ABB C13 110-101    1000
```

Raspberry Pi GPIO header pins: <https://www.raspberrypi-spy.co.uk/2012/06/simple-guide-to-the-rpi-gpio-header-and-pins/>

## Usage

```text
Configuration is passed as environment variables.

mqtt_host  hostname or ip address of mqtt
mqtt_port  tcp port of mqtt
mqtt_user  username used to authenticate to mqtt
mqtt_pass  password used to authenticate to mqtt
config     json with configuration
[
    {
        pin        pin number on Raspberry Pi board
        impkwh     number of impulses the power meter sends per kWh of usage
        topic      mqtt topic to publish the power to in kW
    }
]
```

A docker image is published on Docker Hub. You can start it on a Raspberry Pi with the example script below.

```bash
#!/bin/bash
IMAGE=rhernaus/rpi-pulsecounter
docker pull $IMAGE
docker run \
  --name rpi-pulsecounter \
  --pull always \
  --device /dev/gpiomem:/dev/gpiomem \
  --privileged \
  --restart=unless-stopped \
  -e mqtt_host=x.x.x.x
  -e mqtt_port=1883
  -e mqtt_user=xxxxxx
  -e mqtt_pass=xxxxxx
  -e config='[{"pin":11,"impkwh":100,"topic":"hass/power/meter1/kw"},{"pin":15,"impkwh":1000,"topic":"hass/power/meter2/kw"},{"pin":13,"impkwh":100,"topic":"hass/power/meter3/kw"}]'
  -d $IMAGE
```

## Example output

```text
pi@raspberrypi:~ $ docker logs -f rpi-pulsecounter
2022-02-19 13:35:31 INFO     Pin: 11 | Power: 1.744 kW | Last pulse 9 seconds ago
2022-02-19 13:35:31 INFO     Pin: 15 | Power: 0.935 kW | Last pulse 0 seconds ago
2022-02-19 13:35:31 INFO     Pin: 13 | Power: 0.000 kW | Last pulse 30 seconds ago
2022-02-19 13:35:35 INFO     Pin: 15 | Power: 0.837 kW | Pulse!
2022-02-19 13:35:39 INFO     Pin: 15 | Power: 0.900 kW | Pulse!
2022-02-19 13:35:41 INFO     Pin: 11 | Power: 1.744 kW | Last pulse 19 seconds ago
2022-02-19 13:35:41 INFO     Pin: 15 | Power: 0.900 kW | Last pulse 1 seconds ago
2022-02-19 13:35:41 INFO     Pin: 13 | Power: 0.000 kW | Last pulse 40 seconds ago
2022-02-19 13:35:43 INFO     Pin: 15 | Power: 0.859 kW | Pulse!
2022-02-19 13:35:47 INFO     Pin: 15 | Power: 0.866 kW | Pulse!
2022-02-19 13:35:51 INFO     Pin: 11 | Power: 1.222 kW | Last pulse 29 seconds ago
2022-02-19 13:35:51 INFO     Pin: 15 | Power: 0.866 kW | Last pulse 3 seconds ago
2022-02-19 13:35:51 INFO     Pin: 13 | Power: 0.000 kW | Last pulse 50 seconds ago
2022-02-19 13:35:51 INFO     Pin: 15 | Power: 0.918 kW | Pulse!
2022-02-19 13:35:52 INFO     Pin: 11 | Power: 1.178 kW | Pulse!
2022-02-19 13:35:55 INFO     Pin: 15 | Power: 0.854 kW | Pulse!
2022-02-19 13:35:59 INFO     Pin: 15 | Power: 0.928 kW | Pulse!
2022-02-19 13:36:01 INFO     Pin: 11 | Power: 1.178 kW | Last pulse 8 seconds ago
2022-02-19 13:36:01 INFO     Pin: 15 | Power: 0.928 kW | Last pulse 1 seconds ago
2022-02-19 13:36:01 INFO     Pin: 13 | Power: 0.000 kW | Last pulse 60 seconds ago
2022-02-19 13:36:03 INFO     Pin: 15 | Power: 0.854 kW | Pulse!
```
