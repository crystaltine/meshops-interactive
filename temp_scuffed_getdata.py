import json, torch
import matplotlib.colors as colors
import numpy as np

def get_rgb_ndarr(arr: torch.Tensor) -> np.ndarray:
    scaled_vals = -0.693 * arr + 0.693
    hsv_tensor = torch.stack([scaled_vals, torch.ones_like(arr), torch.ones_like(arr)], dim=-1)
    hsv_array = hsv_tensor.cpu().numpy()

    rgb_array = colors.hsv_to_rgb(hsv_array) * 255
    frame = np.round(rgb_array).astype(np.uint8)
    return frame

filename = input('linebyline tempdata filename: ')

with open(filename, 'r') as f:
    arr = []
    curr_row = 0 # max 23
    
    for i in range(24):
        arr.append([])    
        for j in range(36):
            arr[i].append(float(f.readline().strip()))
            
    max_temp = max([max(row) for row in arr])
    min_temp = min([min(row) for row in arr])
    
    # scale from 0-1
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr[i][j] = round((arr[i][j] - min_temp) / (max_temp - min_temp), 4)

    with open(f'{filename[:-4]}-scaled-01.json', 'w') as f2:
        f2.write(json.dumps(
            arr
        ))
        f2.close()
        
    # get rgb array
    with open(f'{filename[:-4]}-colorhexes.json', 'w') as f3:
        arr = json.load(open(f'{filename[:-4]}-scaled-01.json', 'r'))
        arr = torch.tensor(arr)
        
        colors_arr = get_rgb_ndarr(arr).tolist()
        f3.write(json.dumps(
            colors_arr
        ))