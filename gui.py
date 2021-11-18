#### imports
import PySimpleGUI as sg
from debyetools.tpropsgui.layout import layout
import debyetools.tpropsgui.events as events
import debyetools.tpropsgui.toolbox as tbox
from debyetools.aux_functions import load_doscar, load_V_E, load_EM, load_cell
import debyetools.potentials as potentials
import traceback
from debyetools.poisson import poisson_ratio
from debyetools.electronic import fit_electronic
from debyetools.ndeb import nDeb
from debyetools.aux_functions import gen_Ts
from debyetools.fs_compound_db import fit_FS
import numpy as np
EOS_long_lst = {'Morse':'MP','Birch-Murnaghan (3)':'BM','Rose-Vinet':'RV','Mie-Gruneisen':'MG','TB-SMA':'TB','Murnaghan (1)':'MU','Poirier-Tarantola':'PT','Birch-Murnaghan (4)':'BM4','Murnaghan (2)':'MU2','EAM':'EAM',
                }#'*Morse':'MP','*Birch-Murnaghan (3)':'*BM','*Rose-Vinet':'*RV','*Mie-Gruneisen':'*MG','*TB-SMA':'*TB','*Murnaghan (1)':'*MU','*Poirier-Tarantola':'*PT','*Birch-Murnaghan (4)':'*BM4','*Murnaghan (2)':'*MU2','*EAM':'*EAM'}
EOS_str_lst = ['MP','BM','RV','MG','TB','MU','PT','BM4','MU2','EAM']#,'*MP','*BM','*RV','*MG','*TB','*MU','*PT','*BM4','*MU2','*EAM']
contcar_str = '/CONTCAR.5'
opened_EOS_dict = {str_i:False for str_i in EOS_str_lst}#{'MP':False,'BM':False,'RV':False,'MG':False,'TB':False,'MU':False,'BM3':False}
checked_EOS_dict = {str_i:True for str_i in EOS_str_lst}
EOS2plot_dict = {str_i:'' for str_i in EOS_str_lst}
mws_dict = tbox.MWs('./tests/inpt_files/table_MW')
#


#### Window layout
layout = layout(EOS_str_lst)

#### Window creation
window = sg.Window('ThermoProps V0.0', layout=layout)

#### loop to wait for user action
all_props={}
tprops_dict_all = {}
p_el_inittial = [3.8027342892e-01, -1.8875015171e-02,
                5.3071034596e-04, -7.0100707467e-06]
