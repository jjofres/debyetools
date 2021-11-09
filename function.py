# Inports:
import numpy as np
import itertools as it

def generate_cells_coordinates(size, center, primitive_cell):
    """ generate the cell coordinates for which we are going
    to calculate the neighbor list.

    :param array size: Number of times we are replicating the primitive cell
    :param array center: The position (x,y,z) in space where the ceneter is
    :param array primitive_cell: The primitive cell
    """

    cell_coords = np.array(list((it.product(np.arange(size[0]),
                                            np.arange(size[1]),
                                            np.arange(size[2])))))
    cell_coords_centered = cell_coords + center
    cell_coords_centered = np.dot(cell_coords_centered, primitive_cell)

    return cell_coords_centered

size = np.array([2,2,2])       # Number of times we are replicating the primitive cell
center = np.array([0,0,0])     # The position (x,y,z) in space where the ceneter is
primitive_cell = np.array([[4,0,0],[0,4,0],[0,0,4]]) # The primitive cell
print(generate_cells_coordinates(size, center, primitive_cell
                                 ))
