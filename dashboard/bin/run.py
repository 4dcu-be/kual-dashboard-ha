
from datetime import datetime
import os
import json
from os.path import join
from extract import get_ha_data
from config import HA_URL, HA_TOKEN

svg_path = '/mnt/base-us/extensions/dashboard/svg/' if os.name != 'nt' else '../svg'
cache_file = join(svg_path, 'sensor_cache.json')


def create_svg(svg_data, svg_template, svg_output):
    with open(svg_template, 'r') as fin:
        template = fin.read()
        for k, v in svg_data.items():
            template = template.replace(k, v)
        with open(svg_output, 'w') as fout:
            fout.write(template)


def round_if_float(s):
    try:
        return f"{round(float(s), 1):.1f}"
    except ValueError:
        return s


def load_cache():
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return {}


def save_cache(data):
    with open(cache_file, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    ha_urls = [
        f"{HA_URL}sensor.sensor_bedroom_temperature",
        f"{HA_URL}sensor.sensor_bedroom_humidity",
        f"{HA_URL}sensor.sensor_nursery_temperature",
        f"{HA_URL}sensor.sensor_nursery_humidity",
        f"{HA_URL}sensor.upgraded_sensor_bme680_temperature",
        f"{HA_URL}sensor.upgraded_sensor_bme680_humidity",
        f"{HA_URL}sensor.herenthumidity",
        f"{HA_URL}sensor.herenttemperature",
        f"{HA_URL}sensor.herentpressure",
        f"{HA_URL}sensor.herentuv"
    ]

    cache = load_cache()
    all_data = []
    had_failure = False

    for ha_url in ha_urls:
        sensor_id = ha_url.split("sensor.")[-1]
        try:
            ha_data = get_ha_data(ha_url, HA_TOKEN)
            sensor_name = ha_data['attributes']['friendly_name']
            readout = f"{round_if_float(ha_data['state'])} {ha_data['attributes']['unit_of_measurement']}"
            all_data.append({'sensor': sensor_name, 'readout': readout})
            cache[sensor_id] = {'sensor': sensor_name, 'readout': readout}
        except Exception as e:
            print(f"Failed to update {ha_url}: {e}")
            had_failure = True
            cached = cache.get(sensor_id, {'sensor': 'Failed read', 'readout': 'Failed Update'})
            all_data.append(cached)

    save_cache(cache)

    svg_data = {
        "LASTUPDATE": ("Last Update (with errors): " if had_failure else "Last Update: ") +
                      datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),
        "R1_TEMP": all_data[4]['readout'].replace("°", ""),
        "R1_HUM": all_data[5]['readout'],
        "R2_TEMP": all_data[0]['readout'].replace("°", ""),
        "R2_HUM": all_data[1]['readout'],
        "R3_TEMP": all_data[2]['readout'].replace("°", ""),
        "R3_HUM": all_data[3]['readout'],
        "OUT_TEMP": all_data[7]['readout'].replace("°", ""),
        "OUT_HUM": all_data[6]['readout'],
        "OUT_PRES": all_data[8]['readout'],
        "OUT_UV": all_data[9]['readout'],
    }

    create_svg(svg_data, join(svg_path, "template.svg"), join(svg_path, "tmp.svg"))