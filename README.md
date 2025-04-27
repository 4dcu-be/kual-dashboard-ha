# KUAL Dashboard - Home Assistant

This is a KUAL extension that turns a Kindle Paperwhite 3 into a dashboard which reads sensor values from Home 
Assistant's API.
 
## Requirements

  * A Jailbroken Kindle Paperwhite 3
  * KUAL installed with Python 3
  * If you are looking for instructions to do this, check [here](http://blog.4dcu.be/diy/2020/09/27/PythonKindleDashboard_1.html) for details and links to additional resources.
  
## Installation

Copy the folder `dashboard` from the repository to the `/extensions` folder on the Kindle (if that folder is not there
KUAL isn't installed properly).

Copy the file `/extensions/dashboard/bin/config.example.py` to `/extensions/dashboard/bin/config.py` and update the
URL and access token in the file with your Home Assistant instance. The URL should be the full URL to your Home 
Assistant API states endpoint (including the slash at the end) and the access token should be a long-lived access token.

```python
HA_URL="URL to your Home Assistant instance" # e.g. "https://your-home-assistant.duckdns.org:8123/api/states/" should end with a slash
HA_TOKEN="your long-lived access token"
```

Given that no two Home Assistant
instances are the same, you will need to update the names of the sensors in the list `ha_urls` to match your own in 
`/extensions/dashboard/bin/run.py`. You'll probably want to update the svg template 
(`/extensions/dashboard/svg/svg_template.svg`) as well to match your setup.
```python
    ha_urls = [
        f"{HA_URL}sensor.sensor_bedroom_temperature",
        f"{HA_URL}sensor.sensor_bedroom_humidity",
        f"{HA_URL}sensor.sensor_nursery_temperature",
        f"{HA_URL}sensor.sensor_nursery_humidity",
        f"{HA_URL}sensor.living_room_sensor_bme680_temperature",
        f"{HA_URL}sensor.living_room_sensor_bme680_humidity",
        f"{HA_URL}sensor.herenthumidity",
        f"{HA_URL}sensor.herenttemperature",
        f"{HA_URL}sensor.herentpressure",
        f"{HA_URL}sensor.herentuv"]
```


## Starting the Dashboard

First type `~ds` in the searchbar and hit enter. This will disable the Kindle's own deep sleep and screensaver, this is
required as deep sleep disables the wake-up timer, which will stop the dashboard from refreshing. To re-enable deep sleep, you will need to restart the Kindle by holding the power button for
15-20 seconds and pushing restart in the menu.

Next, open KUAL and start "Home Assistant", wait 30 seconds for the dashboard to appear and done!

## Acknowledgements

rsvg-convert included in this repo is derived from [https://github.com/x-magic/kindle-weather-stand-alone](https://github.com/x-magic/kindle-weather-stand-alone) as well
as the configuration files to integrate the script with KUAL.