import numpy as np
import itertools as it
import debyetools.aux_functions as afn



def neighbor_list(size, max_distance, center, basis_vectors, primitive_cell, ncells=True):
    """ calculate a list i, j, dij where i and j are a pair of atoms of
    indexes i and j, respectively, and dij is the distance between them.

    :param array size: Number of times we are replicating the primitive cel
    :param int max_distance: Number of times we are replicating the supercell up to which we are considering for the calculation (uses pbc)
    :param array center: The position in space where the system of reference is
    :param array basis_vectors: atoms position within a single primitive cell
    :param array primitive_cell: the primitive cell
    :return: D, I , J
    """

    basis_vectors = np.dot(basis_vectors,primitive_cell)
    size_g = size + 2*max_distance  #to do: change max_distance for some other word and add a max_distance distance.
                              # new_co= int(min(max_distance,....))

    cell_coords_centered = afn.generate_cells_coordinates(size, primitive_cell, center)
    cell_coords_centered_g = afn.generate_cells_coordinates(size_g, primitive_cell, center-max_distance)
    # print(size_g)

    XCs = []
    Is = []
    Js = []
    CIXs = []


    ixs = np.arange(len(basis_vectors))
    jxs = np.arange(len(basis_vectors))

    for cell_coords_i in cell_coords_centered:
        ix_neighbor = np.where(np.all(abs(cell_coords_centered_g-cell_coords_i)<=max_distance, axis=1))[0]
        Xs = np.array([cell_coords_i,]*len(basis_vectors))+basis_vectors

        for ixx, cell_coords_i_g in enumerate(cell_coords_centered_g[ix_neighbor]):
            Xsg = np.array([cell_coords_i_g,]*len(basis_vectors))+basis_vectors
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

    CX = np.sum(XCs/max_distance**2, axis=1)

    ix = np.where(np.all([CX<=1, CX>0], axis=0))[0]
    distances = np.sqrt(np.sum(XCs[ix], axis=1))

    res = distances, Is[ix], Js[ix], cell_coords_centered_g, CIXs[ix]

    return res

def pair_analysis(atom_types, size, max_distance, center, basis_vectors, primitive_cell, prec=10, full=False, cutoff=None):
    """
    run a pair analysis of a crystal structure of almost any type of symmetry.

    :param list_of_str atom_types: the types of each atom in the primitive cell in the same order as the basis vectors.
    :param array size: Number of times we are replicating the primitive cel
    :param int max_distance: Number of times we are replicating the supercell up to which we are considering for the calculation (uses pbc)
    :param array center: The position in space where the system of reference is
    :param array basis_vectors: atoms position within a single primitive cell
    :param array primitive_cell: the primitive cell
    :return:  pair distance, pair number, pair types
    """
    max_distance = np.array([int(max_distance), int(max_distance), int(max_distance)]) ##<--- fix_here
    dAxBy, iAxBy, jAxBy, cells_cohordniates, ij_ccix  = neighbor_list(size, max_distance, center, basis_vectors, primitive_cell)
    if cutoff is not None:
        maxdjx = np.where(dAxBy <= cutoff)
        dAxBy, iAxBy, jAxBy, ij_ccix = dAxBy[maxdjx], iAxBy[maxdjx], jAxBy[maxdjx], ij_ccix[maxdjx]
    dAxBy = np.array([np.round(d,prec) for d in dAxBy])
    res_2 = dAxBy, iAxBy, jAxBy
    nat = np.prod(size)*len(basis_vectors)

    combs_types,types_all = afn.c_types(atom_types)

    # dAxBy = np.array([float('%0.10e'%(d)) for d in dAxBy])
    bins_dAxBy =list(set([li for li in list(set(np.append(dAxBy, [max(max_distance)])))]))
    bins_dAxBy.sort()
    distances = bins_dAxBy[:-1]

    ptlst = []
    for i,j,d in zip(iAxBy,jAxBy,dAxBy):
        for ii in range(len(combs_types)):
            if (types_all[i]+'-'+types_all[j] == combs_types[ii]) or (types_all[j]+'-'+types_all[i] == combs_types[ii]):
                pairtype = ii
        ptlst.append(pairtype)

    ptlst=np.array(ptlst)

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
