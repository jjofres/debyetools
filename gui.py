#### imports
import PySimpleGUI as sg
from debyetools.tpropsgui.layout import layout
import debyetools.tpropsgui.events as events
# from dependencies.ifgui.layout import layout
# import dependencies.ifgui.events as events
import debyetools.tpropsgui.toolbox as tbox
# from scipy.optimize import fmin, curve_fit

EOS_long_lst = {'Morse':'MP','Birch-Murnaghan (3)':'BM','Rose-Vinet':'RV','Mie-Gruneisen':'MG','TB-SMA':'TB','Murnaghan (1)':'MU','Poirier-Tarantola':'PT','Birch-Murnaghan (4)':'BM4','Murnaghan (2)':'MU2','EAM':'EAM',
                }#'*Morse':'MP','*Birch-Murnaghan (3)':'*BM','*Rose-Vinet':'*RV','*Mie-Gruneisen':'*MG','*TB-SMA':'*TB','*Murnaghan (1)':'*MU','*Poirier-Tarantola':'*PT','*Birch-Murnaghan (4)':'*BM4','*Murnaghan (2)':'*MU2','*EAM':'*EAM'}
EOS_str_lst = ['MP','BM','RV','MG','TB','MU','PT','BM4','MU2','EAM']#,'*MP','*BM','*RV','*MG','*TB','*MU','*PT','*BM4','*MU2','*EAM']
contcar_str = '/CONTCAR.5'
opened_dict = {str_i:False for str_i in EOS_str_lst}#{'MP':False,'BM':False,'RV':False,'MG':False,'TB':False,'MU':False,'BM3':False}
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
while True:
    event, values = window.read()

    # #close window
    if event in (sg.WIN_CLOSED, '--B_close'):
        break
    #
    # #file browser
    if event == '--I_FILEBROWSE_':
        # try:
            # opened_dict = events.fbrowser_resets(window, opened_dict)
        str_folderbrowser = events.fbrowser_fill_browser(window, event)
        events.fbrowser_update_fields(window, contcar_str, mws_dict, str_folderbrowser)
    #     except Exception as e:
    #         sg.popup_ok(str(e))
    # # #EOS Checkbox
    # if '--LBx_EOS_listbox' in event:#'--Chk_eos_' in event:
    #     print(window[event].get())
    #     #
    if event == '||B_add_EOS':
        for k in opened_dict.keys():
            opened_dict[k]=False
        for k in window['--LBx_EOS_listbox'].get():
            opened_dict[EOS_long_lst[k]]=True
        print(opened_dict)

        events.chk_eos(window,opened_dict)
    #
    # #EOS calculation Checkbox
    # if '--Chk_calc_params_' in event:
    #     events.chk_calc_params(window,event)
    #
    # #EOS fitting button
    # if event == '||B_run_eos_fitting':
    #     try:
    #         initial_compound_path = window['--I_compound'].get()
    #         if initial_compound_path == '':
    #             sg.popup_ok('Please select a compound/element.')
    #             continue
    #         params_dict = events.eos_fitting(window,opened_dict,initial_compound_path,contcar_str,params_dict)
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
    #         minF_header,Volume_calculated,ndeb_dict = events.minF_run_minimization(window,T,nu, r, m,Tf,contcar_str,EOS_str_lst,opened_dict)
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
    # if event == 'open fitting tool::fittingToolEOS':
    #     initial_compound_path = window['--I_compound'].get()
    #     if initial_compound_path == '':
    #         sg.popup_ok('Please select a compound/element.')
    #         continue
    #     events.open_fittin_tool(window, opened_dict, initial_compound_path, contcar_str)
    #
    # if event == 'details...::nu':
    #     if nu_bool==False:
    #         sg.popup('First, calculate nu.')
    #     else:
    #         sg.popup(txt_out,title='details...',font=('Courier',8))
    #
    # #update enabled/disabled boxes and buttons
    events.update_diabled(window,opened_dict,EOS_str_lst)
