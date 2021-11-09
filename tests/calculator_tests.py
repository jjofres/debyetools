import unittest
import numpy as np
from pairanalysis import NeighborList

class GenerateCellCoordinatesTestCase(unittest.TestCase):
    def setUp(self):
        center = np.array([0,0,0])
        self.coords_generation = NeighborList(center)

    def test_unitary_cell(self):
        """ Test cubic cell of lattice a=1 1x1x1 times and center=(0,0,0)"""
        size = np.array([1,1,1])
        a =1
        primitive_cell = np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])

        result = self.coords_generation.generate_cells_coordinates(size, primitive_cell)

        self.assertTrue(np.array_equal(result, np.array([[0,0,0]])))

    def test_supercell(self):
        """ Test cubic cell of lattice a=4 2x2x2 times and center=(0,0,0) """

        size = np.array([2, 2, 2])
        a = 4
        primitive_cell = np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])

        result = self.coords_generation.generate_cells_coordinates(size, primitive_cell)

        self.assertTrue(np.array_equal(result, np.array([[0, 0, 0], [0, 0, 4], [0, 4, 0], [0, 4, 4], [4, 0, 0], [4, 0, 4], [4, 4, 0], [4, 4, 4]])))

if __name__=='__main__':
    unittest.main()
