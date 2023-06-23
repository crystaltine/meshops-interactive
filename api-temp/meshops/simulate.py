import torch
from meshops.media import NDSquareMesh
from meshops.utils.GIFmake import draw_gif
from meshops.utils.log import IterativeFile
import numpy as np
from PIL import Image
from meshops.utils.debug_progress_bar import _get_progress_string
import matplotlib.colors as colors

def get_rgb_ndarr(arr: torch.Tensor) -> np.ndarray:
        scaled_vals = -0.693 * arr + 0.693
        hsv_tensor = torch.stack([scaled_vals, torch.ones_like(arr), torch.ones_like(arr)], dim=-1)
        hsv_array = hsv_tensor.cpu().numpy()

        rgb_array = colors.hsv_to_rgb(hsv_array) * 255
        frame = np.round(rgb_array).astype(np.uint8)
        return frame

def simulate2d(
    tensor: torch.Tensor | np.ndarray = None,
    image_path: str = None,
    iteration_count: int = 50,
    conduction_kernel: torch.Tensor | np.ndarray | list = [
        [0.2, 0.8, 0.2], 
        [0.8, 1, 0.8], 
        [0.2, 0.8, 0.2]
    ],
    mesh_velocity_angles: float | list[float] = None,
    as_list: bool = False
    ) -> torch.Tensor | list[list[list[float]]]:
    """
    Simulate a 2D mesh of heat values. Takes input from a starting tensor or an image file (which will be converted
    to a heatmap) and runs the simulation for the specified number of iterations. Returns a tensor (1 dimension
    higher than the original) of all frames OR a list of lists representing each frame. Values should all be between 0 and 1."""
    
    if tensor is not None and image_path:
        raise ValueError("Cannot specify both tensor and image_path")
    if tensor is None and not image_path:
        raise ValueError("Must specify either tensor or image_path")

    heatmap = NDSquareMesh(tensor) if tensor is not None else NDSquareMesh()._import_from_image(image_path)
    frames = []
    
    def __add(frames: list, new: torch.Tensor):
        if as_list:
            frames.append(new.tolist())
        else:
            frames.append(new)
            
    
    time_counter = 0
    if type(mesh_velocity_angles) == float: # one angle specified, constant
        for i in range(iteration_count):
            time_counter += 1
            __add(frames, heatmap.get_iterable())
            heatmap.run_timestep(kernel=conduction_kernel, velocity_angle=mesh_velocity_angles)
            print(f"{_get_progress_string(time_counter/iteration_count)} Iteration: {time_counter}/{iteration_count}", end='\r')
    elif type(mesh_velocity_angles) == list:
        if len(mesh_velocity_angles) != iteration_count:
            raise ValueError("Length of mesh_velocity_angles must be equal to iteration_count")
        for i in range(iteration_count):
            time_counter += 1
            __add(frames, heatmap.get_iterable())
            heatmap.run_timestep(kernel=conduction_kernel, velocity_angle=mesh_velocity_angles[i])
            print(f"{_get_progress_string(time_counter/iteration_count)} Iteration: {time_counter}/{iteration_count}", end='\r')
    else:
        for i in range(iteration_count):
            time_counter += 1
            __add(frames, heatmap.get_iterable())
            heatmap.run_timestep(kernel=conduction_kernel)
            print(f"{_get_progress_string(time_counter/iteration_count)} Iteration: {time_counter}/{iteration_count}", end='\r')

    print("\n")
    if not as_list:
        return torch.stack(frames)
    return frames

def to_images(tensor: torch.Tensor) -> list:
    """
    Converts a tensor of shape (frames, height, width) to a list of PIL Images"""
    frames = []
    for i in range(tensor.shape[0]):
        frames.append(Image.fromarray(get_rgb_ndarr(tensor[i]), 'RGB'))
    return frames
    
        