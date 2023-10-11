import sys
from PySide6.QtWidgets import QApplication

from debyetools.tpropsgui.mainwindow import MainWindow
def interface() -> None:
    """
    Function that calls the mainWindow class from  debyetools.tpropsgui.mainwindow.
    """
    app = QApplication(sys.argv)

    widget = MainWindow(app=app)
    # widget.app = app
    widget.show()
    sys.exit(app.exec())

#
def gui():
    from warnings import warn

    warn('This is deprecated', DeprecationWarning, stacklevel=2)

    import PySimpleGUI as sg
    from debyetools.tpropsgui.layout import layout
    import debyetools.tpropsgui.events as events
    # import debyetools.tpropsgui.toolbox as tbox
    from debyetools.aux_functions import load_doscar, load_V_E, load_EM, load_cell
    import debyetools.potentials as potentials
    import traceback
    from debyetools.poisson import poisson_ratio
    from debyetools.electronic import fit_electronic
    from debyetools.ndeb import nDeb
    from debyetools.aux_functions import gen_Ts
    from debyetools.fs_compound_db import fit_FS
    import numpy as np
    # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import debyetools.tpropsgui.plotter_class as plotter


    sg.set_options(element_padding=(0, 0))

    from matplotlib import pyplot as plt
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["mathtext.fontset"] = "dejavuserif"


    EOS_long_lst = {'Morse':'MP','Birch-Murnaghan (3)':'BM','Rose-Vinet':'RV','Mie-Gruneisen':'MG','TB-SMA':'TB','Murnaghan (1)':'MU','Poirier-Tarantola':'PT','Birch-Murnaghan (4)':'BM4','Murnaghan (2)':'MU2','EAM':'EAM'}
    EOS_str_lst = ['MP','BM','RV','MG','TB','MU','PT','BM4','MU2','EAM']

    # loc = '..'
    contcar_str = '/CONTCAR.5'
    opened_EOS_dict = {str_i:False for str_i in EOS_str_lst}
    checked_EOS_dict = {str_i:True for str_i in EOS_str_lst}
    EOS2plot_dict = {str_i:'' for str_i in EOS_str_lst}
    mws_dict = {'Al3Ca_D022': 0.030255624999999998, 'H': 0.0010079, 'He': 0.0040026, 'Li': 0.006941, 'Be': 0.0090122, 'B': 0.010811, 'C': 0.0120107, 'N': 0.0140067, 'O': 0.0159994, 'F': 0.0189984, 'Ne': 0.020179700000000002, 'Na': 0.0229897, 'Mg': 0.024305, 'Al': 0.026981500000000002, 'Si': 0.0280855, 'P': 0.0309738, 'S': 0.032064999999999996, 'Cl': 0.035453000000000005, 'K': 0.0390983, 'Ar': 0.039948, 'Ca': 0.040078, 'Sc': 0.0449559, 'Ti': 0.047867, 'V': 0.0509415, 'Cr': 0.051996099999999996, 'Mn': 0.054938, 'Fe': 0.055845, 'Ni': 0.0586934, 'Co': 0.0589332, 'Cu': 0.063546, 'Zn': 0.06539, 'Ga': 0.069723, 'Ge': 0.07264, 'As': 0.0749216, 'Se': 0.07895999999999999, 'Br': 0.079904, 'Kr': 0.0838, 'Rb': 0.0854678, 'Sr': 0.08762, 'Y': 0.0889059, 'Zr': 0.091224, 'Nb': 0.0929064, 'Mo': 0.09594, 'Tc': 0.098, 'Ru': 0.10107, 'Rh': 0.1029055, 'Pd': 0.10642, 'Ag': 0.1078682, 'Cd': 0.112411, 'In': 0.114818, 'Sn': 0.11871, 'Sb': 0.12176000000000001, 'I': 0.1269045, 'Te': 0.1276, 'Xe': 0.131293, 'Cs': 0.13290549999999998, 'Ba': 0.137327, 'La': 0.1389055, 'Ce': 0.14011600000000002, 'Pr': 0.1409077, 'Nd': 0.14424, 'Pm': 0.145, 'Sm': 0.15036000000000002, 'Eu': 0.151964, 'Gd': 0.15725, 'Tb': 0.1589253, 'Dy': 0.1625, 'Ho': 0.1649303, 'Er': 0.167259, 'Tm': 0.1689342, 'Yb': 0.17304, 'Lu': 0.174967, 'Hf': 0.17849, 'Ta': 0.1809479, 'W': 0.18384, 'Re': 0.18620699999999998, 'Os': 0.19022999999999998, 'Ir': 0.19221700000000003, 'Pt': 0.195078, 'Au': 0.1969665, 'Hg': 0.20059, 'Tl': 0.2043833, 'Pb': 0.2072, 'Bi': 0.2089804, 'Po': 0.209, 'At': 0.21, 'Rn': 0.222, 'Fr': 0.223, 'Ra': 0.226, 'Ac': 0.227, 'Pa': 0.2310359, 'Th': 0.2320381, 'Np': 0.237, 'U': 0.2380289, 'Am': 0.243, 'Pu': 0.244, 'Cm': 0.247, 'Bk': 0.247, 'Cf': 0.251, 'Es': 0.252, 'Fm': 0.257, 'Md': 0.258, 'No': 0.259, 'Rf': 0.261, 'Lr': 0.262, 'Db': 0.262, 'Bh': 0.264, 'Sg': 0.266, 'Mt': 0.268, 'Rg': 0.272, 'Hs': 0.277}

    #### Window layout
    layout = layout(EOS_str_lst)

    #### Window creation
    window1, window2, window3,window4,window5, window7 = sg.Window('tProps V1.0.3', layout=layout, finalize=True), None, None, None, None, None

    #### loop to wait for user action
    all_props={}
    tprops_dict_all = {}
    p_el_initial = [3.8027342892e-01, -1.8875015171e-02,
                    5.3071034596e-04, -7.0100707467e-06]
    FS_db_params = {}

    data4plot_dict = {}
    window5_counter = 0
    windows_ix = ''
    bool_anh = False
    while True:
        window,event, values = sg.read_all_windows()
        # pr0nt(window,event)
        # pr0nt(window1, window2, window3,window4,window5)
        # print(event)
        try:
            ips = event.index('ix')
            ips2 = event[ips:].index('-')
            windows_ix = event[ips+2:ips+ips2]
            # print(windows_ix)
        except:
            print(False)

        # #close window
        if event == sg.WIN_CLOSED or event == '--B_close':
            window.close()
            if window == window2:       # if closing win 2, mark as closed
                window2 = None
                continue
            elif window == window3:       # if closing win 2, mark as closed
                window3 = None
                continue
            elif window == window4:       # if closing win 2, mark as closed
                window4 = None
                continue
            elif window == window5:       # if closing win 2, mark as closed
                window5 = None
                continue
            elif window == window1:     # if closing win 1, exit program
                break
            elif window == window7:
                window7 = None
                bool_anh = False
                continue
        #
        # #file browser
        elif event == '--I_FILEBROWSE_':
            try:
                # opened_EOS_dict = events.fbrowser_resets(window, opened_EOS_dict)
                str_folderbrowser = events.fbrowser_fill_browser(window, event)
                checked_EOS_dict = events.fbrowser_update_fields(window, window7, contcar_str, mws_dict, str_folderbrowser, opened_EOS_dict,EOS_long_lst,EOS_str_lst,checked_EOS_dict, bool_anh)
            except Exception as e:
                sg.popup_ok(traceback.format_exc())
        elif event == '||B_add_EOS':
            try:
                events.add_EOS(window, opened_EOS_dict,EOS_long_lst)
            except Exception as e:
                sg.popup_ok(traceback.format_exc())
