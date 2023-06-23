import torch, math
from typing import Union

"""
Hashmap of which direction to steal from and which direction to give to.
"""
RANGES = {
    (0, 90): ((-1, 0), (0, 1)),
    (90, 180): ((-1, 0), (0, -1)),
    (180, 270): ((1, 0), (0, -1)),
    (270, 360): ((1, 0), (0, 1)),
}

AXES = {
    0: (0, 1),
    90: (-1, 0),
    180: (0, -1),
    270: (1, 0)
}


def apply_padding(tensor: torch.Tensor, pad: Union[str, float, int] = "copy") -> torch.Tensor:
    if pad == 'copy':
        
        padded = torch.nn.functional.pad(tensor, (1, 1, 1, 1), mode='constant', value=0)
        for i in range(padded.shape[0]):
            padded[i][0] = padded[i][1]
            padded[i][-1] = padded[i][-2]
            
        for j in range(padded.shape[1]):
            padded[0][j] = padded[1][j]
            padded[-1][j] = padded[-2][j]
            
        return padded
        

    if (type(pad) == int or type(pad) == float) and 0 <= pad <= 1:
        # constant value
        return torch.nn.functional.pad(tensor, (1, 1, 1, 1), mode='constant', value=pad)

    else:
        raise ValueError("Invalid pad. It should be either 'copy' or a float value between 0 and 1.")



def apply_velocity(
    tensor: torch.Tensor, 
    degrees: float, 
    device: torch.device = torch.device('cpu'), 
    padding: Union[str, float] = 'copy'
    ) -> torch.Tensor:
    """
    Applies a global velocity to all cells in a mesh (think of the values "moving" in a certain direction).
    
    If `padding` == 'copy', then the padding on the outside of the tensor will be filled with the values of the border.
    Another option is to set `padding` to a float value, which will fill the padding completely.
    """

    #tensor = tensor.to(device)

    abs_component_horiz = abs(math.cos(math.radians(degrees))) # changes along a row
    abs_component_vert = abs(math.sin(math.radians(degrees))) # changes along a column

    ratio_horiz = round(abs_component_horiz / (abs_component_horiz + abs_component_vert), 7)
    ratio_vert = round(abs_component_vert / (abs_component_horiz + abs_component_vert), 7)
    
    steal_direction: ... # info about the cells to check when pulling heat from the direction of velocity
    if degrees > 0 and degrees < 90: steal_direction = ((0, -1), (1, 0))
    elif degrees > 90 and degrees < 180: steal_direction = ((0, 1), (1, 0))
    elif degrees > 180 and degrees < 270: steal_direction = ((0, 1), (1, 0))
    elif degrees > 270 and degrees < 360: steal_direction = ((0, 1), (1, 0))

    elif degrees == 0: steal_direction = ((0, -1), (0, 0))
    elif degrees == 90: steal_direction = ((0, 0), (1, 0))
    elif degrees == 180: steal_direction = ((0, 1), (0, 0))
    elif degrees == 270: steal_direction = ((0, 0), (-1, 0))
        
    if not (padding == "copy" or padding < 0 or padding > 1):
        raise ValueError("Padding must be either 'copy' or a value between 0 and 1 inclusive.")

    adjusted = apply_padding(tensor, padding)
    padded = adjusted.clone()
    # Example corner:
    #
    #   Z       Y    Y2     
    #       _____________
    #       |>CURR|
    #   X   |  A  |  B
    #       |------------
    #   X2  |  C  |  D
    #       |     |
    
    for i in range(tensor.shape[0]):
        for j in range(tensor.shape[1]):            
            _steal_x = ratio_horiz * (
                padded[i+steal_direction[0][0]+1, j+steal_direction[0][1]+1] - # coordinates of neighbor 1
                tensor[i, j] # value of A originally
            )

            _steal_y = ratio_vert * (
                padded[i+steal_direction[1][0]+1, j+steal_direction[1][1]+1] - # coordinates of neighbor 2
                tensor[i,j] # value of A originally
            )
            adjusted[i+1, j+1] = tensor[i, j] + _steal_x + _steal_y
    
    return adjusted[1:-1, 1:-1]


