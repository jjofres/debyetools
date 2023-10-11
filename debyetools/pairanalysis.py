import numpy as np
import itertools as it
import debyetools.aux_functions as afn
from typing import Tuple

def neighbor_list(size: np.ndarray, basis: np.ndarray, cell: np.ndarray, cutoff: float)->Tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]:
    """ calculate a list i, j, dij where i and j are a pair of atoms of
    indexes i and j, respectively, and dij is the distance between them.

    :param np.ndarray size: Number of times we are replicating the primitive cel
    :param np.ndarray basis: atoms position within a single primitive cell
    :param np.ndarray cell: the primitive cell
    :param float cutoff: cut-off distance
    :return: D, I , J
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
    
    """
    max_depth = np.array([2*int(m) for m in cutoff/np.linalg.norm(cell, axis=1)])
    center = np.array([0,0,0])
    basis = np.dot(basis, cell)
    size_g = size + 2*max_depth

    cell_coords_centered = afn.generate_cells_coordinates(size, cell, center)
    cell_coords_centered_g = afn.generate_cells_coordinates(size_g, cell, center-max_depth)

    XCs = []
    Is = []
    Js = []
    CIXs = []


    ixs = np.arange(len(basis))
    jxs = np.arange(len(basis))

    for cell_coords_i in cell_coords_centered:
        ix_neighbor = np.where(np.all(abs(cell_coords_centered_g-cell_coords_i)<=cutoff, axis=1))[0]
        Xs = np.array([cell_coords_i,]*len(basis))+basis

        for ixx, cell_coords_i_g in enumerate(cell_coords_centered_g[ix_neighbor]):
            Xsg = np.array([cell_coords_i_g,]*len(basis))+basis
            for x, xg in it.product(Xs, Xsg):
                XCs.append((x-xg)**2)
            for i, j in it.product(ixs, jxs):
                Is.append(i)
                Js.append(j)
                CIXs.append(ix_neighbor[ixx])


    XCs = np.array(XCs)
    Is = np.array(Is)
    Js = np.array(Js)
    CIXs = np.array(CIXs)

    CX = np.sum(XCs/cutoff**2, axis=1)

    ix = np.where(np.all([CX<=1, CX>0], axis=0))[0]
    distances = np.sqrt(np.sum(XCs[ix], axis=1))

    return distances, Is[ix], Js[ix], cell_coords_centered_g, CIXs[ix]

def pair_analysis(atom_types, cutoff, basis, cell, prec=10, full=False):
    """
    run a pair analysis of a crystal structure of almost any type of symmetry.

    :param str atom_types: the types of each atom in the primitive cell in the same order as the basis vectors.
    :param float cutoff: cut-off distance
    :param np.ndarray basis: atoms position within a single primitive cell
    :param np.ndarray cell: the primitive cell
    :param int prec: precision.
    :param boolean full: if True, returns also data of ghost cells.
    :return:  pair distance, pair number, pair types
    :rtype: Tuple[np.ndarray,np.ndarray,np.ndarray]
    """
    size=np.array([1,1,1])
    dAxBy, iAxBy, jAxBy, cells_cohordniates, ij_ccix  = neighbor_list(size, basis, cell, cutoff)
    if cutoff is not None:
        maxdjx = np.where(dAxBy <= cutoff)
        dAxBy, iAxBy, jAxBy = dAxBy[maxdjx], iAxBy[maxdjx], jAxBy[maxdjx]
    dAxBy = np.array([np.round(d,prec) for d in dAxBy])
    res_2 = dAxBy, iAxBy, jAxBy
    nat = np.prod(size)*len(basis)

    combs_types,types_all = afn.c_types(atom_types)

    bins_dAxBy =list(set([li for li in list(set(np.append(dAxBy, [cutoff])))]))
    bins_dAxBy.sort()
    distances = bins_dAxBy[:-1]

    ptlst = []
    pairtype = 0
    for i,j,d in zip(iAxBy,jAxBy,dAxBy):
        for ii in range(len(combs_types)):
            if (types_all[i]+'-'+types_all[j] == combs_types[ii]) or (types_all[j]+'-'+types_all[i] == combs_types[ii]):
                pairtype = ii
        ptlst.append(pairtype)

    ptlst = np.array(ptlst)

    ds = ['' for x in range(len(combs_types))]
    for i in range(len(combs_types)):
        ds[i] = np.array([d for d in dAxBy[np.where(ptlst==i)[0]]])
    hs = ['' for x in range(len(combs_types))]
    bs = ['' for x in range(len(combs_types))]
    for i in range(len(combs_types)):
        hs[i], bs[i] = np.histogram(ds[i], bins=bins_dAxBy)
    tot_num_bonds_per_molecule = np.array(hs).T
    num_bonds_per_formula = tot_num_bonds_per_molecule/nat

    if full:
        return np.array(distances), num_bonds_per_formula, combs_types, res_2[0], res_2[1], res_2[2], cells_cohordniates, ij_ccix
    else:
        return np.array(distances), num_bonds_per_formula, combs_types
