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
2022-02-19 13:16:53 INFO     Pulse! Pin: 15 Power: 1.167 kW
2022-02-19 13:16:57 INFO     Pulse! Pin: 15 Power: 0.84 kW
2022-02-19 13:17:00 INFO     Pin: 11 Power: 0.0 kW SecondsSinceLastPulse: 10
2022-02-19 13:17:00 INFO     Pin: 15 Power: 0.84 kW SecondsSinceLastPulse: 2
2022-02-19 13:17:00 INFO     Pin: 13 Power: 0.0 kW SecondsSinceLastPulse: 10
2022-02-19 13:17:01 INFO     Pulse! Pin: 15 Power: 0.872 kW
2022-02-19 13:17:06 INFO     Pulse! Pin: 15 Power: 0.872 kW
2022-02-19 13:17:10 INFO     Pulse! Pin: 15 Power: 0.826 kW
2022-02-19 13:17:10 INFO     Pin: 11 Power: 0.0 kW SecondsSinceLastPulse: 20
2022-02-19 13:17:10 INFO     Pin: 15 Power: 0.826 kW SecondsSinceLastPulse: 0
2022-02-19 13:17:10 INFO     Pin: 13 Power: 0.0 kW SecondsSinceLastPulse: 20
2022-02-19 13:17:14 INFO     Pulse! Pin: 15 Power: 0.911 kW
2022-02-19 13:17:18 INFO     Pulse! Pin: 15 Power: 0.831 kW
2022-02-19 13:17:20 INFO     Pin: 11 Power: 0.0 kW SecondsSinceLastPulse: 30
2022-02-19 13:17:20 INFO     Pin: 15 Power: 0.831 kW SecondsSinceLastPulse: 1
2022-02-19 13:17:20 INFO     Pin: 13 Power: 0.0 kW SecondsSinceLastPulse: 30
2022-02-19 13:17:22 INFO     Pulse! Pin: 15 Power: 0.901 kW
2022-02-19 13:17:26 INFO     Pulse! Pin: 15 Power: 0.831 kW
2022-02-19 13:17:27 INFO     Pulse! Pin: 11 Power: 0.976 kW
2022-02-19 13:17:30 INFO     Pin: 11 Power: 0.976 kW SecondsSinceLastPulse: 3
2022-02-19 13:17:30 INFO     Pin: 15 Power: 0.831 kW SecondsSinceLastPulse: 3
2022-02-19 13:17:30 INFO     Pin: 13 Power: 0.0 kW SecondsSinceLastPulse: 40
2022-02-19 13:17:31 INFO     Pulse! Pin: 15 Power: 0.832 kW
2022-02-19 13:17:35 INFO     Pulse! Pin: 15 Power: 0.893 kW
2022-02-19 13:17:39 INFO     Pulse! Pin: 15 Power: 0.829 kW
```
