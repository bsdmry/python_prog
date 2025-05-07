#!/usr/bin/env python3
import math
#from urllib.request import urlopen
import json
from pprint import pprint
import time
import requests
def haversine_distance(lat1, lon1, lat2, lon2):
    # Радиус Земли в километрах
    R = 6371.0

    # Преобразование градусов в радианы
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Формула Хаверсина
    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def is_within_radius(lat_ref, lon_ref, lat_check, lon_check,radius_km_ref=10):
    distance = haversine_distance(lat_ref, lon_ref, lat_check, lon_check)
    return distance <= radius_km_ref

vilnius_lat =  54.68722 
vilnius_lon = 25.28000

def record_check(r):
	if r['geometry']['type'] == 'Point':
		return is_within_radius(vilnius_lat, vilnius_lon, r['geometry']['coordinates'][1], r['geometry']['coordinates'][0], 20)
	return False

def record_check1(r):
	return r['properties']['name'] == 'S3951052 - END'

urls = ['https://radiosondy.info/mail_reports/LatestFlightsA.json',
	'https://radiosondy.info/mail_reports/LatestFlightsB.json',
	'https://radiosondy.info/mail_reports/LatestFlightsC.json',
	'https://radiosondy.info/mail_reports/LatestFlightsD.json'
]

headers = {
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0",
"Accept": "application/json, text/javascript, */*; q=0.01",
"Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
"Accept-Encoding": "gzip, deflate, br, zstd",
"X-Requested-With": "XMLHttpRequest",
"Connection": "keep-alive",
"Referer": "https://radiosondy.info/maps/web_map.php?latest_flights=1",
"Sec-Fetch-Dest": "empty",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Site": "same-origin"
}

session = requests.session()
session.get('https://radiosondy.info/')
time.sleep(1)
session.get("https://radiosondy.info/maps/web_map.php?latest_flights=1")
time.sleep(1)
for url in urls: 
	reply = session.get(url, headers=headers)
	if reply.status_code == 200:
		data = reply.json()
		ext = list(filter(record_check, data['features']))
		if len(ext) > 0:
			pprint(ext)
	else:
		print(reply.status_code)
		print(reply.text)
