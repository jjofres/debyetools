from debyetools.tpropsgui.elastic_props import run_script
from debyetools.aux_functions import load_EM

EM = load_EM( '../Al3Li_L12/OUTCAR_elastic')/10
txt2output, results_data = run_script(EM)

print(txt2output.expandtabs(8))
