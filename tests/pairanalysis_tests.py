import unittest
import numpy as np
from debyetools import pairanalysis as pa_calc
from debyetools import aux_functions as aux_fn

class GenerateCellCoordinatesTestCase(unittest.TestCase):
    def setUp(self):
        self.size = lambda s: np.array([s,s,s])
        self.center = lambda c: np.array([c, c, c])
        self.primitive_cell = lambda a: np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])
        self.basis_vectors = np.array([[0,0,0],[.5,.5,0],[.5,0,.5],[0,.5,.5]])

    def test_gencellcoords_unitary_cell(self):
        """ Test cubic cell of lattice a=1 1x1x1 times and center=(0,0,0)"""
        result = aux_fn.generate_cells_coordinates(self.size(1), self.primitive_cell(1), self.center(0))
        self.assertTrue(np.array_equal(result, np.array([[0,0,0]])))

    def test_gencellcoords_supercell(self):
        """ Test cubic cell of lattice a=4 2x2x2 times and center=(0,0,0) """
        result = aux_fn.generate_cells_coordinates(self.size(2), self.primitive_cell(4), self.center(0))
        self.assertTrue(np.array_equal(result, np.array([[0, 0, 0], [0, 0, 4], [0, 4, 0], [0, 4, 4], [4, 0, 0], [4, 0, 4], [4, 4, 0], [4, 4, 4]])))

    def test_nl_0(self):
        """ Test fcc crystal of lattice a=1 1x1x1 times and center=(0,0,0) """
        result = pa_calc.neighbor_list(self.size(1),2,self.center(0),self.basis_vectors,self.primitive_cell(1))
        bool_1 = None==np.testing.assert_array_almost_equal(result[0][3:10],np.array([1.87082869,1.87082869,1.87082869,1.87082869,1.87082869,1.58113883,1.87082869]))
        bool_2 = None==np.testing.assert_array_almost_equal(result[1][3:10],np.array([0,3,0,3,0,0,3]))
        bool_3 = None==np.testing.assert_array_almost_equal(result[2][3:10],np.array([2,1,1,1,1,2,2]))

        self.assertTrue(bool_1 and bool_2 and bool_3 and True)

    def test_pa_0(self):
        """ Test the pair analysis calculation for a fcc crystal up to 7NN"""
        results =pa_calc.pair_analysis('AABA', self.size(1), 2, self.center(0), self.basis_vectors, self.primitive_cell(1))
        bool_1 = None == np.testing.assert_array_almost_equal(results[0], np.array(
            [0.70710678, 1., 1.22474487, 1.41421356, 1.58113883, 1.73205081, 1.87082869]))
        bool_2 = None == np.testing.assert_array_almost_equal(results[1][1:3,:], np.array([[4.5,0.,1.5],[12.,12.,0.]]))
        bool_3 = None == np.testing.assert_array_equal(results[2], np.array(['A-A', 'A-B', 'B-B']))

        self.assertTrue(bool_1 and bool_2 and bool_3 and True)

    def test_pa_1(self):
        formula = 'AABA'
        supcell_size = np.array([1,1,1])
        cutoff = 5
        center = np.array([0,0,0])
        basis_vectors = np.array([[0,0,0],[.5,.5,0],[.5,0,.5],[0,.5,.5]])
        primitive_cell =  np.array([[4, 0, 0], [0, 4, 0], [0, 0, 4]])
        distances, num_bonds_per_formula, combs_types = pa_calc.pair_analysis(formula, supcell_size, cutoff, center, basis_vectors, primitive_cell)

        print('')
        print('distances  | # of pairs per type')
        print('           | ' + '  '.join(['%s' for _ in combs_types])%tuple(combs_types))
        for d, n in zip(distances, num_bonds_per_formula):
            print('%.6f  '%(d)+' | ' + ' '.join(['%.2f' for _ in n])%tuple(n))


if __name__=='__main__':
    unittest.main()