#
        #EOS calculation Checkbox
        elif '--Chk_calc_params_' in event:
            try:
                events.chk_calc_params(window,event)
            except Exception as e:
                sg.popup_ok(traceback.format_exc())

        #
        #EOS fitting button

        elif event == '||B_run_eos_fitting':
            # print(verb,'0')
            try:
                # print(verb,'1')
                window['--M_minF_output'].update('')
                for k in EOS_str_lst:
                    window['--M_tprop_'+k].update('')
                    window['--Tab_'+k].update(visible=False)
                    window['--Tab_fs_'+k].update(visible=False)
                    window['--I_H298'+k].update('',disabled=True)
                    window['--I_S298'+k].update('',disabled=True)
                    for i in range(6):
                        window['--I_fsCp_P'+str(i)+k].update('',disabled=True)
                    for i in range(4):
                        window['--I_fsa_P'+str(i)+k].update('',disabled=True)
                    for i in range(4):
                        window['--I_fsK_P'+str(i)+k].update('',disabled=True)
                    for i in range(2):
                        window['--I_fsKp_P'+str(i)+k].update('',disabled=True)
                window['--Tab_'].update(visible=True)
                window['--Tab_'].select()
                window['--Tab_fs_'].update(visible=True)
                window['--Tab_fs_'].select()

                window['--I_fs_Tfrom'].update('')
                window['--I_fs_Tfrom'].update(disabled = True)
                window['--I_fs_Tto'].update('')
                window['--I_fs_Tto'].update(disabled = True)
                window['||B_plotter'].update(disabled=True)
                window['||B_plotter_tprops'].update(disabled=True)
                window['||B_plotter_fsprop2plt'].update(disabled=True)
                window['||B_eval_tprops'].update(disabled=True)
                window['||B_run_fs_params'].update(disabled=True)

                window['--IC_prop2plt'].update('')
                # print(verb,'02')

                V_DFT, E_DFT = load_V_E(str_folderbrowser+'/SUMMARY.fcc', str_folderbrowser+'/CONTCAR.5', units='J/mol')
                # print(verb,'3')

                for k in opened_EOS_dict:
                    if opened_EOS_dict[k]:
                        if k in ['MP','EAM']:
                            # print(verb,'4')

                            cutoff, number_of_neighbor_levels = float(window['--I_cutoff_MP'].get()), int(window['--I_ndists_MP'].get())
                            formula, primitive_cell, basis_vectors = load_cell(str_folderbrowser+'/CONTCAR.5')
                            args = formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels
                            # print(verb,'5')

                        else:
                            args = ''
                        EOS2params = getattr(potentials,k)(*args)
                        if k == 'MP':
                            initial_parameters = [float(pi) for pi in window['--I_params_MP'].get().split(', ')]
                            if np.sum(initial_parameters)==0:
                                initial_parameters =  [0.35, 1, 3.2]*len(EOS2params.comb_types)
                        elif k =='EAM':
                            initial_parameters = [float(pi) for pi in window['--I_params_EAM'].get().split(', ')]
                            if np.sum(initial_parameters)==0:
                                initial_parameters = [3.647649855e-03, 1.240435594e-02, 2.680203750e-04, 1.031741230e-02, 1.486608160e-01, 5.221433411e-02]*len(EOS2params.comb_types)+[2.254792255e+00, 6.613537850e-02, 3.011790966e-01, 5.312117043e-05]*EOS2params.ntypes
                        else:
                            # print(verb,'6')
                            E0 = min(E_DFT)
                            V0 = V_DFT[np.where(E_DFT==E0)]
                            initial_parameters = [float(pi) for pi in window['--I_params_'+k].get().split(', ')]+[0]
                            if np.sum(initial_parameters)==0:
                                initial_parameters =  [E0, V0, 7.618619745e+10, 4.591924487e+00,1e-10]
                            else:
                                pass

                        if checked_EOS_dict[k]:
                            # print(verb,'7')
                            initial_parameters = np.array(initial_parameters,dtype=object)
                            EOS2params.fitEOS(V_DFT, E_DFT, initial_parameters=initial_parameters)
                            # print(k, 'fitted')
                        else:
                            initial_parameters = np.array([float(pi) for pi in window['--I_params_'+k].get().split(', ')])
                            # pr0nt(initial_parameters)
                            EOS2params.fitEOS(V_DFT, E_DFT, initial_parameters=initial_parameters, fit=False)
                            print(k, 'not fitted')
                            #EOS2params.pEOS = np.array([float(pi) for pi in window['--I_params_'+k].get().split(', ')])
                            #EOS2params.V0=1e-5

                        # pr0nt(EOS2params.pEOS)
                        # print(verb,'8')

                        events.eos_write_params(window,k,EOS2params.pEOS)
                        # print(verb,'9')

                        EOS2plot_dict[k] = EOS2params
                EOS2plot_dict['V_DFT']=V_DFT
                EOS2plot_dict['E_DFT']=E_DFT
            except Exception as e:
                sg.popup_ok(traceback.format_exc())
        # Plot the fitting
        #     print(verb,'10')

        elif event == '||B_PlotfittingEOS':
            try:
                if  window2 is not None:
                    window2.close()
                data4plot_dict[str(window5_counter)] = events.plot_EvV(window, EOS2plot_dict, opened_EOS_dict,window5_counter)
                window2 = data4plot_dict[str(window5_counter)].window
                window5_counter+=1

            except Exception as e:
                sg.popup_ok(traceback.format_exc())
        elif event == '--B_edit_fig':
            try:
                if  window3 is not None:
                    window3.close()
                data4plot_dict[str(window5_counter)] = events.plot_EvV_full(window, EOS2plot_dict, opened_EOS_dict,window5_counter)
                window3 = data4plot_dict[str(window5_counter)].window
                window5_counter+=1

            except Exception as e:
                sg.popup_ok(traceback.format_exc())


        elif event == '||B_calc_nu':
            try:
                window['--M_minF_output'].update('')
                for k in EOS_str_lst:
                    window['--M_tprop_'+k].update('')
                    window['--Tab_'+k].update(visible=False)
                    window['--Tab_fs_'+k].update(visible=False)
                    window['--I_H298'+k].update('',disabled=True)
                    window['--I_S298'+k].update('',disabled=True)
                    for i in range(6):
                        window['--I_fsCp_P'+str(i)+k].update('',disabled=True)
                    for i in range(4):
                        window['--I_fsa_P'+str(i)+k].update('',disabled=True)
                    for i in range(4):
                        window['--I_fsK_P'+str(i)+k].update('',disabled=True)
                    for i in range(2):
                        window['--I_fsKp_P'+str(i)+k].update('',disabled=True)
                window['--Tab_'].update(visible=True)
                window['--Tab_'].select()
                window['--Tab_fs_'].update(visible=True)
                window['--Tab_fs_'].select()

                window['--I_fs_Tfrom'].update('')
                window['--I_fs_Tfrom'].update(disabled = True)
                window['--I_fs_Tto'].update('')
                window['--I_fs_Tto'].update(disabled = True)
                window['||B_plotter'].update(disabled=True)
                window['||B_plotter_tprops'].update(disabled=True)
                window['||B_plotter_fsprop2plt'].update(disabled=True)
                window['||B_eval_tprops'].update(disabled=True)
                window['||B_run_fs_params'].update(disabled=True)

                window['--IC_prop2plt'].update('')

                EM = load_EM(str_folderbrowser+'/OUTCAR.eps')
                nu = poisson_ratio(EM)
                window['--I_nu'].update('%.3f' % (nu))
            except Exception as e:
                sg.popup_ok(traceback.format_exc())
        elif event == '||B_calc_el':
            try:
                window['--M_minF_output'].update('')
                for k in EOS_str_lst:
                    window['--M_tprop_'+k].update('')
                    window['--Tab_'+k].update(visible=False)
                    window['--Tab_fs_'+k].update(visible=False)
                    window['--I_H298'+k].update('',disabled=True)
                    window['--I_S298'+k].update('',disabled=True)
                    for i in range(6):
                        window['--I_fsCp_P'+str(i)+k].update('',disabled=True)
                    for i in range(4):
                        window['--I_fsa_P'+str(i)+k].update('',disabled=True)
                    for i in range(4):
                        window['--I_fsK_P'+str(i)+k].update('',disabled=True)
                    for i in range(2):
                        window['--I_fsKp_P'+str(i)+k].update('',disabled=True)
                window['--Tab_'].update(visible=True)
                window['--Tab_'].select()
                window['--Tab_fs_'].update(visible=True)
                window['--Tab_fs_'].select()

                window['--I_fs_Tfrom'].update('')
                window['--I_fs_Tfrom'].update(disabled = True)
                window['--I_fs_Tto'].update('')
                window['--I_fs_Tto'].update(disabled = True)
                window['||B_plotter'].update(disabled=True)
                window['||B_plotter_tprops'].update(disabled=True)
                window['||B_plotter_fsprop2plt'].update(disabled=True)
                window['||B_eval_tprops'].update(disabled=True)
                window['||B_run_fs_params'].update(disabled=True)

                window['--IC_prop2plt'].update('')
                E, N, Ef = load_doscar(str_folderbrowser+'/DOSCAR.EvV.')
                p_electronic = fit_electronic(V_DFT, p_el_initial,E,N,Ef)

                window['--I_p_el'].update(', '.join(['%.5e' for _ in p_electronic]) % tuple(p_electronic))
            except FileNotFoundError:
                sg.popup_ok("DOSCAR files not found.\n\nIf you don't have any, try using your own parameter values or just without electronic contribution.")
            except Exception as e:
                # print(e.__class__)
                sg.popup_ok(traceback.format_exc())

        elif event == '||B_run_minF':
            # mode=''
            try:
                for k in EOS_str_lst:
                    window['--M_tprop_'+k].update('')
                    window['--Tab_'+k].update(visible=False)
                    window['--Tab_fs_'+k].update(visible=False)
                    window['--I_H298'+k].update('',disabled=True)
                    window['--I_S298'+k].update('',disabled=True)
                    for i in range(6):
                        window['--I_fsCp_P'+str(i)+k].update('',disabled=True)
                    for i in range(4):
                        window['--I_fsa_P'+str(i)+k].update('',disabled=True)
                    for i in range(4):
                        window['--I_fsK_P'+str(i)+k].update('',disabled=True)
                    for i in range(2):
                        window['--I_fsKp_P'+str(i)+k].update('',disabled=True)
                window['--Tab_'].update(visible=True)
                window['--Tab_'].select()
                window['--Tab_fs_'].update(visible=True)
                window['--Tab_fs_'].select()

                window['--I_fs_Tfrom'].update('')
                window['--I_fs_Tfrom'].update(disabled = True)
                window['--I_fs_Tto'].update('')
                window['--I_fs_Tto'].update(disabled = True)
                window['||B_plotter'].update(disabled=True)
                window['||B_plotter_tprops'].update(disabled=True)
                window['||B_plotter_fsprop2plt'].update(disabled=True)
                window['||B_eval_tprops'].update(disabled=True)
                window['||B_run_fs_params'].update(disabled=True)

                window['--IC_prop2plt'].update('')

                nu = float(window['--I_nu'].get())
                m =float(window['--I_mass'].get())




                if window['--Chk_def'].get():
                    p_defects = float(window['--I_p_evac'].get()),float(window['--I_p_svac'].get()), float(window['--I_Tm'].get()), 0.1
                else:
                    p_defects = 1e10, 0, float(window['--I_Tm'].get()), 0.1
                if window['--Chk_anhxc'].get():
                    p_anh = [float(stri) for stri in window['--I_p_anhxc'].get().replace(' ', '').split(',')]
                else:
                    p_anh = [0,0,0]
                nDebs_dict = {}
                if window['--Chk_intanh'].get():
                    p_intanh = [float(stri) for stri in window['--I_p_intanh'].get().replace(' ', '').split(',')]
                else:
                    p_intanh = [0,1]
                if window['--Chk_el'].get():
                    p_electronic = [float(stri) for stri in window['--I_p_el'].get().replace(' ', '').split(',')]
                else:
                    p_electronic = [0,0,0,0]

                for k in opened_EOS_dict.keys():
                    if opened_EOS_dict[k]:
                        nDebs_dict[k] = {'ndeb':'','T':'','V':'','tprops':''}
                Pressure, T_initial, T_final, number_Temps = window['--I_Pi'].get(), float(window['--I_Ti'].get()), float(window['--I_Tf'].get()), float(window['--I_ntemps'].get())

                Pressure = float(Pressure)


                T = gen_Ts(T_initial, T_final, number_Temps)

                for k in opened_EOS_dict.keys():
                    if opened_EOS_dict[k]:
                        # print(window['--I_formula'].get(), nu, m, p_intanh, EOS2plot_dict[k], p_electronic,p_defects, p_anh, mode)
                        nDebs_dict[k]['ndeb'] = nDeb(nu, m, p_intanh, EOS2plot_dict[k], p_electronic,
                                             p_defects, p_anh, mode=mode)
                        Tmin, Vmin = nDebs_dict[k]['ndeb'].min_G(T,EOS2plot_dict[k].V0,Pressure)
                        #Tmin, Vmin = nDebs_dict[k]['ndeb'].min_G(T,nDebs_dict[k]['ndeb'].EOS.V0,Pressure, Vmin[0], a_DM, b_DM)
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
            except Exception as e:
                sg.popup_ok(traceback.format_exc())

        elif event == '||B_plotter':
            try:
                # if  window4 is not None:
                #     window4.close()
                data4plot_dict[str(window5_counter)] = events.plot_VvT(window,window5_counter)
                window4 = data4plot_dict[str(window5_counter)].window
                window5_counter +=1
            except Exception as e:
                sg.popup_ok(traceback.format_exc())


        elif event == '||B_eval_tprops':
            try:
                for o in opened_EOS_dict:
                    if opened_EOS_dict[o]:
                        # print('Results for:',o)
                        tprops_dict_all[o] = nDebs_dict[o]['ndeb'].eval_props(nDebs_dict[o]['T'],nDebs_dict[o]['V'],Pressure)

                        window['--Tab_'+o].update(visible=True)
                        #window['--Tab_'+o].select()
                        keys_TPs = tprops_dict_all[o].keys()
                        tprops_str = '#T          '+' '.join([(j+'            ') for j in list(keys_TPs)[1:]])+'\n'
                        TPs_arr = np.c_[tuple([tprops_dict_all[o][j] for j in keys_TPs])]
                        for rowi in TPs_arr:
                            tprops_str = tprops_str + ' '.join(['%.11e' for i in rowi])%tuple(rowi)+'\n'
                        window['--M_tprop_'+o].update(tprops_str)
                        window['--IC_prop2plt'].update(values=list(keys_TPs)[1:])



                for k in EOS_str_lst:
                    window['--Tab_fs_'+k].update(visible=False)
                    window['--I_H298'+k].update('',disabled=True)
                    window['--I_S298'+k].update('',disabled=True)
                    for i in range(6):
                        window['--I_fsCp_P'+str(i)+k].update('',disabled=True)
                    for i in range(4):
                        window['--I_fsa_P'+str(i)+k].update('',disabled=True)
                    for i in range(4):
                        window['--I_fsK_P'+str(i)+k].update('',disabled=True)
                    for i in range(2):
                        window['--I_fsKp_P'+str(i)+k].update('',disabled=True)
                window['--Tab_fs_'].update(visible=True)
                window['--Tab_fs_'].select()
                window['--I_fs_Tfrom'].update('')
                window['--I_fs_Tfrom'].update(disabled = True)
                window['--I_fs_Tto'].update('')
                window['--I_fs_Tto'].update(disabled = True)
                window['||B_plotter_fsprop2plt'].update(disabled=True)
                window['||B_run_fs_params'].update(disabled=True)

                window['--Tab_'].update(visible=False)
                events.tprops_enable_nexts(window)



            except Exception as e:
                sg.popup_ok(traceback.format_exc())

        elif event == '||B_eval_anh':
            if opened_EOS_dict['MU']==False:
                sg.popup_ok('Please add the Murnaghan EOS to the calculation.')
            elif len([o for o in opened_EOS_dict if opened_EOS_dict[o] == True])<2:
                sg.popup_ok('Please add at least one EOS different from Murnaghan to evaluate its anharmonicity contribution.')

            else:
                anh_arr_MU = np.c_[tuple([tprops_dict_all['MU'][j] for j in keys_TPs])]
                import debyetools.tpropsgui.elements as elmt
                # print('XXXXXXXXXXXXXXXXXXXXXXXXX')
                lo_tabs_anh = [[elmt.Tab(eos_str,[[elmt.sCol([[elmt.M('','anh_'+eos_str,1000,7)]], 'anh_'+eos_str, 470, 80)]],'anh_'+eos_str,False) for eos_str in ['','MP','BM','RV','MG','TB','MU','PT','BM4','MU2','EAM','*MP','*BM','*RV','*MG','*TB','*MU','*PT','*BM4','*MU2','*EAM']]]

                lo_anh = [[elmt.TG(lo_tabs_anh, 'tabs_anh')],
                          [elmt.T('select property to plot:', 'anh2plt'),
                           elmt.ICombo(['       ', '       ', '       ', '       '], 'anh2plt', 10, 1),
                           elmt.Bc('Plot', 'plotter_anh', ('white', elmt.theme_background_color()))]]

                data4plot_dict[str(window5_counter)] = sg.Window('Anh', lo_anh, finalize=True)
                window7 = data4plot_dict[str(window5_counter)]
                window5_counter += 1


                for o in opened_EOS_dict:
                    if opened_EOS_dict[o]:
                        anh_arr = np.c_[tuple([tprops_dict_all[o][j] for j in keys_TPs])]
                        for i in range(len(anh_arr_MU[:,0])):
                            anh_arr_MU[i, 0] = 0

                        anh_arr = anh_arr - anh_arr_MU

                        anh_str = '#T          '+' '.join([(j+'            ') for j in list(keys_TPs)[1:]])+'\n'
                        # TPs_arr = np.c_[tuple([tprops_dict_all[o][j] for j in keys_TPs])]
                        for rowi in anh_arr:
                            anh_str = anh_str + ' '.join(['%.11e' for i in rowi])%tuple(rowi)+'\n'
                        window7['--M_anh_'+o].update(anh_str)
                        window7['--IC_anh2plt'].update(values=list(keys_TPs)[1:])
                        window7['--Tab_anh_' + o].update(visible=True)



                        # pr0nt(anh_arr-anh_arr_MU)
                window7['--Tab_anh_'].update(visible=False)
                bool_anh = True
                # print('bool_anh', bool_anh)

        elif event == '||B_plotter_tprops':
            try:
                keys_EOS = []
                for o in opened_EOS_dict:
                    if opened_EOS_dict[o]:
                        keys_EOS.append(o)
                # if  window5 is not None:
                #     window5.close()
                data4plot_dict[str(window5_counter)] = events.plot_tprops(window,keys_EOS,window5_counter)
                window5 = data4plot_dict[str(window5_counter)].window
                window5_counter+=1
                # pr0nt(window5)
            except Exception as e:
                sg.popup_ok(traceback.format_exc())
        elif event == '||B_plotter_anh':
            try:
                keys_EOS = []
                for o in opened_EOS_dict:
                    if opened_EOS_dict[o]:
                        keys_EOS.append(o)
                # if  window5 is not None:
                #     window5.close()
                data4plot_dict[str(window5_counter)] = events.plot_anh(window7,keys_EOS,window5_counter)
                window6 = data4plot_dict[str(window5_counter)].window
                window5_counter+=1
                # pr0nt(window5)
            except Exception as e:
                sg.popup_ok(traceback.format_exc())

        #electronic Checkbox
        elif event == '--Chk_el':
            try:
                events.chk_el(window,event)
            except Exception as e:
                sg.popup_ok(traceback.format_exc())
        #intrinsic anharmonicity Checkbox
        elif event == '--Chk_def':
            try:
                events.chk_def(window,event)
            except Exception as e:
                sg.popup_ok(traceback.format_exc())
        #intrinsic anharmonicity Checkbox
        elif event == '--Chk_intanh':
            try:
                events.chk_intanh(window,event)
            except Exception as e:
                sg.popup_ok(traceback.format_exc())

        elif event == '--Chk_anhxc':
            try:
                events.chk_anhxc(window,event)
            except Exception as e:
                sg.popup_ok(traceback.format_exc())
        #
        # #parametrization of FS parameters button
        elif event == '||B_run_fs_params':
            try:
                for o in opened_EOS_dict:
                    if opened_EOS_dict[o]:
                        FS_db_params[o] = fit_FS(tprops_dict_all[o],float(window['--I_fs_Tfrom'].get()), float(window['--I_fs_Tto'].get()))

                        ix_T0 = np.where(np.round(tprops_dict_all[o]['T'],2) == np.round(298.15,2))[0][0]
                        H298 = tprops_dict_all[o]['G'][ix_T0]+tprops_dict_all[o]['T'][ix_T0]*tprops_dict_all[o]['S'][ix_T0]
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
                            #window['--I_fsCp_P'+str(0)+o].update(' '.join(['%.7e' for i in FS_db_params[o]['Cp']])%tuple(FS_db_params[o]['Cp']))
                        for i in range(len(FS_db_params[o]['a'])):
                            window['--I_fsa_P'+str(i)+o].update(disabled=False)
                            window['--I_fsa_P'+str(i)+o].update('%.4e'%(FS_db_params[o]['a'][i]))
                            #window['--I_fsa_P'+str(0)+o].update(' '.join(['%.7e' for i in FS_db_params[o]['a']])%tuple(FS_db_params[o]['a']))

                        for i in range(len(FS_db_params[o]['1/Ks'])):
                            window['--I_fsK_P'+str(i)+o].update(disabled=False)
                            window['--I_fsK_P'+str(i)+o].update('%.4e'%(FS_db_params[o]['1/Ks'][i]))
                            #window['--I_fsK_P'+str(0)+o].update(' '.join(['%.7e' for i in FS_db_params[o]['1/Ks']])%tuple(FS_db_params[o]['1/Ks']))

                        for i in range(len(FS_db_params[o]['Ksp'])):
                            window['--I_fsKp_P'+str(i)+o].update(disabled=False)
                            window['--I_fsKp_P'+str(i)+o].update('%.4e'%(FS_db_params[o]['Ksp'][i]))
                            #window['--I_fsKp_P'+str(0)+o].update(' '.join(['%.7e' for i in FS_db_params[o]['Ksp']])%tuple(FS_db_params[o]['Ksp']))

                        # print('xxxxx', window['--I_formula'].get(), window['--I_strkt'].get(),o,mode,H298,S298,' '.join(['%.7e' for i in FS_db_params[o]['Cp']])%tuple(FS_db_params[o]['Cp']), ' '.join(['%.7e' for i in FS_db_params[o]['a']])%tuple(FS_db_params[o]['a']), ' '.join(['%.7e' for i in FS_db_params[o]['1/Ks']])%tuple(FS_db_params[o]['1/Ks']), ' '.join(['%.7e' for i in FS_db_params[o]['Ksp']])%tuple(FS_db_params[o]['Ksp']))


                window['--Tab_fs_'].update(visible=False)
            except Exception as e:
                sg.popup_ok(traceback.format_exc())

        elif '||B_plotter_fsprop2plt' in event:
            try:
                data4plot_dict[str(window5_counter)] = events.plot_fsprops(window,event,FS_db_params, float(window['--I_fs_Tfrom'].get()),float(window['--I_fs_Tto'].get()), tprops_dict_all,window5_counter)
                window8 = data4plot_dict[str(window5_counter)].window
                window5_counter+=1
            except Exception as e:
                sg.popup_ok(traceback.format_exc())
        elif '--Chk_mode_' in event:
            window['--M_minF_output'].update('')
            l = ['jjsl', 'jjdm', 'jjfv',
                 # 'DM', 'Sl', 'VZ', 'mfv'
                 ]
            l.remove(event.replace('--Chk_mode_',''))
            for stri in l:
                window['--Chk_mode_'+stri].update(False)
            # if window['--Chk_mode_jj'].get()==True:
            #     for stri in ['DM', 'Sl', 'VZ', 'mfv']:
            #         window['--Chk_mode_'+stri].update(disabled=True)
            #
            # if window['--Chk_mode_jj'].get()==False:
            #     for stri in ['DM', 'Sl', 'VZ', 'mfv']:
            #         window['--Chk_mode_'+stri].update(disabled=False)

            if window[event].get():
                mode = event.replace('--Chk_mode_','')
            else:
                mode = 'xx'
            # print(mode)


        elif event in ['--B_ix'+windows_ix+'-figwidth_UP', '--B_ix'+windows_ix+'-figheight_UP', '--B_ix'+windows_ix+'-figwidth_DN', '--B_ix'+windows_ix+'-figheight_DN']:
            data4plot_dict[windows_ix].increment_b_updn(event, values,0.1,1)
            data4plot_dict[windows_ix].update_formats()
            data4plot_dict[windows_ix].update_canvas(show=False)
        elif event in ['--B_ix'+windows_ix+'-titlesize_UP','--B_ix'+windows_ix+'-labelxsize_UP','--B_ix'+windows_ix+'-labelysize_UP','--B_ix'+windows_ix+'-titlesize_DN','--B_ix'+windows_ix+'-labelxsize_DN','--B_ix'+windows_ix+'-labelysize_DN','--B_ix'+windows_ix+'-legendncol_UP','--B_ix'+windows_ix+'-legendncol_DN','--B_ix'+windows_ix+'-legendfontsize_UP','--B_ix'+windows_ix+'-legendfontsize_DN']:
            data4plot_dict[windows_ix].increment_b_updn(event, values,1,None)
            data4plot_dict[windows_ix].update_formats()
            data4plot_dict[windows_ix].update_canvas(show=False)
        elif event in ['--B_ix'+windows_ix+'-lmargin_UP','--B_ix'+windows_ix+'-rmargin_UP','--B_ix'+windows_ix+'-bmargin_UP','--B_ix'+windows_ix+'-tmargin_UP','--B_ix'+windows_ix+'-lmargin_DN','--B_ix'+windows_ix+'-rmargin_DN','--B_ix'+windows_ix+'-bmargin_DN','--B_ix'+windows_ix+'-tmargin_DN','--B_ix'+windows_ix+'-titlexpos_UP','--B_ix'+windows_ix+'-titlexpos_DN','--B_ix'+windows_ix+'-titleypos_UP','--B_ix'+windows_ix+'-titleypos_DN']:
            data4plot_dict[windows_ix].increment_b_updn(event, values,0.01,2)
            data4plot_dict[windows_ix].update_formats()
            data4plot_dict[windows_ix].update_canvas(show=False)
        elif event in ['--B_ix'+windows_ix+'-limxmax_UP','--B_ix'+windows_ix+'-limxmin_UP','--B_ix'+windows_ix+'-limxmax_DN','--B_ix'+windows_ix+'-limxmin_DN','--B_ix'+windows_ix+'-limymax_UP','--B_ix'+windows_ix+'-limymin_UP','--B_ix'+windows_ix+'-limymax_DN','--B_ix'+windows_ix+'-limymin_DN']:
            data4plot_dict[windows_ix].increment_b_updn(event, values,.1,2)
            data4plot_dict[windows_ix].update_formats()
            data4plot_dict[windows_ix].update_canvas(show=False)
        elif event in ['ix'+windows_ix+'-use_grid','ix'+windows_ix+'-use_legend','ix'+windows_ix+'-use_xlabel','ix'+windows_ix+'-use_ylabel','ix'+windows_ix+'-use_title','ix'+windows_ix+'-auto_xlim','ix'+windows_ix+'-auto_ylim']:
            data4plot_dict[windows_ix].update_formats()
            data4plot_dict[windows_ix].update_canvas(show=False)

        elif ('++plot++' in event or '--B_ix'+windows_ix+'-refresh' in event):
            data4plot_dict[windows_ix].update_lines_settings()
            data4plot_dict[windows_ix].update_formats()
            data4plot_dict[windows_ix].update_canvas(show=False)

        elif ('++linewidth++'in event or '++markersize++'in event) :
            data4plot_dict[windows_ix].increment_b_updn(event, values,1,None)
            data4plot_dict[windows_ix].update_lines_settings()
            data4plot_dict[windows_ix].update_formats()
            data4plot_dict[windows_ix].update_canvas(show=False)
        elif event == '--B_ix'+windows_ix+'-loaddata':
            filename = sg.popup_get_file('Load Figure...')
            try:
                with open(filename,'r') as f:
                    lines=f.readlines()
                    setting_dict = {}
                    for line in lines:
                        if '->' in line[0:2] and '<-' in line[-3:-1]:
                            setting_dict[line[2:-3]]={}
                            last_keylvl0 = line[2:-3]
                            lvl = 0
                            continue
                        elif '*>' in line[0:2] and '<*' in line[-3:-1]:
                            setting_dict[last_keylvl0][line[2:-3]]={}
                            last_keylvl1 = line[2:-3]
                            lvl = 1
                            continue
                        if '*k>' in line[0:3]:
                            if lvl == 0:
                                ix0 = line.find('*k>')
                                ix1 = line.find('<k*')
                                jx0 = line.find('>|')
                                jx1 = line.find('|<')
                                val = line[jx0+2:jx1].replace('||newline','\n')
                                if val == 'True':
                                    val=True
                                if val == 'False':
                                    val=False
                                setting_dict[last_keylvl0][line[ix0+3:ix1]] = val
                            if lvl == 1:
                                ix0 = line.find('*k>')
                                ix1 = line.find('<k*')
                                jx0 = line.find('>|')
                                jx1 = line.find('|<')
                                val = line[jx0+2:jx1].replace('||newline','\n')
                                if val == 'True':
                                    val=True
                                if val == 'False':
                                    val=False
                                setting_dict[last_keylvl0][last_keylvl1][line[ix0+3:ix1]] = val

            except Exception as e:
                sg.popup_ok(traceback.format_exc())
            data4plot_dict[windows_ix].window.close()
            tabs = plotter.tabs(setting_dict['tabs_multilinetxt'])
            data4plot_dict[windows_ix] = plotter.dataplot(windows_ix)
            data4plot_dict[windows_ix].load_tab_data(tabs)
            data4plot_dict[windows_ix].load_lines_settings(setting_dict['lines_settings'])

            data4plot_dict[windows_ix].create_window()
            data4plot_dict[windows_ix].fig_settings=setting_dict['figure_settings']
            data4plot_dict[windows_ix].update_window(setting_dict['figure_settings'])
            data4plot_dict[windows_ix].create_canvas(show=False)

        elif event == '--B_ix'+windows_ix+'-savefig':

            filename = sg.popup_get_file('Save Figure',save_as=True)
            data4plot_dict[windows_ix].fig.savefig(filename+".pdf")

            with open(filename+'.ftg','w') as f:
                f.write('->figure_settings<-\n')
                for k in data4plot_dict[windows_ix].fig_settings.keys():
                    f.write('*k>'+k+'<k*'+">|"+str(data4plot_dict[windows_ix].window['ix'+windows_ix+'-'+k].get())+'|<\n')

                f.write('->lines_settings<-\n')
                for l in data4plot_dict[windows_ix].lines.keys_list:
                    f.write('*>'+l+'<*\n')
                    for k in getattr(data4plot_dict[windows_ix].lines,l)['settings'].keys():
                        f.write('*k>'+k+'<k*'+">|"+str(getattr(data4plot_dict[windows_ix].lines,l)['settings'][k])+'|<\n')

                f.write('->tabs_multilinetxt<-\n')
                for i,l in enumerate(data4plot_dict[windows_ix].lines.keys_list):
                    f.write('*>t'+str(i)+'<*\n')
                    f.write('*k>'+'multiline<k*>|')
                    f.write('#X '+getattr(data4plot_dict[windows_ix].lines,l)['label']+'||newline')
                    sm_array = np.array([getattr(data4plot_dict[windows_ix].lines,l)['x'],getattr(data4plot_dict[windows_ix].lines,l)['y']]).T
                    for line in sm_array:
                        f.write(str(line[0])+' '+str(line[1])+'||newline')
                    f.write('|<\n')

        elif '--B_ix'+windows_ix+'-editdata' == event:
            data4plot_dict[windows_ix].create_popupwindow()

            while True:
                event2, values2 = data4plot_dict[windows_ix].popup_window.read()
                # print(event2)
                if event2 in ('--B_ok_w2',sg.WIN_CLOSED):
                    # print('ok')
                    break

                if event2 == '--B_addtab_w2':
                    data4plot_dict[windows_ix].copy_multiline2dic(add=True)
                    data4plot_dict[windows_ix].popup_window.close()
                    data4plot_dict[windows_ix].create_popupwindow()
                    data4plot_dict[windows_ix].popup_window['--Tab_data_'+data4plot_dict[windows_ix] .tabs.keys()[-1]].select()
                    # pr0nt(data4plot.tabs.keys())

                if '--B_remove_t' in event2:
                    # pr0nt(event2.replace('_',' ').split()[2])
                    delattr(data4plot_dict[windows_ix].tabs,event2.replace('_',' ').split()[2])
                    data4plot_dict[windows_ix].copy_multiline2dic()
                    data4plot_dict[windows_ix].popup_window.close()
                    data4plot_dict[windows_ix].create_popupwindow()

            data4plot_dict[windows_ix].copy_multiline2dic()
            data4plot_dict[windows_ix].load_tab_data(data4plot_dict[windows_ix].tabs)

            data4plot_dict[windows_ix].load_lines_settings(data4plot_dict[windows_ix].lines_settings)

            data4plot_dict[windows_ix].window.close()
            data4plot_dict[windows_ix].create_window()
            data4plot_dict[windows_ix].update_window(data4plot_dict[windows_ix].fig_settings)
            data4plot_dict[windows_ix].create_canvas(show=False)

            data4plot_dict[windows_ix].popup_window.close()
        checked_EOS_dict = events.update_diabled(window1, window7,opened_EOS_dict,EOS_str_lst,checked_EOS_dict, bool_anh)

