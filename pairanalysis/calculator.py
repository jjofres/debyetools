import numpy as np
import itertools as it

class NeighborList:
    """
    Calculate neighbor list for pair analysis.

    """

    def __init__(self):
        pass

    def generate_cells_coordinates(self, size, primitive_cell,center):
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

    def neighbor_list(self,size, cutoff, center, basis_vectors, primitive_cell):
        """ calculate a list i,j,dij where i is the index of an atom j is the
        index of its neighbor and dij is the distance between atoms i and j.

        :param array size: Number of times we are replicating the primitive cel
        :param int cutoff: Number of times we are replicating the supercell
        up to which we are considering for the calculation (uses pbc)
        :param array center: The position in space where the system of reference is
        :param array basis_vectors: atoms position within a single primitive cell
        :param array primitive_cell: the primitive cell"""

        size_g = size + 2*cutoff  #change cutoff for some other word and add a cutoff distance.
                                  # new_co= int(min(cutoff,....))

        cell_coords_centered = self.generate_cells_coordinates(size, primitive_cell, center)
        cell_coords_centered_g = self.generate_cells_coordinates(size_g, primitive_cell, center-cutoff)

        XCs = []
        Is = []
        Js = []

        ixs = np.arange(len(basis_vectors))
        jxs = np.arange(len(basis_vectors))

        for icell, cell_coords_i in enumerate(cell_coords_centered):
            ix_neighbor = np.where(np.all(abs(cell_coords_centered_g-cell_coords_i)<=cutoff, axis=1))[0]
            Xs = np.array([cell_coords_i,]*len(basis_vectors))+basis_vectors

            for cell_coords_i_g in cell_coords_centered_g[ix_neighbor]:
                Xsg = np.array([cell_coords_i_g,]*len(basis_vectors))+basis_vectors
                for x, xg in it.product(Xs, Xsg):
                    XCs.append((x-xg)**2)
                for i, j in it.product(ixs, jxs):
                    Is.append(i)
                    Js.append(j)

        XCs = np.array(XCs)
        Is = np.array(Is)
        Js = np.array(Js)
        CX = np.sum(XCs/cutoff**2, axis=1) #<--- /cutoff**2 is arbitraty, change to a function

        ix = np.where(np.all([CX<=1, CX>0], axis=0))[0]
        distances = np.sqrt(np.sum(XCs[ix], axis=1))

        return distances, Is[ix], Js[ix]
