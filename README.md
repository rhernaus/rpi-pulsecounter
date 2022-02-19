# rpi-pulsecounter

## Introduction

I use this to monitor GPIO pins on a Raspberry Pi for pulses from my power meters and publish the power usage to mqtt.

```text
Meter              Pulses per kWh
-----------------------------------
ABB C13 110-100    100
ABB C13 110-101    1000
```

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

A docker image with the script is published on Docker Hub. You can start it on a Raspberry Pi with the example script below.

```bash
#!/bin/bash
IMAGE=rhernaus/rpi-pulsecounter:1645260297
docker pull $IMAGE
docker run \
  --name rpi-pulsecounter \
  --device /dev/gpiomem:/dev/gpiomem \
  --privileged --restart=unless-stopped \
  -e mqtt_host=x.x.x.x
  -e mqtt_port=1883
  -e mqtt_user=xxxxxx
  -e mqtt_pass=xxxxxx
  -e config='[{"pin":11,"impkwh":100,"topic":"hass/power/meter1/kw"},{"pin":15,"impkwh":1000,"topic":"hass/power/meter2/kw"},{"pin":13,"impkwh":100,"topic":"hass/power/meter3/kw"}]'
  -d $IMAGE
```
