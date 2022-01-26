from debyetools.potentials import EAM
str_comp = 'Al3Sc_D022'#'Al_fcc'#
import numpy as np
if str_comp == 'Al_fcc':
    formula = 'AlAlAlAl'
    primitive_cell = [[4.03969186,0.,0.],
                      [0.,4.03969186,0.],
                      [0.,0.,4.03969186]]

    basis_vectors = [[0.,0.,0.],
                     [0.,0.5,0.5],
                     [0.5,0.,0.5],
                     [0.5,0.5,0.]]
    parameters = [0.18318,0.87227,0.091429,0.20779979,0.196389116,1.113313856,0.937727513,9.75135E-07,0.163110675,1.200599326]

if str_comp == 'Al3Sc_D022':
    formula = 'ScScAlAlAlAlAlAl'
    primitive_cell = np.array([[4.02313455,0.,0.],
                              [0.,4.02313455,0.],
                              [0.,0.,8.82222431]])

    basis_vectors = np.array([[0.,0.,0.,],
                              [0.5,0.5,0.5],
                              [0.5,0.5,0.],
                              [0., 0.5,0.25],
                              [0.5,0., 0.25],
                              [0., 0., 0.5 ],
                              [0.5,0., 0.75],
                              [0., 0.5,0.75]])
    parameters = np.array([0.169819962,0.454365291,0.119099223,0.368288522,0.709933127,1.264964287,0.012154572,0.016058894,0.198616837,0.086910117,1.86383E-05,0.188265644,0.013958715,0.068557233,0.000395168,0.028036644,0.012553532,0.030720411,2.315737178,0.44494801,0.041461558,0.812497249,0.056485806,0.02921995,0.846667671,0.329545854])

cutoff = 10
number_of_neighbor_levels = 8
eam = EAM(formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels,units='eV/atom',parameters=parameters)
print(eam.E0(16.2792233))
