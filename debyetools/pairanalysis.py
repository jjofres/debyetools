import numpy as np
import itertools as it
import debyetools.aux_functions as afn
from typing import Tuple

def neighbor_list(size: np.ndarray, basis: np.ndarray, cell: np.ndarray, cutoff: float)->Tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray,np.ndarray]:
    """ calculate a list i, j, dij where i and j are a pair of atoms of
    indexes i and j, respectively, and dij is the distance between them.

    All image cells that can hold a neighbour within the cut-off are included:
    for an atom pair in image cell n, the fractional component i of the pair
    vector is n_i + (f_j - f_i), and ``abs(r . b_i) <= cutoff*norm(b_i)`` (b_i reciprocal
    vectors, a_i . b_j = delta_ij, 1/norm(b_i) = interplanar spacing). Hence
    ``abs(n_i) <= cutoff*norm(b_i) + span_i``, with span_i the spread of the basis in
    fractional coordinate i. This holds for any cell shape and any cut-off.

    :param np.ndarray size: Number of times we are replicating the primitive cel
    :param np.ndarray basis: atoms position within a single primitive cell (fractional)
    :param np.ndarray cell: the primitive cell (rows = lattice vectors)
    :param float cutoff: cut-off distance
    :return: distances, I, J, image-cell coordinates, image-cell index of each pair
    :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]

    """
    cell = np.asarray(cell, dtype=float)
    basis_frac = np.asarray(basis, dtype=float)
    recip = np.linalg.inv(cell).T
    span = np.ptp(basis_frac, axis=0)
    max_depth = np.ceil(cutoff*np.linalg.norm(recip, axis=1) + span).astype(int)
    center = np.array([0,0,0])
    basis = np.dot(basis_frac, cell)
    size_g = size + 2*max_depth

    cell_coords_centered = afn.generate_cells_coordinates(size, cell, center)
    cell_coords_centered_g = afn.generate_cells_coordinates(size_g, cell, center-max_depth)

    nb = len(basis)
    ng = len(cell_coords_centered_g)
    # pair order: image cell, then atom i, then atom j (same order as the former nested loops)
    ij_I = np.repeat(np.arange(nb), nb)
    ij_J = np.tile(np.arange(nb), nb)
    Is = np.tile(ij_I, ng)
    Js = np.tile(ij_J, ng)
    CIXs = np.repeat(np.arange(ng), nb*nb)
    Xg = cell_coords_centered_g[:, None, :] + basis[None, :, :]          # (ng, nb, 3)

    XCs, Iall, Jall, Call = [], [], [], []
    for cell_coords_i in cell_coords_centered:
        Xs = cell_coords_i + basis                                        # (nb, 3)
        XCs.append(((Xs[None, :, None, :] - Xg[:, None, :, :])**2).reshape(-1, 3))
        Iall.append(Is); Jall.append(Js); Call.append(CIXs)

    XCs = np.concatenate(XCs)
    Is = np.concatenate(Iall)
    Js = np.concatenate(Jall)
    CIXs = np.concatenate(Call)

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

    ptlst = []
    pairtype = 0
    for i,j,d in zip(iAxBy,jAxBy,dAxBy):
        for ii in range(len(combs_types)):
            if (types_all[i]+'-'+types_all[j] == combs_types[ii]) or (types_all[j]+'-'+types_all[i] == combs_types[ii]):
                pairtype = ii
        ptlst.append(pairtype)

    ptlst = np.array(ptlst, dtype=int)

    # count pairs per unique (rounded) distance and pair type; a shell lying exactly
    # at the cut-off is kept as its own shell
    distances = np.unique(dAxBy)
    tot_num_bonds_per_molecule = np.zeros((len(distances), len(combs_types)), dtype=int)
    np.add.at(tot_num_bonds_per_molecule, (np.searchsorted(distances, dAxBy), ptlst), 1)
    num_bonds_per_formula = tot_num_bonds_per_molecule/nat

    if full:
        return np.array(distances), num_bonds_per_formula, combs_types, res_2[0], res_2[1], res_2[2], cells_cohordniates, ij_ccix
    else:
        return np.array(distances), num_bonds_per_formula, combs_types