FS_db_params = {}
while True:
    event, values = window.read()
    print(event)

    # #close window
    if event in (sg.WIN_CLOSED, '--B_close'):
        break
    #
    # #file browser
    if event == '--I_FILEBROWSE_':
        # try:
            # opened_EOS_dict = events.fbrowser_resets(window, opened_EOS_dict)
        str_folderbrowser = events.fbrowser_fill_browser(window, event)
        events.fbrowser_update_fields(window, contcar_str, mws_dict, str_folderbrowser)

    if event == '||B_add_EOS':
        for k in opened_EOS_dict.keys():
            opened_EOS_dict[k]=False
        for k in window['--LBx_EOS_listbox'].get():
            opened_EOS_dict[EOS_long_lst[k]]=True
        print(opened_EOS_dict)

        events.chk_eos(window,opened_EOS_dict)
    #
    #EOS calculation Checkbox
    if '--Chk_calc_params_' in event:
        events.chk_calc_params(window,event)
    #
    #EOS fitting button
    if event == '||B_run_eos_fitting':
        try:
            V_DFT, E_DFT = load_V_E(str_folderbrowser, str_folderbrowser+'/CONTCAR.5', units='J/mol')
            for k in opened_EOS_dict:
                if opened_EOS_dict[k]:
                    if k in ['MP','EAM']:
                        cutoff, number_of_neighbor_levels = float(window['--I_cutoff_MP'].get()), int(window['--I_ndists_MP'].get())
                        formula, primitive_cell, basis_vectors = load_cell(str_folderbrowser+'/CONTCAR.5')
                        args = formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels

                    else:
                        args = ''
                    EOS2params = getattr(potentials,k)(*args)
                    if k == 'MP':
                        initial_parameters =  [0.35, 1, 3.2]*len(EOS2params.comb_types)
                    elif k =='EAM':
                        initial_parameters = [1,1,1,1,1,1]*len(EOS2params.comb_types)+[1,1,1,1]*EOS2params.ntypes
                    else:
                        initial_parameters =  [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00,1e-10]

                    if checked_EOS_dict[k]:
                        print(k, 'fitted')
                        EOS2params.fitEOS(V_DFT, E_DFT, initial_parameters=initial_parameters)
                    else:
                        print(k, 'not fitted')
                        EOS2params.pEOS = [float(pi) for pi in window['--I_params_'+k].get().split(', ')]

                    print(EOS2params.pEOS)
                    events.eos_write_params(window,k,EOS2params.pEOS)

                    EOS2plot_dict[k] = EOS2params
            EOS2plot_dict['V_DFT']=V_DFT
            EOS2plot_dict['E_DFT']=E_DFT
        except Exception as e:
            sg.popup_ok(traceback.format_exc())
    # Plot the fitting
    if event == 'plot fitting::PlotfittingEOS':
        try:
            events.plot_EvV(window, EOS2plot_dict, opened_EOS_dict)
        except Exception as e:
            sg.popup_ok(traceback.format_exc())

    if event == '||B_calc_nu':
        try:
            EM = EM = load_EM(str_folderbrowser+'/OUTCAR.eps')
            nu = poisson_ratio(EM)
            print(nu)
            window['--I_nu'].update('%.3f' % (nu))
        except Exception as e:
            sg.popup_ok(traceback.format_exc())
    if event == '||B_calc_el':
        E, N, Ef = load_doscar(str_folderbrowser+'/DOSCAR.EvV.')
        p_electronic = fit_electronic(V_DFT, p_el_inittial,E,N,Ef)

        window['--I_p_el'].update(', '.join(['%.5e' for _ in p_electronic]) % tuple(p_electronic))

    if event == '||B_run_minF':
        nu = float(window['--I_nu'].get())
        m =float(window['--I_mass'].get())
        p_electronic = [float(stri) for stri in window['--I_p_el'].get().replace(' ','').split(',')]
        p_intanh = [float(stri) for stri in window['--I_p_intanh'].get().replace(' ','').split(',')]
        p_anh = [float(stri) for stri in window['--I_p_anhxc'].get().replace(' ','').split(',')]

        p_defects = float(window['--I_p_evac'].get()),float(window['--I_p_svac'].get()), float(window['--I_Tm'].get()), 0.1
        nDebs_dict = {}
        for k in opened_EOS_dict.keys():
            if opened_EOS_dict[k]:
                nDebs_dict[k] = {'ndeb':'','T':'','V':'','tprops':''}
        T_initial, T_final, number_Temps = float(window['--I_Ti'].get()), float(window['--I_Tf'].get()), float(window['--I_ntemps'].get())
        T = gen_Ts(T_initial, T_final, number_Temps)

        for k in opened_EOS_dict.keys():
            if opened_EOS_dict[k]:
                nDebs_dict[k]['ndeb'] = nDeb(nu, m, p_intanh, EOS2plot_dict[k], p_electronic,
                                     p_defects, p_anh)
                Tmin, Vmin = nDebs_dict[k]['ndeb'].min_F(T,nDebs_dict[k]['ndeb'].EOS.V0)
                nDebs_dict[k]['T'] = np.array(Tmin)
                nDebs_dict[k]['V'] = Vmin
        txt2VT = '#T'

        mtxs = np.array(T)

        for o in opened_EOS_dict:
            if opened_EOS_dict[o]:
                txt2VT = txt2VT + '             '+ o
                mtxs=np.c_[mtxs,nDebs_dict[o]['V']]

        txt2VT = txt2VT+'\n'
        for line in mtxs:
            txt2VT = txt2VT + ' '.join(['%.9e' for _ in line]) % tuple(line) + '\n'
        window['--M_minF_output'].update(txt2VT)

        events.minF_enable_nexts(window)

    if event == '||B_plotter':
        events.plot_VvT(window)


    if event == '||B_eval_tprops':
        for o in opened_EOS_dict:
            if opened_EOS_dict[o]:
                print('Results for:',o)
                tprops_dict_all[o] = nDebs_dict[o]['ndeb'].eval_props(nDebs_dict[o]['T'],nDebs_dict[o]['V'])

                window['--Tab_'+o].update(visible=True)
                #window['--Tab_'+o].select()
                keys_TPs = tprops_dict_all[o].keys()
                tprops_str = '#T          '+' '.join([(j+'            ') for j in list(keys_TPs)[1:]])+'\n'
                TPs_arr = np.c_[tuple([tprops_dict_all[o][j] for j in keys_TPs])]
                for rowi in TPs_arr:
                    tprops_str = tprops_str + ' '.join(['%.11e' for i in rowi])%tuple(rowi)+'\n'
                window['--M_tprop_'+o].update(tprops_str)
                window['--IC_prop2plt'].update(values=list(keys_TPs)[1:])
        window['--Tab_'].update(visible=False)
        events.tprops_enable_nexts(window)

    if event == '||B_plotter_tprops':
        keys_EOS = []
        for o in opened_EOS_dict:
            if opened_EOS_dict[o]:
                keys_EOS.append(o)
        events.plot_tprops(window,keys_EOS)

    #electronic Checkbox
    if event == '--Chk_el':
        events.chk_el(window,event)
    #intrinsic anharmonicity Checkbox
    if event == '--Chk_def':
        events.chk_def(window,event)
    #intrinsic anharmonicity Checkbox
    if event == '--Chk_intanh':
        events.chk_intanh(window,event)
    if event == '--Chk_anhxc':
        events.chk_anhxc(window,event)
    #
    # #parametrization of FS parameters button
    if event == '||B_run_fs_params':
        for o in opened_EOS_dict:
            if opened_EOS_dict[o]:
                FS_db_params[o] = fit_FS(tprops_dict_all[o],float(window['--I_fs_Tfrom'].get()), float(window['--I_fs_Tto'].get()))

                ix_T0 = np.where(np.round(tprops_dict_all[o]['T'],2) == np.round(298.15,2))[0][0]
                H298 = tprops_dict_all[o]['F'][ix_T0]+tprops_dict_all[o]['T'][ix_T0]*tprops_dict_all[o]['S'][ix_T0]
                S298 = tprops_dict_all[o]['S'][ix_T0]

                window['--Tab_fs_'+o].update(visible=True)
                window['--Tab_fs_'+o].select()

                window['--I_H298'+o].update(disabled=False)
                window['--I_H298'+o].update(H298)
                window['--I_S298'+o].update(disabled=False)
                window['--I_S298'+o].update(S298)
                for i in range(len(FS_db_params[o]['Cp'])):
                    window['--I_fsCp_P'+str(i)+o].update(disabled=False)
                    window['--I_fsCp_P'+str(i)+o].update('%.4e'%(FS_db_params[o]['Cp'][i]))
                for i in range(len(FS_db_params[o]['a'])):
                    window['--I_fsa_P'+str(i)+o].update(disabled=False)
                    window['--I_fsa_P'+str(i)+o].update('%.4e'%(FS_db_params[o]['a'][i]))
                for i in range(len(FS_db_params[o]['1/Ks'])):
                    window['--I_fsK_P'+str(i)+o].update(disabled=False)
                    window['--I_fsK_P'+str(i)+o].update('%.4e'%(FS_db_params[o]['1/Ks'][i]))
                for i in range(len(FS_db_params[o]['Ksp'])):
                    window['--I_fsKp_P'+str(i)+o].update(disabled=False)
                    window['--I_fsKp_P'+str(i)+o].update('%.4e'%(FS_db_params[o]['Ksp'][i]))


        window['--Tab_fs_'].update(visible=False)

    if '||B_plotter_fsprop2plt' in event:
        events.plot_fsprops(window,event,FS_db_params, float(window['--I_fs_Tfrom'].get()),float(window['--I_fs_Tto'].get()), tprops_dict_all)


    checked_EOS_dict = events.update_diabled(window,opened_EOS_dict,EOS_str_lst,checked_EOS_dict)
