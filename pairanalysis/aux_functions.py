import itertools as it
import re
def c_types(atom_types):
    types_all = re.findall('[A-Z][^A-Z]*', atom_types)
    ptypes=list(set([s for s in types_all]))
    ptypes.sort()
    combs_types = list(it.combinations_with_replacement(ptypes, r=2))
    combs_types = [A[0]+'-'+A[1] for A in combs_types]
    return combs_types, types_all
