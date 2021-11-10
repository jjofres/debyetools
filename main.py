from pairanalysis import PairAnalysisCalculator
import numpy as np

center = np.array([0,0,0])
coords_generation = PairAnalysisCalculator()

# Call generation method
size = np.array([2,2,2])
primitive_cell = np.array([[4,0,0],[0,4,0],[0,0,4]])
print(coords_generation.generate_cells_coordinates(size, primitive_cell,center))
