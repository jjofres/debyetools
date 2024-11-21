import numpy as np

def cell(w):
    cell = np.array([[0.,0.,0.],[0.,0.,0.],[0.,0.,.0]])
    for i in range(3):
        for j in range(3):
            cell[i,j] = float(w.cellparamsTable.item(i,j).text())
    return cell

def basis(w):
    rows = w.basisTable.rowCount()
    columns = 3
    basis = np.zeros((rows, columns))
    iend = []
    for i in range(rows):
        for j in range(columns):
            try:
                basis[i,j] = float(w.basisTable.item(i,j).text())
            except:
                iend.append(i)
                break
#    print(iend, basis, basis[:iend[0],:])
    return basis[:iend[0],:]

def formula(w):
    rows = w.basisTable.rowCount()
    columns = 3

    types_list = []
    for i in range(rows):
        try:
            types_list.append(w.basisTable.item(i,columns).text())
        except:
            continue

    return types_list

def mass(w):
    mass = 0
    for el in w.molecule.types:
        mass += w.mass_dict[el]
    mass = mass/len(w.molecule.types)

    return mass

def morse_params_molecule(w):
    header = ['D', 'alpha', 'r0']
    morse_params_this = {cti:{hi:0 for hi in header} for cti in w.molecule.combs_types}
    for i in range(len(header)):
        for j in range(len(w.molecule.combs_types)):
            try:
                value = float(w.morse_params_table.item(i, j).text())
            except:
                value = ''
            morse_params_this[w.molecule.combs_types[j]][header[i]] = value

    parameters_as_list = []
    for ci in w.molecule.combs_types:
        for hi in header:
            parameters_as_list.append(morse_params_this[ci][hi])
    return morse_params_this, parameters_as_list

def C(w):
    C = np.zeros((6,6))
    for i in range(6):
        for  j in range(6):
            try:
                C[i,j] = float(w.elasticTable.item(i,j).text())
            except:
                C[i,j] = 0
    return C

def T(w):

    T_initial, T_final, Tstep = (float(sti) for sti in w.ui.lineEdit.text().split())
    T = np.arange(T_initial, T_final+Tstep, Tstep)
    T = np.r_[T, [298.15]]
    T.sort()

    return T

def P(w):
    return float(w.ui.lineEdit_2.text().replace(' ', ''))*1e9

def FS_T(w):
    return float(w.ui.lineEdit_3.text()), float(w.ui.lineEdit_4.text())

