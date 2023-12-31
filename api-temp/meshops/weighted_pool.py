import torch
from typing import Iterable, SupportsIndex, Union

def _index_out_of_bounds(arr: Union[Iterable, SupportsIndex], row: int, col: int) -> bool:
    """
    Checks if a row and column are out of bounds of a 2D array.
    """
    return row < 0 or col < 0 or row >= len(arr) or col >= len(arr[row])


def weighted_pool(arr: Union[torch.Tensor, SupportsIndex], row: int, col: int, kernel: torch.Tensor) -> list:   
    weighted_sum = 0.0
    kernel_weights_used = 0.0
    
    _kernel_lrow = kernel.shape[0] // 2 # radius along rows (horizontal), also the center row of the kernel
    _kernel_lcol = kernel.shape[1] // 2 # radius along cols (vertical), also the center col of the kernel
    
    #arr_interior = arr[_kernel_lrow:-_kernel_lrow, _kernel_lcol:-_kernel_lcol]
    
    # optimize to only weighted pool the edges, not going through all the interior
    for mov_row in range(-_kernel_lrow, _kernel_lrow + 1):
        for mov_col in range(-_kernel_lcol, _kernel_lcol + 1):
            if _index_out_of_bounds(arr, row + mov_row, col + mov_col):
                continue
            
            weight = kernel[mov_row + _kernel_lrow][mov_col + _kernel_lcol]
            _dot = weight * arr[row + mov_row][col + mov_col]
            weighted_sum += _dot
            kernel_weights_used += weight
            
    return weighted_sum / kernel_weights_used