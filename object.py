import numpy as np
import itertools as it

class GenerateCellCoordinates:
    """
    Instantiate cells coordinates replication for pair analysis.

    :param array center: The position in space where the system of reference is
    """

    def __init__(self, center):
        self.center = center

    def generate_cells_coordinates(self, size, primitive_cell):
        """ generate the cell coordinates for which we are going
        to calculate the neighbor list.

        :param array size: Number of times we are replicating the primitive cell
        :param array primitive_cell: The primitive cell
        """

        cell_coords = np.array(list((it.product(np.arange(size[0]),
                                                np.arange(size[1]),
                                                np.arange(size[2])))))
        cell_coords_centered = cell_coords + self.center
        cell_coords_centered = np.dot(cell_coords_centered, primitive_cell)

        return cell_coords_centered

# Instantiation of GenerateCellCoordinates object
center = np.array([0,0,0])
coords_generation = GenerateCellCoordinates(center)

# Call generation method
size = np.array([2,2,2])
primitive_cell = np.array([[4,0,0],[0,4,0],[0,0,4]])
print(coords_generation.generate_cells_coordinates(size, primitive_cell))
