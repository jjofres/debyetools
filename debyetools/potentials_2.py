from __future__ import division
from scipy.optimize import least_squares, fmin, minimize

import numpy as np
import debyetools.pairanalysis as pairanalysis

class MP:  # Morse
    def __init__(self, *args, parameters='', prec=10):
        formula, primitive_cell, basis_vectors, cutoff, number_of_distances = args
        self.formula, self.primitive_cell, self.basis_vectors = formula, primitive_cell, basis_vectors

        size = np.array([1, 1, 1])
        center = np.array([0, 0, 0])
        atom_types = formula * np.prod(size)
        pa_results = pairanalysis.pair_analysis(atom_types, size, cutoff, center, basis_vectors, primitive_cell,
                                                                                                          prec=prec)
        distances_of_neigbor_at_Vstar, number_of_pairs_per_distance, combinations_of_types = pa_results

        distances_of_neigbor_at_Vstar = distances_of_neigbor_at_Vstar[:number_of_distances]
        number_of_pairs_per_distance = number_of_pairs_per_distance[:number_of_distances, :]

        self.comb_types = combinations_of_types
        Vstar = np.linalg.det(primitive_cell) / len(basis_vectors)

        self.ndist = distances_of_neigbor_at_Vstar
        self.npair = number_of_pairs_per_distance
        self.Vstar = Vstar

        if parameters != '':
            self.pEOS = parameters

    def fitEOS(self, Vdata, Edata, initial_parameters='', fit=True):
        if fit:
            pEOS = initial_parameters
            lstsq_sol = least_squares(self.error2min, pEOS, args=(Vdata, Edata), bounds=(0, np.inf))
            popt = lstsq_sol['x']
            self.pEOS = popt
            self.eos_residuals = lstsq_sol['fun']
        if not fit:
            self.pEOS = initial_parameters

        mV = minimize(self.E0, np.mean(Vdata), bounds=[(min(Vdata) * .9, max(Vdata) * 1.1)], tol=1e-10)
        self.V0 = mV['x'][0]

        return self.pEOS

    def fitEOS2(self, Vdata, Edata, initial_parameters='', fit=True):
        if fit:
            pEOS = initial_parameters
            lstsq_sol = least_squares(self.error2min2, pEOS, args=(Vdata, Edata), bounds=(0, np.inf))
            popt = lstsq_sol['x']
            self.pEOS = popt
            self.eos_residuals = lstsq_sol['fun']
        if not fit:
            self.pEOS = initial_parameters

        mV = minimize(self.E02, np.mean(Vdata), bounds=[(min(Vdata) * .9, max(Vdata) * 1.1)], tol=1e-10)
        self.V0 = mV['x'][0]

        return self.pEOS

    def morse_ij(self, r, parameters=[]):
        D, alpha, r0 = parameters
        return D * ((1 - np.exp(-alpha * (r - r0))) ** 2 - 1)

    def E04min(self, V, pEOS):
        if type(V) == np.ndarray:
            return np.array([self.E04min(Vi, pEOS) for Vi in V])

        pEOS = np.reshape(pEOS, (len(self.ndist), 3*len(self.npair.T)))
        V = V
        Ds = []
        alphas = []
        r0s = []
        for pEOSi in pEOS:
            pEOSi = np.reshape(pEOSi, (int(len(pEOSi)/3), 3))
            Dsi, alphasi, r0si = pEOSi.T[:]
            Ds.append(Dsi)
            alphas.append(alphasi)
            r0s.append(r0si)
        ms = 0
        Ds = np.array(Ds)
        alphas = np.array(alphas)
        r0s = np.array(r0s)
        for njs, Dj, alphaj, r0j in zip(self.npair.T, Ds.T, alphas.T, r0s.T):
            for rstari, nij, Dij, alphaij, r0ij in zip(self.ndist, njs, Dj, alphaj, r0j):
                ri = rstari*(V/self.Vstar)**(1/3)
                ms += (nij/2*self.morse_ij(ri, parameters=[Dij, alphaij, r0ij]))

        return ms

    def f2map(self, n, r, D, a, r0):
        return n/2*self.morse_ij(r, parameters=[D, a, r0])

    def E04min2(self, V, pEOS_in):
        if type(V) == np.ndarray:
            return np.array([self.E04min2(Vi, pEOS_in) for Vi in V])

        pEOS_2 = np.reshape(pEOS_in, (len(self.ndist), len(self.npair.T), 3))
        rs = np.array([self.ndist for _ in range(len(self.npair.T))]).T*(V/self.Vstar)**(1/3)

        mmatrix = map(self.f2map, self.npair, rs, pEOS_2[:, :, 0], pEOS_2[:, :, 1], pEOS_2[:, :, 2])
        ret = np.sum(list(mmatrix))
        return ret


    def E0(self, V):
        if type(V) == np.ndarray:
            return np.array([self.E0(Vi) for Vi in V])

        pEOS = self.pEOS
        return self.E04min(V,pEOS)

    def E02(self, V):
        if type(V) == np.ndarray:
            return np.array([self.E02(Vi) for Vi in V])

        pEOS = self.pEOS
        return self.E04min2(V, pEOS)

    def error2min(self, P, Vdata, Edata):
        Ecalc = [self.E04min(Vi, P) for Vi in Vdata]
        return Ecalc - Edata

    def error2min2(self, P, Vdata, Edata):
        Ecalc = self.E04min2(Vdata, P)
        return Ecalc - Edata

