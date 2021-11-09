import unittest
import numpy as np
from pairanalysis import NeighborList

class GenerateCellCoordinatesTestCase(unittest.TestCase):
    def setUp(self):
        self.NL = NeighborList()

    def test_gencellcoords_unitary_cell(self):
        """ Test cubic cell of lattice a=1 1x1x1 times and center=(0,0,0)"""
        size = np.array([1,1,1])
        a =1
        primitive_cell = np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])
        center = np.array([0, 0, 0])
        result = self.NL.generate_cells_coordinates(size, primitive_cell, center)

        self.assertTrue(np.array_equal(result, np.array([[0,0,0]])))

    def test_gencellcoords_supercell(self):
        """ Test cubic cell of lattice a=4 2x2x2 times and center=(0,0,0) """

        size = np.array([2, 2, 2])
        a = 4
        primitive_cell = np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])
        center = np.array([0, 0, 0])
        result = self.NL.generate_cells_coordinates(size, primitive_cell, center)

        self.assertTrue(np.array_equal(result, np.array([[0, 0, 0], [0, 0, 4], [0, 4, 0], [0, 4, 4], [4, 0, 0], [4, 0, 4], [4, 4, 0], [4, 4, 4]])))

    def test_nl_0(self):
        """ Test fcc crystal of lattice a=1 1x1x1 times and center=(0,0,0) """
        size = np.array([1, 1, 1])
        cutoff = 2
        center = np.array([0,0,0])
        a = 1
        primitive_cell = np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])
        basis_vectors = np.array([[0,0,0],[.5,.5,0],[.5,0,.5],[0,.5,.5]])
        result = self.NL.neighbor_list(size,cutoff,center,basis_vectors,primitive_cell)
        bool_1 = None==np.testing.assert_array_almost_equal(result[0][3:10],np.array([1.87082869,1.87082869,1.87082869,1.87082869,1.87082869,1.58113883,1.87082869]))
        bool_2 = None==np.testing.assert_array_almost_equal(result[1][3:10],np.array([0,3,0,3,0,0,3]))
        bool_3 = None==np.testing.assert_array_almost_equal(result[2][3:10],np.array([2,1,1,1,1,2,2]))

        self.assertTrue(bool_1 and bool_2 and bool_3 and True)

if __name__=='__main__':
    unittest.main()
