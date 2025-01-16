from matplotlib import pyplot as plt
from debyetools.tpropsgui.elastic_props import run_script_plots
from debyetools.aux_functions import load_EM


EM = load_EM('../Al3Li_L12/OUTCAR_elastic')/10

fig, ax = plt.subplots(4,3, subplot_kw={'projection': 'polar'}, figsize=(8,12), layout='constrained')
ax = run_script_plots(ax, EM)
plt.show()