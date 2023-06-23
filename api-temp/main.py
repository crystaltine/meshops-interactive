import json
from flask import Flask, request
from KEY import API_KEY
import requests
import torch
import numpy as np
from meshops.simulate import simulate2d
import matplotlib.colors as colors
from time import sleep
app = Flask(__name__)

@app.route('/')
def index():
    def fetch(lat, lon):
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'
        sleep(0.2)
        response = requests.get(url)
        data = response.json()
        return data['main']['temp']

    def get_rgb_ndarr(arr: torch.Tensor) -> np.ndarray:
        scaled_vals = -0.693 * arr + 0.693
        hsv_tensor = torch.stack([scaled_vals, torch.ones_like(arr), torch.ones_like(arr)], dim=-1)
        hsv_array = hsv_tensor.cpu().numpy()

        rgb_array = colors.hsv_to_rgb(hsv_array) * 255
        frame = np.round(rgb_array).astype(np.uint8)
        return frame
    coords = json.load(open('api-temp/coords.json', 'r'))
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
            print(f"{temps[i][j]} : fetched #{(23-i) * 36 + j}/864")
        
    for i in range(len(temps)):
        for j in range(len(temps[i])):
            temps[i][j] = round(temps[i][j] - 273.15, 4)
  
    frames = simulate2d(torch.tensor(temps), iteration_count=7, as_list=True)
    color_frames_255 = []
    for frame in frames:
        color_frames_255.append(get_rgb_ndarr(torch.tensor(frame)).tolist())
        
    # write to files
    with open(f'night_data/{city}_temps.json', 'w') as f:
        f.write(f'{json.dumps(frames)}')
        f.close()
    with open(f'night_data/{city}_colors.json', 'w') as f:
        f.write(f'{json.dumps(color_frames_255)}')
        f.close()
        
    return json.dumps({
        'temps': frames,
        'colors': color_frames_255
    })

if __name__ == '__main__':
    app.run(debug=True, port=5050)