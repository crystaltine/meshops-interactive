import torch
from media import NDSquareMesh
from utils.log import Log
from utils.log import IterativeFile
from utils.GIFmake import draw_gif
from utils.timing import Timer
import numpy as np
from PIL import Image
from utils.debug_progress_bar import _get_progress_string
import matplotlib.colors as colors


# RUN THIS FILE AND CHEC THE GIFS FOLDER!

NUM_ITERATIONS = int(input("Iteration count (recommended < 500): "))
FPS = int(input("FPS: "))
FILE = input("FIle? (<filepath>/'no'): ")
LENGTH = 50
WIDTH = 50

gifFS = IterativeFile("meshops-gifs/2d/", "2D", ".gif")
gif_path = gifFS.getFileName()

def get_rgb_ndarr(arr: torch.Tensor) -> np.ndarray:
    scaled_vals = -0.693 * arr + 0.693
    hsv_tensor = torch.stack([scaled_vals, torch.ones_like(arr), torch.ones_like(arr)], dim=-1)
    hsv_array = hsv_tensor.cpu().numpy()

    rgb_array = colors.hsv_to_rgb(hsv_array) * 255
    frame = np.round(rgb_array).astype(np.uint8)
    return frame

time_counter = 0
new_heatmap = NDSquareMesh((LENGTH, WIDTH), 0)
if FILE == 'no':
    new_heatmap.set_region((LENGTH//2, WIDTH//2), LENGTH//3, 1)
else:
    new_heatmap._import_from_image(FILE)

frames = [Image.fromarray(get_rgb_ndarr(new_heatmap.get_iterable()), 'RGB')]
for i in range(NUM_ITERATIONS):

    time_counter += 1
    new_heatmap.run_timestep()
    frames.append(Image.fromarray(get_rgb_ndarr(new_heatmap.get_iterable()), 'RGB'))
    print(f"{_get_progress_string(time_counter/NUM_ITERATIONS)} Iteration: {time_counter}/{NUM_ITERATIONS}", end='\r')

draw_gif(frames, gif_path, FPS)