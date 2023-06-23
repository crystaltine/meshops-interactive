# get data from scaled linebyline jsons
from meshops.simulate import simulate2d, get_rgb_ndarr
import json, torch

listfile = input('scaled json listfile: ')
data = json.load(open(listfile, 'r'))

# simulate data for 7 days and get as lists
frames = simulate2d(torch.tensor(data), iteration_count=7, as_list=True, mesh_velocity_angles=[140, 190, 270, 200, 150, 70, 110])

with open(f'{listfile[:-5]}-temps_frameslist.json', 'w') as f:
    f.write(json.dumps(frames))
    f.close()

with open(f'{listfile[:-5]}-colors_frameslist.json', 'w') as f:
    color_frames = []
    for frame in frames:
        color_frames.append(get_rgb_ndarr(torch.tensor(frame)).tolist())
    f.write(json.dumps(color_frames))
    f.close()
        