import json
from flask import Flask, request
from KEY import API_KEY
import requests
app = Flask(__name__)

def fetch(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['main']['temp']

coords = json.load(open('coords.json'))

@app.route('/')
def index():
    
    city = request.args.get('city')
    coords = coords[city]
    
    # using 24 cells for latitude, 36 cells for longitude
    step_lat = (coords['lat2'] - coords['lat1']) / 23
    step_lon = (coords['lon2'] - coords['lon1']) / 35
    
    temps = [[0] * 36] * 24
    
    lat=coords['lat1']
    lon=coords['lon1']    
    for i in range(23, -1, -1):
        lat += step_lat
        lon = coords['lon1']
        for j in range(36):
            lon += step_lon
            temps[i][j] = fetch(lat, lon)
            
    # Get data from OpenWeatherApi, generate starting mesh
    # Simulate mesh for ~7 days or some amt of time, return list of meshes
    
    
    
    # data ...
    # simulate(data)
    # frames.append(simulated) x 7
    # return:
    # - list of frames to frontend
    # - other data, like temperature
    
    return json.dumps({
        'avg_temperature': temps[11][17],
        'frames': [
            temps,
            # simulated frames below
        ]
    })
