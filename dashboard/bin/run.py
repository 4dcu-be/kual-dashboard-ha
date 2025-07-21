# bin/python3
# encoding: utf-8

from datetime import datetime
import os
from os.path import join
from extract import get_ha_data
from config import HA_URL, HA_TOKEN


svg_path = '/mnt/base-us/extensions/dashboard/svg/' if os.name != 'nt' else '../svg'


def create_svg(svg_data, svg_template, svg_output):
    with open(svg_template, 'r') as fin:
        template = fin.read()

        for k, v in svg_data.items():
            template = template.replace(k, v)

        with open(svg_output, 'w') as fout:
            fout.write(template)


def fmt_date(date_input):
    d = datetime.strptime(date_input, '%Y-%m-%d')
    return d.strftime('%d/%m/%Y')


def is_today(date_input, fmt="%Y-%m-%d"):
    return date_input == datetime.now().strftime(fmt)


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
        f"{HA_URL}sensor.herentuv"]

    all_data = []

    for ha_url in ha_urls:
        try:
            ha_data = get_ha_data(ha_url, HA_TOKEN)
            all_data.append({
                'sensor': ha_data['attributes']['friendly_name'],
                'readout': f"{ha_data['state']} {ha_data['attributes']['unit_of_measurement']}"
            })
        except Exception as _:
            all_data.append({
                'sensor': "Failed read",
                'readout': "Failed Update"
            })

    print(all_data)

    # Combine into dict
    svg_data = {"LASTUPDATE": "Last Update: " + datetime.now().strftime("%d/%m/%Y - %H:%M:%S"),
                "R1_TEMP": all_data[4]['readout'].replace("°", ""),
                "R1_HUM": all_data[5]['readout'],
                "R2_TEMP": all_data[0]['readout'].replace("°", ""),
                "R2_HUM": all_data[1]['readout'],
                "R3_TEMP": all_data[2]['readout'].replace("°", ""),
                "R3_HUM": all_data[3]['readout'],
                "OUT_TEMP": all_data[7]['readout'].replace("°", ""),
                "OUT_HUM": all_data[6]['readout'],
                "OUT_PRES": all_data[8]['readout'],
                "OUT_UV": all_data[9]['readout'],}

    # Load Data into SVG
    create_svg(svg_data, join(svg_path, "template.svg"), join(svg_path, "tmp.svg"))