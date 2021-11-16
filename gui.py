#### imports
import PySimpleGUI as sg
from debyetools.tpropsgui.layout import layout
import debyetools.tpropsgui.events as events
import debyetools.tpropsgui.toolbox as tbox
from debyetools.aux_functions import load_doscar, load_V_E, load_EM, load_cell
import debyetools.potentials as potentials
import traceback
from debyetools.poisson import poisson_ratio

EOS_long_lst = {'Morse':'MP','Birch-Murnaghan (3)':'BM','Rose-Vinet':'RV','Mie-Gruneisen':'MG','TB-SMA':'TB','Murnaghan (1)':'MU','Poirier-Tarantola':'PT','Birch-Murnaghan (4)':'BM4','Murnaghan (2)':'MU2','EAM':'EAM',
                }#'*Morse':'MP','*Birch-Murnaghan (3)':'*BM','*Rose-Vinet':'*RV','*Mie-Gruneisen':'*MG','*TB-SMA':'*TB','*Murnaghan (1)':'*MU','*Poirier-Tarantola':'*PT','*Birch-Murnaghan (4)':'*BM4','*Murnaghan (2)':'*MU2','*EAM':'*EAM'}
EOS_str_lst = ['MP','BM','RV','MG','TB','MU','PT','BM4','MU2','EAM']#,'*MP','*BM','*RV','*MG','*TB','*MU','*PT','*BM4','*MU2','*EAM']
contcar_str = '/CONTCAR.5'
opened_EOS_dict = {str_i:False for str_i in EOS_str_lst}#{'MP':False,'BM':False,'RV':False,'MG':False,'TB':False,'MU':False,'BM3':False}
checked_EOS_dict = {str_i:True for str_i in EOS_str_lst}
EOS2plot_dict = {str_i:'' for str_i in EOS_str_lst}
# doscar_str = '/DOSCAR.EvV.'
# eps_str = '/OUTCAR.eps'
mws_dict = tbox.MWs('./tests/inpt_files/table_MW')
#
# #print(tms_dict)
# params_dict = {}

#### Window layout
layout = layout(EOS_str_lst)

#### Window creation
window = sg.Window('ThermoProps V0.0', layout=layout)

