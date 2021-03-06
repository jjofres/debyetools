import itertools as it
import re
import numpy as np
hola
def c_types(atom_types):
    """
    returns all the pair types combinations.

    :param list_of_str atom_types: the types of each atom in the primitive cell in the same order as the basis vectors.
    """
    types_all = re.findall('[A-Z][^A-Z]*', atom_types)
    ptypes=list(set([s for s in types_all]))
    ptypes.sort()
    combs_types = list(it.combinations_with_replacement(ptypes, r=2))
    combs_types = [A[0]+'-'+A[1] for A in combs_types]
    return combs_types, types_all

def generate_cells_coordinates(size, primitive_cell,center):
    """ generate the cell coordinates for which we are going
    to calculate the neighbor list.

    :param array size: Number of times we are replicating the primitive cell
    :param array primitive_cell: The primitive cell
    :param array center: The position in space where the system of reference is
    """

    cell_coords = np.array(list((it.product(np.arange(size[0]),
                                            np.arange(size[1]),
                                            np.arange(size[2])))))
    cell_coords_centered = cell_coords + center
    cell_coords_centered = np.dot(cell_coords_centered, primitive_cell)

    return cell_coords_centered
