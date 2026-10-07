# Kept for backward compatibility of the example scripts: the maintained implementation is
# debyetools.get_elastic (this copy had drifted: wrong volume, GPa instead of kBar - review findings 7.4, 7.7).
from debyetools.get_elastic import *  # noqa: F401,F403
from debyetools.get_elastic import parse_outcar, quadratic_fun, get_EM  # noqa: F401