#### loop to wait for user action
all_props={}
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
    #     except Exception as e:
    #         sg.popup_ok(str(e))
    # # #EOS Checkbox
    # if '--LBx_EOS_listbox' in event:#'--Chk_eos_' in event:
    #     print(window[event].get())
    #     #
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
        EM = EM = load_EM(str_folderbrowser+'/OUTCAR.eps')
        nu = poisson_ratio(EM)
        print(nu)
        window['--I_nu'].update('%.3f' % (nu))


    #     try:
    #         initial_compound_path = window['--I_compound'].get()
    #         if initial_compound_path == '':
    #             sg.popup_ok('Please select a compound/element.')
    #             continue
    #         params_dict = events.eos_fitting(window,opened_EOS_dict,initial_compound_path,contcar_str,params_dict)
    #         events.eos_write_params(window,params_dict)
    #         for K in EOS_str_lst:
    #             try:
    #                 print(K,' '.join(['%.10e' for _ in params_dict[K]]) % tuple(params_dict[K]))
    #             except:
    #                 print(K,';;;')
    #     except Exception as e:
    #         sg.popup_ok(str(e))
    #
    # #Nu calculation button
    # if event == '||B_calc_nu':
    #     try:
    #         txt_out,nu_bool,txt_out2 = events.calc_nu(window,eps_str)
    #
    #         print(txt_out2)
    #     except Exception as e:
    #         sg.popup_ok(str(e))
    #
    # #electronic Checkbox
    # if event == '--Chk_el':
    #     events.chk_el(window,event)
    #
    # #electronic calculation button
    # if event == '||B_calc_el':
    #     try:
    #         events.calc_el(window,doscar_str,contcar_str)
    #     except Exception as e:
    #         sg.popup_ok(str(e))
    #
    # #intrinsic anharmonicity Checkbox
    # if event == '--Chk_def':
    #     events.chk_def(window,event)
    #
    # #intrinsic anharmonicity Checkbox
    # if event == '--Chk_intanh':
    #     events.chk_intanh(window,event)
    # if event == '--Chk_anhxc':
    #     events.chk_anhxc(window,event)
    #
    # #run free energy minimization button
    # if event == '||B_run_minF':
    #     try:
    #         events.minF_enable_nexts(window)
    #         Ti,Tf,nu,r,m = events.minF_get_ins(window)
    #         T = events.minF_generate_Temps(window,Ti,Tf)
    #         minF_header,Volume_calculated,ndeb_dict = events.minF_run_minimization(window,T,nu, r, m,Tf,contcar_str,EOS_str_lst,opened_EOS_dict)
    #     except Exception as e:
    #         sg.popup_ok(str(e))
    #
    # #evaluation of the thermoproperties button
    # if event == '||B_eval_tprops':
    #     try:
    #         events.tprops_enable_nexts(window)
    #
    #         TPs_calculated_dict = events.tprops_evaluate(window,minF_header,Volume_calculated,ndeb_dict,T)
    #     except Exception as e:
    #         sg.popup_ok(str(e))
    #
    # #parametrization of FS parameters button
    # if event == '||B_run_fs_params':
    #     try:
    #         fs_params_Cp_dict,fs_params_alpha_dict,fs_params_Ksinv_dict,fs_params_Ksp_dict,T_data,ix_Tfrom,ix_Tto,fs_params_H298_dict,fs_params_S298_dict = events.fs_params(window,minF_header,TPs_calculated_dict)
    #         for K in EOS_str_lst:
    #             try:
    #                 print(K,'%.10e' % tuple([fs_params_H298_dict[K]]),
    #                         '%.10e' % tuple([fs_params_S298_dict[K]]),
    #                         ' '.join(['%.10e' for _ in fs_params_Cp_dict[K]]) % tuple(fs_params_Cp_dict[K]),
    #                         ' '.join(['%.10e' for _ in fs_params_alpha_dict[K]]) % tuple(fs_params_alpha_dict[K]),
    #                         ' '.join(['%.10e' for _ in fs_params_Ksinv_dict[K]]) % tuple(fs_params_Ksinv_dict[K]),
    #                         ' '.join(['%.10e' for _ in fs_params_Ksp_dict[K]]) % tuple(fs_params_Ksp_dict[K]))
    #             except:
    #                 print(K,';;;')
    #     except Exception as e:
    #         sg.popup_ok(str(e))
    #
    # #plot V(T)
    # if event == '||B_plotter':
    #     events.plot_VvT(window)
    #
    # #plot TProps
    # if event == '||B_plotter_tprops':
    #     events.plot_tprops(window,minF_header)
    #
    # #plot FS TProps1
    # if '||B_plotter_fsprop2plt' in event:
    #     events.plot_fsprops(window,event,fs_params_Cp_dict,fs_params_alpha_dict,fs_params_Ksinv_dict,fs_params_Ksp_dict,T_data,ix_Tfrom,ix_Tto,TPs_calculated_dict)
    #
    # #open fittingToolEOS button
    #     initial_compound_path = window['--I_compound'].get()
    #     if initial_compound_path == '':
    #         sg.popup_ok('Please select a compound/element.')
    #         continue
    #     events.open_fittin_tool(window, opened_EOS_dict, initial_compound_path, contcar_str)
    #
    # if event == 'details...::nu':
    #     if nu_bool==False:
    #         sg.popup('First, calculate nu.')
    #     else:
    #         sg.popup(txt_out,title='details...',font=('Courier',8))
    #
    # #update enabled/disabled boxes and buttons
    checked_EOS_dict = events.update_diabled(window,opened_EOS_dict,EOS_str_lst,checked_EOS_dict)
