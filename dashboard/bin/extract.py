import ssl
import urllib.request
import json


def get_ha_data(url, access_token):
    ssl_context = ssl._create_unverified_context()

    request = urllib.request.Request(
        url,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    )

    with urllib.request.urlopen(request, context=ssl_context) as response:
        html = response.read()

    return json.loads(html.decode('utf-8'))
