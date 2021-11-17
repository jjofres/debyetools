# import re
import numpy as np
import debyetools.tpropsgui.toolbox as tbox
# import dependencies.eos_fitting_tools as eos_fitting_tools
# import dependencies.thermo.poisson as poisson
# import dependencies.thermo.load_ins as load_ins
# import dependencies.thermo.electronic as electronic
# from dependencies.thermo.nDeb import gen_Ts
# from dependencies.thermo import potentials as pots
# from scipy.optimize import fmin, curve_fit
# from dependencies.thermo.nDeb import nDeb as nDeb
# import dependencies.thermo.anharmonicity as anharmonicity
# import dependencies.thermo.electronic as electronic
# import dependencies.thermo.defects as defects
import debyetools.tpropsgui.plotter as plot
from debyetools.fs_compound_db import Cp2fit, alpha2fit, Ksinv2fit, Ksp2fit
# import dependencies.thermo.pair_analysis as pair_analysis
#
# Cp2fit = lambda T, P0, P1, P2, P3, P4, P5: P0*T**0 + P1*T**1 + P2*T**(-2) + P3*T**2 + P4*T**(-.5) + P5*T**(-3)
# alpha2fit = lambda T, Q0, Q1, Q2, Q3: Q0*T**0 + Q1*T**1 + Q2*T**(-1) + Q3*T**(-2)
# Ksinv2fit = lambda T, R0, R1, R2, R3: R0*T**0 + R1*T**1 + R2*T**2 + R3*T**3
# Ksp2fit = lambda T, S0, S1: S0 + S1*(T-298.15)*np.log(T/298.15)
#
def fbrowser_fill_browser(window,event):
    str_I_compound = window['--I_compound'].get()
    str_folderbrowser = window[event].get()
    if str_folderbrowser == '': str_folderbrowser = str_I_compound

    window['--I_compound'].update(str_folderbrowser)
    window['--I_compound'].update(move_cursor_to='end')
    return str_folderbrowser
#
# def fbrowser_fill_browser_bulk(window,event):
#     str_I_compound = window['--I_folder_bulk'].get()
#     str_folderbrowser = window[event].get()
#     if str_folderbrowser == '': str_folderbrowser = str_I_compound
#
#     window['--I_folder_bulk'].update(str_folderbrowser)
#     window['--I_folder_bulk'].update(move_cursor_to='end')
#     return str_folderbrowser
#
def fbrowser_update_fields(window,contcar_str,mws_dict,str_folderbrowser):

    with open(window['--I_compound'].get() +contcar_str) as f:
        lines = f.readlines()
    els_lst = lines[5].split()
    nats_lst = [int(i) for i in lines[6].split()]
    nat = np.sum(nats_lst)

    mass = 0
    for ei, ni in zip(els_lst, nats_lst):
        mass+=mws_dict[ei]*ni

    nats_lst_int = [int(i) for i in np.array(nats_lst)/tbox.compute_gcd(nats_lst)]

    window['--I_formula'].update(''.join(['%s%s' for i in els_lst])%tuple(np.reshape(list(zip(els_lst, nats_lst_int)),len(nats_lst)*2)))
    window['--I_mass'].update(mass/nat)
    window['--I_strkt'].update(str_folderbrowser.split('_')[-1])
    window['--I_p_el'].update('0, 0, 0, 0')
    window['--I_p_intanh'].update('0, 1')
    window['--I_p_anhxc'].update('0, 0, 0')
    window['--I_p_evac'].update('8')
    window['--I_p_svac'].update('2')
    window['--I_Ti'].update('0.1')
    window['--I_Tm'].update('1000')
    window['--I_Tf'].update(window['--I_Tm'].get())
    window['--I_ntemps'].update(20)
    window['--I_Tm'].update(disabled=False)
    window['--I_mass'].update(disabled=False)
#
# def reset_I(window):
#     for k in window.key_dict:
#         if '--I_' in str(k):
#             if 'FILEBROWSE_' not in str(k):
#                 window[k].update('')
#                 window[k].update(disabled=True)
#         else:
#             pass
#
# def reset_M(window):
#     for k in window.key_dict:
#         if '--M_' in str(k):
#             window[k].update('')
#         else:
#             pass
# def reset_Chk_eos(window,opened_dict):
#     for k in window.key_dict:
#         if '--Chk_eos_' in str(k):
#             window[k].update(False)
#             window['||Col_options_'+k.split('_')[-1]].update(visible=False)
#             opened_dict[k.split('_')[-1]]=False
#         else:
#             pass
#
#     return opened_dict
# def reset_Chk_poisson(window):
#     for k in window.key_dict:
#         if '--Chk_el' in str(k):
#             window[k].update(False)
#         else:
#             pass
# def reset_Chk_defs(window):
#     for k in window.key_dict:
#         if '--Chk_def' in str(k):
#             window[k].update(False)
#         else:
#             pass
# def reset_Chk_intanh(window):
#     for k in window.key_dict:
#         if '--Chk_intanh' in str(k):
#             window[k].update(False)
#         else:
#             pass
# def reset_Chk_anhxc(window):
#     for k in window.key_dict:
#         if '--Chk_anhxc' in str(k):
#             window[k].update(False)
#         else:
#             pass
#
# def reset_T(window):
#     for k in window.key_dict:
#         if '--Tab_' in str(k):
#             window[k].update(visible=False)
#             if str(k)[-1]=='_':
#                 window[k].update(visible=True)
#                 window[k].select()
#
# def fbrowser_resets(window,opened_dict):
#     reset_I(window)
#     reset_M(window)
#     opened_dict = reset_Chk_eos(window,opened_dict)
#     reset_Chk_poisson(window)
#     reset_Chk_defs(window)
#     reset_Chk_intanh(window)
#     reset_Chk_anhxc(window)
#     reset_T(window)
#     window['||F_fsparams'].update('FactSage Parameters')
#
#     window['||B_run_fs_params'].update(disabled=True)
#     window['||B_eval_tprops'].update(disabled=True)
#     window['||B_plotter'].update(disabled=True)
#     window['--I_cutoff'].update(5.0)
#     window['--I_ndists'].update(6)
#     window['--I_r'].update(1)
#
#     return opened_dict
#
def chk_eos(window,opened_dict):
    for k in opened_dict.keys():
        window['||Col_options_'+k].update(visible=opened_dict[k])
#
def chk_calc_params(window,event):
    eos_str = event.split('_')[-1]
    window['--I_params_'+eos_str].update(disabled= bool(window[event].get()))
#
def bool_chks(window,opened_dict):
    bool_dict_params_EOS = {stri:window['--Chk_calc_params_'+stri].get() for stri in opened_dict.keys()}
    bool_dict_EOS =  {stri:opened_dict[stri] for stri in opened_dict.keys()}
    bool_run_eos_fitting = any([all([bool_dict_params_EOS[stri],bool_dict_EOS[stri]]) for stri in opened_dict.keys()])

    return bool_run_eos_fitting, bool_dict_params_EOS
#
def update_diabled(window,opened_dict,eos_available,bool_dict_params_EOS):
    bool_run_eos_fitting, bool_dict_params_EOS = bool_chks(window,opened_dict)
    window['||B_run_eos_fitting'].update(disabled=not bool_run_eos_fitting)

    bool_minF = bool_run_eos_fitting and (True if window['--I_nu'].get()!='' else False)

    window['||B_run_minF'].update(disabled=not bool_minF)

    window['--I_nu'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['||B_calc_nu'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--Chk_el'].update(disabled=True if window['--I_compound'].get()=='' else False)


    for str_eos in eos_available:
        window['||B_plotter_fsprop2plt'+str_eos].update(disabled=True if window['--IC_fsprop2plt'+str_eos].get()== '' else False)

    window['--Chk_def'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--Chk_intanh'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--Chk_anhxc'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--I_Ti'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--I_Tf'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--I_Tm'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--I_ntemps'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['||B_plotter_tprops'].update(disabled=True if window['--IC_prop2plt'].get()== '' else False)
    window['--I_cutoff_MP'].update(disabled=False)
    window['--I_ndists_MP'].update(disabled=False)

    return bool_dict_params_EOS
#
# def eos_fitting(window,opened_dict,initial_compound_path,contcar_str,params_dict):
#     initial_chk_selections ={eos_str:bool(opened_dict[eos_str]*window['--Chk_calc_params_'+eos_str].get()) for eos_str in opened_dict.keys()}
#     intial_cuttof_ndist = window['--I_cutoff'].get(), window['--I_ndists'].get()
#
#     for eos_str in opened_dict.keys():
#         if window['--Chk_calc_params_'+eos_str].get() and opened_dict[eos_str]:
#
#             rslts = eos_fitting_tools.run_minimization(initial_compound_path,[-3e5, 2e-5, 7e10, 4,1e-10],
#                                                                        initial_compound_path+contcar_str, eos_str.replace('*',''), units='J/mol',
#                                                                        cutoff=float(intial_cuttof_ndist[0]),
#                                                                        number_of_neighbor_levels=int(intial_cuttof_ndist[1]))
#
#             if eos_str in ['MP','EAM']:
#                 params, nl,    pa, comb_types, Edata,VDFT,Emodel = rslts
#             else:
#                 params, Edata,VDFT,Emodel = rslts
#             params_dict[eos_str]=params
#
#     return params_dict
#
def eos_write_params(window,EOSStr,pEOS):
        window['--I_params_'+EOSStr].update(', '.join(['%.9e' for i in pEOS])%tuple(pEOS))
##
def chk_el(window,event):
    window['--I_p_el'].update(disabled= not bool(window[event].get()))
    window['||B_calc_el'].update(disabled= not bool(window[event].get()))
#
def chk_def(window,event):
    window['--I_p_evac'].update(disabled= not bool(window[event].get()))
    window['--I_p_svac'].update(disabled= not bool(window[event].get()))
##
def chk_intanh(window,event):
    window['--I_p_intanh'].update(disabled= not bool(window[event].get()))
def chk_anhxc(window,event):
    window['--I_p_anhxc'].update(disabled= not bool(window[event].get()))
#
def minF_enable_nexts(window):
    window['||B_plotter'].update(disabled=False)
    window['||B_eval_tprops'].update(disabled=False)
#
# def minF_get_ins(window):
#     nu = float(window['--I_nu'].get())
#     r = float(window['--I_r'].get())
#     m = float(window['--I_mass'].get())
#     Ti = float(window['--I_Ti'].get())
#     Tf = float(window['--I_Tf'].get())
#
#     return Ti,Tf, nu, r,m
#
# def minF_generate_Temps(window,Ti,Tf):
#     nTemps  = float(window['--I_ntemps'].get())
#     T = gen_Ts(Ti,Tf,nTemps)
#
#     return T
#
# def minF_run_minimization(window,T,nu, r, m,Tf,contcar_str,eos_available,opened_dict):
#     Tm = float(window['--I_Tm'].get())
#     minF_arr = np.array([T]).T
#     minF_header = ['#T']
#     Volume_calculated={}
#     ndeb_dict = {}
#
#     for eos_str in eos_available:
#
#         if opened_dict[eos_str]==True:
#             print(eos_str+':')
#             eos_str2=eos_str.replace('*','')
#             minF_header.append(eos_str)
#             if eos_str2 in ['MP', 'EAM']:
#                 print('xxx',window['--I_compound'].get() +contcar_str)
#                 formula,    primitive_cell,    basis_vectors    = pair_analysis.ReadPOSCAR(window['--I_compound'].get() +contcar_str)
#
#                 Vstar = np.linalg.det(primitive_cell)/len(basis_vectors)
#                 cutoff = float(window['--I_cutoff'].get())#Vstar**(1/3)*4
#                 number_of_neighbor_levels = int(window['--I_ndists'].get())
#                 eos_obj = getattr(pots,eos_str2)(window['--I_compound'].get() +contcar_str,cutoff,number_of_neighbor_levels,units = 'J/mol')
#             else:
#                 eos_obj = getattr(pots,eos_str2)()
#
#             if eos_str2=='EAM':
#                 pEOS_pt , pEOS_et = eos_obj.paramos_raw_2_pt_et(np.array([float(str_p) for str_p in window['--I_params_'+eos_str].get().replace(',',' ').split()]))
#
#                 eos_obj.params_pair_type(pEOS_pt)
#                 eos_obj.params_elmt_type(pEOS_et)
#             else:
#                 eos_obj.pEOS = np.array([float(str_p) for str_p in window['--I_params_'+eos_str].get().replace(',',' ').split()])
#
#             f2min = lambda V:eos_obj.E0(V)
#             V0 = fmin(f2min,1e-5,disp=False)[0]
#             E0 = f2min(V0)
#
#             ndeb_dict[eos_str] = nDeb(nu, r, m)
#             ndeb_dict[eos_str].EOS = eos_obj
#             ndeb_dict[eos_str].V_0,ndeb_dict[eos_str].E_0 = V0,E0
#             s0,s1,s2 = [float(i) for i in window['--I_p_anhxc'].get().replace(',',' ').split()] if bool(window['--Chk_anhxc'].get()) else [0,0,0]
#             ndeb_dict[eos_str].anh = anharmonicity.Anharmonicity(s0,s1,s2)
#             a0,m0 = [float(i) for i in window['--I_p_intanh'].get().replace(',',' ').split()] if bool(window['--Chk_intanh'].get()) else [0,1]
#             ndeb_dict[eos_str].intanh = anharmonicity.intAnharmonicity(a0,m0,V0)
#             q0,q1,q2,q3 = [float(i) for i in window['--I_p_el'].get().replace(',',' ').split()] if bool(window['--Chk_el'].get()) else [0,0,0,0]
#             ndeb_dict[eos_str].el = electronic.Electronic(r,q0,q1,q2,q3)
#             p_evac, p_svac = [float(window['--I_p_evac'].get()),float(window['--I_p_svac'].get())] if bool(window['--Chk_def'].get()) else [1e10, 0.]
#
#             if eos_str2 in ['MP','EAM']:
#                 P2 = 1e10
#             else:
#                 P2 = ndeb_dict[eos_str].EOS.pEOS[2]
#             ndeb_dict[eos_str].deff = defects.Defects(p_evac, p_svac,Tm,0.1,P2,V0)
#
#             Tvol,Volume_calculated[eos_str] = ndeb_dict[eos_str].Volume(T)
#
#             for i in range(np.size(T)-np.size(Volume_calculated[eos_str])):
#                 Volume_calculated[eos_str]=np.append(Volume_calculated[eos_str],np.array([np.nan]))
#
#             minF_arr = np.c_[minF_arr,np.array(Volume_calculated[eos_str]).T]
#
#         else:
#             pass
#
#     txt_minF_output = '          '.join(minF_header) + '\n'
#     for i in minF_arr:
#         txt_minF_output = txt_minF_output + ' '.join(['%.9e' for ii in i])%tuple(i) + '\n'
#     window['--M_minF_output'].update(txt_minF_output)
#
#     return minF_header,Volume_calculated,ndeb_dict
#
def tprops_enable_nexts(window):
    window['||B_run_fs_params'].update(disabled=False)
    window['--I_fs_Tfrom'].update('298.15')
    window['--I_fs_Tto'].update(window['--I_Tf'].get())
    window['--I_fs_Tfrom'].update(disabled=False)
    window['--I_fs_Tto'].update(disabled=False)
    window['--Tab_'].update(visible=False)
#
# def tprops_evaluate(window,minF_header,Volume_calculated,ndeb_dict,T):
#     TPs_calculated_dict={}
#
#     print('xxxxx',minF_header)
#     for ix, k in enumerate(minF_header[1:]):
#         print(k+':')
#
#         window['--Tab_'+k].update(visible=True)
#         window['--Tab_'+k].select()
#         print('--Tab_'+k)
#         print(window.Element('--TG_tabs_tprops').find_key_from_tab_name('--Tab_'+k))#.SetTitle(ix,k)
#         inx = np.where(np.invert(np.isnan(Volume_calculated[k])))[0]
#         TPs_calculated = ndeb_dict[k].Cp(T[inx],Volume_calculated[k][inx])
#         TPs_calculated_dict[str(k)]=TPs_calculated
#         keys_TPs = TPs_calculated.keys()
#         tprops_str = '#T          '+' '.join([(j+'            ')[:11] for j in list(keys_TPs)[1:]])+'\n'
#         TPs_arr = np.c_[tuple([TPs_calculated[j] for j in keys_TPs])]
#         for rowi in TPs_arr:
#             tprops_str = tprops_str + ' '.join(['%.11e' for i in rowi])%tuple(rowi)+'\n'
#         window['--M_tprop_'+k].update(tprops_str)
#
#         window['--IC_prop2plt'].update(values=list(keys_TPs)[1:])
#
#     return TPs_calculated_dict
#
# def fs_params(window,minF_header,TPs_calculated_dict):
#     fs_params_Cp_dict = {}
#     fs_params_alpha_dict = {}
#     fs_params_Ksinv_dict = {}
#     fs_params_Ksp_dict = {}
#     fs_params_H298_dict={}
#     fs_params_S298_dict={}
#
#     window['--Tab_fs_'].update(visible=False)
#
#     for ix, k in enumerate(minF_header[1:]):
#
#         TPs_calculated = TPs_calculated_dict[str(k)]
#         window['--Tab_fs_'+k].update(visible=True)
#         window['--Tab_fs_'+k].select()
#
#         T_data = TPs_calculated['T']
#
#         if float(window['--I_fs_Tfrom'].get())<298.15:
#             window['--I_fs_Tfrom'].update(298.15)
#
#         if float(window['--I_fs_Tto'].get())>T_data[-1]:
#             window['--I_fs_Tto'].update(T_data[-1])
#
#         T_from = float(window['--I_fs_Tfrom'].get())
#         T_to = float(window['--I_fs_Tto'].get())
#         ix_Tfrom = np.where(T_data <= T_from)[0][-1]
#         ix_Tto = np.where(T_data >= T_to)[0][0]
#
#         ix_T0 = np.where(T_data == 298.15)[0][0]
#
#         ix_T1 = np.where(T_data >= max(T_data))[0][0]
#         Cp_data = TPs_calculated['Cp']
#         alpha_data = TPs_calculated['a']
#         Ks_data = TPs_calculated['Ks']
#         Ksp_data = TPs_calculated['Ksp']
#
#         H298 = TPs_calculated['F'][ix_T0]+T_data[ix_T0]*TPs_calculated['S'][ix_T0]
#         S298 = TPs_calculated['S'][ix_T0]
#
#         window['--I_H298'+k].update(disabled=False)
#         window['--I_H298'+k].update(H298)
#         window['--I_S298'+k].update(disabled=False)
#         window['--I_S298'+k].update(S298)
#
#
#         fs_params_Cp , c = curve_fit(Cp2fit, T_data[ix_Tfrom:ix_Tto+1], Cp_data[ix_Tfrom:ix_Tto+1])
#         fs_params_alpha , c = curve_fit(alpha2fit, T_data[ix_Tfrom:ix_Tto+1], alpha_data[ix_Tfrom:ix_Tto+1])
#         fs_params_Ksinv , c = curve_fit(Ksinv2fit, T_data[ix_Tfrom:ix_Tto+1], [1/ksi for ksi in Ks_data[ix_Tfrom:ix_Tto+1]])
#         fs_params_Ksp , c = curve_fit(Ksp2fit, T_data[ix_Tfrom:ix_Tto+1], Ksp_data[ix_Tfrom:ix_Tto+1])
#
#         for i in range(len(fs_params_Cp)):
#             window['--I_fsCp_P'+str(i)+k].update(disabled=False)
#             window['--I_fsCp_P'+str(i)+k].update('%.4e'%(fs_params_Cp[i]))
#         for i in range(len(fs_params_alpha)):
#             window['--I_fsa_P'+str(i)+k].update(disabled=False)
#             window['--I_fsa_P'+str(i)+k].update('%.4e'%(fs_params_alpha[i]))
#         for i in range(len(fs_params_Ksinv)):
#             window['--I_fsK_P'+str(i)+k].update(disabled=False)
#             window['--I_fsK_P'+str(i)+k].update('%.4e'%(fs_params_Ksinv[i]))
#         for i in range(len(fs_params_Ksp)):
#             window['--I_fsKp_P'+str(i)+k].update(disabled=False)
#             window['--I_fsKp_P'+str(i)+k].update('%.4e'%(fs_params_Ksp[i]))
#         fs_params_Cp_dict[str(k)]=fs_params_Cp
#         fs_params_alpha_dict[str(k)]=fs_params_alpha
#         fs_params_Ksinv_dict[str(k)]=fs_params_Ksinv
#         fs_params_Ksp_dict[str(k)]=fs_params_Ksp
#
#         fs_params_H298_dict[str(k)]=H298
#         fs_params_S298_dict[str(k)]=S298
#
#     return fs_params_Cp_dict,fs_params_alpha_dict,fs_params_Ksinv_dict,fs_params_Ksp_dict,T_data,ix_Tfrom,ix_Tto,fs_params_H298_dict,fs_params_S298_dict
def plot_EvV(window, eosobj_dict, opened_EOS_dict):
    pots_str_lst = [k for k in opened_EOS_dict if opened_EOS_dict[k]]
    print(pots_str_lst)
    V_DFT = eosobj_dict['V_DFT']
    E_DFT = eosobj_dict['E_DFT']
    tab3_str='#V          DFT         '+'          '.join(['%s' for i in pots_str_lst])%tuple(pots_str_lst)+'\n'
    for Vi, Ei in zip(V_DFT, E_DFT):
        Emi = [eosobj_dict[k].E0(Vi) for k in pots_str_lst]
        tab3_str= tab3_str + '%.10e   %.10e  '%(Vi,Ei) + '  '.join(['%.10e' for i in Emi])%tuple(Emi)+'\n'
    print(tab3_str)
    initial_tabs_multilinetxt = {'t0':{'multiline':tab3_str}}
    initial_lines_settings = {
                              'l0':{'plot':True,'label':0,'linestyle':'None','color':'mediumpurple','marker':'o',   'markerfacecolor':'black', 'markeredgecolor':'mediumpurple','linewidth':2,'markersize':10},
                              'l1':{'plot':True,'label':0,'linestyle':'None','color':'purple', 'marker':'+',   'markerfacecolor':'None', 'markeredgecolor':'deepskyblue','linewidth':2,'markersize':10},
                              'l2':{'plot':True,'label':0,'linestyle':'None','color':'gray',        'marker':'x',   'markerfacecolor':'None', 'markeredgecolor':'aqua','linewidth':2,'markersize':10},
                              'l3':{'plot':True,'label':0,'linestyle':'None','color':'orchid',        'marker':'s',   'markerfacecolor':'None', 'markeredgecolor':'gray','linewidth':2,'markersize':10},
                              'l4':{'plot':True,'label':0,'linestyle':'None','color':'deepskyblue',          'marker':'^',   'markerfacecolor':'None', 'markeredgecolor':'C0','linewidth':2,'markersize':10},
                              'l5':{'plot':True,'label':0,'linestyle':'None','color':'pink',          'marker':'>',   'markerfacecolor':'None', 'markeredgecolor':'C3','linewidth':2,'markersize':10},
                              'l6':{'plot':True,'label':0,'linestyle':'None','color':'aqua',      'marker':'1',   'markerfacecolor':'None', 'markeredgecolor':'orange','linewidth':2,'markersize':10},
                              'l7':{'plot':True,'label':0,'linestyle':'None','color':'cornflowerblue',        'marker':'<','markerfacecolor':'None', 'markeredgecolor':'None','linewidth':2,'markersize':10},
                              'l8':{'plot':True,'label':0,'linestyle':'None','color':'C0',        'marker':'2','markerfacecolor':'None', 'markeredgecolor':'None','linewidth':2,'markersize':10},
                              }
    initial_fig_settings = {'figwidth':5.5,'figheight':4.5,'use_title':False,'title':'','titlexpos':.7,'titleypos':.9,
                            'titlesize':12,'use_xlabel':True,'use_ylabel':True,'xlabel':'Volume $\left[m^3/mol-at\\right]$','ylabel':'$E~\left[J/mol-at\\right]$','labelxsize':13,
                            'labelysize':13,'auto_xlim':True,'auto_ylim':True,'limxmin':-0.5,'limxmax':110,'limymin':-1,'limymax':2,'use_legend':True,'legend_loc':'best',
                            'legendncol':2,'legendfontsize':14,'use_grid':True,'lmargin':0.2,'rmargin':0.98,'tmargin':0.95,'bmargin':0.12}

    plot.pop_window_simple(initial_tabs_multilinetxt,initial_lines_settings,initial_fig_settings)


def plot_VvT(window):
    initial_tabs_multilinetxt = {'t0':{'multiline':window['--M_minF_output'].get()}}
    initial_lines_settings = {
                              'l0':{'plot':True,'label':0,'linestyle':'-','color':'mediumpurple','marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'mediumpurple','linewidth':2,'markersize':10},
                              'l1':{'plot':True,'label':0,'linestyle':'-','color':'purple', 'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'deepskyblue','linewidth':2,'markersize':10},
                              'l2':{'plot':True,'label':0,'linestyle':'-','color':'gray',        'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'aqua','linewidth':2,'markersize':10},
                              'l3':{'plot':True,'label':0,'linestyle':'-','color':'orchid',        'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'gray','linewidth':2,'markersize':10},
                              'l4':{'plot':True,'label':0,'linestyle':'-','color':'deepskyblue',          'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'C0','linewidth':2,'markersize':10},
                              'l5':{'plot':True,'label':0,'linestyle':'-','color':'pink',          'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'C3','linewidth':2,'markersize':10},
                              'l6':{'plot':True,'label':0,'linestyle':'-','color':'aqua',      'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'orange','linewidth':2,'markersize':10},
                              'l7':{'plot':True,'label':0,'linestyle':'-','color':'cornflowerblue',        'marker':'None','markerfacecolor':'None', 'markeredgecolor':'None','linewidth':2,'markersize':10},
                              'l8':{'plot':True,'label':0,'linestyle':'-','color':'C0',        'marker':'None','markerfacecolor':'None', 'markeredgecolor':'None','linewidth':2,'markersize':10},
                              }

    initial_fig_settings = {'figwidth':5.5,'figheight':4.5,'use_title':False,'title':'','titlexpos':.7,'titleypos':.9,
                            'titlesize':12,'use_xlabel':True,'use_ylabel':True,'xlabel':'T $\left[K\\right]$','ylabel':'$V~\left[m^3/atom\\right]$','labelxsize':13,
                            'labelysize':13,'auto_xlim':True,'auto_ylim':True,'limxmin':-0.5,'limxmax':110,'limymin':-1,'limymax':2,'use_legend':True,'legend_loc':'best',
                            'legendncol':2,'legendfontsize':14,'use_grid':True,'lmargin':0.14,'rmargin':0.98,'tmargin':0.95,'bmargin':0.12}

    plot.pop_window_simple(initial_tabs_multilinetxt,initial_lines_settings,initial_fig_settings)
#
def plot_tprops(window,minF_header):
    initial_tabs_multilinetxt = {'t0':{'multiline':[]}}
    for ix, k in enumerate(minF_header):
        window['--M_tprop_'+str(k)].get()
        datas_dict = tbox.txt2dict(window['--M_tprop_'+str(k)].get())
        txt2M = '#T    '+k+'\n'
        for valsi in np.c_[datas_dict['T'].T,datas_dict[window['--IC_prop2plt'].get()].T]:
            txt2M = txt2M + '%.9e %.9e'%tuple(valsi)+'\n'
        initial_tabs_multilinetxt['t'+str(ix)]={'multiline':txt2M}

    initial_lines_settings = {
                              'l0':{'plot':True,'label':0,'linestyle':'-','color':'mediumpurple','marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'mediumpurple','linewidth':2,'markersize':10},
                              'l1':{'plot':True,'label':0,'linestyle':'-','color':'purple', 'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'deepskyblue','linewidth':2,'markersize':10},
                              'l2':{'plot':True,'label':0,'linestyle':'-','color':'gray',        'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'aqua','linewidth':2,'markersize':10},
                              'l3':{'plot':True,'label':0,'linestyle':'-','color':'orchid',        'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'gray','linewidth':2,'markersize':10},
                              'l4':{'plot':True,'label':0,'linestyle':'-','color':'deepskyblue',          'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'C0','linewidth':2,'markersize':10},
                              'l5':{'plot':True,'label':0,'linestyle':'-','color':'pink',          'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'C3','linewidth':2,'markersize':10},
                              'l6':{'plot':True,'label':0,'linestyle':'-','color':'aqua',      'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'orange','linewidth':2,'markersize':10},
                              'l7':{'plot':True,'label':0,'linestyle':'-','color':'cornflowerblue',        'marker':'None','markerfacecolor':'None', 'markeredgecolor':'None','linewidth':2,'markersize':10},
                              'l8':{'plot':True,'label':0,'linestyle':'-','color':'C0',        'marker':'None','markerfacecolor':'None', 'markeredgecolor':'None','linewidth':2,'markersize':10},
                              }
    initial_fig_settings = {'figwidth':5.5,'figheight':4.5,'use_title':False,'title':'','titlexpos':.7,'titleypos':.9,
                            'titlesize':12,'use_xlabel':True,'use_ylabel':True,'xlabel':'T $\left[K\\right]$','ylabel':window['--IC_prop2plt'].get(),'labelxsize':13,
                            'labelysize':13,'auto_xlim':True,'auto_ylim':True,'limxmin':-0.5,'limxmax':110,'limymin':-1,'limymax':2,'use_legend':True,'legend_loc':'best',
                            'legendncol':2,'legendfontsize':14,'use_grid':True,'lmargin':0.14,'rmargin':0.98,'tmargin':0.95,'bmargin':0.12}
    plot.pop_window_simple(initial_tabs_multilinetxt,initial_lines_settings,initial_fig_settings)
#
def plot_fsprops(window,event,fs_params,Tfrom,Tto,TPs_calculated_dict):
    str_eos = event.replace('||B_plotter_fsprop2plt','')
    fs_params_Cp = fs_params[str_eos]['Cp']
    fs_params_alpha = fs_params[str_eos]['a']
    fs_params_Ksinv = fs_params[str_eos]['1/Ks']
    fs_params_Ksp = fs_params[str_eos]['Ksp']
    T_data = TPs_calculated_dict[str_eos]['T']
    ix_Tfrom = np.where(np.round(TPs_calculated_dict[str_eos]['T'],2) == np.round(Tfrom,2))[0][0]
    ix_Tto = np.where(np.round(TPs_calculated_dict[str_eos]['T'],2) == np.round(Tto,2))[0][0]
    if window['--IC_fsprop2plt'+str_eos].get()=='Cp':
        prop2plt = [Cp2fit(Ti,fs_params_Cp[0],fs_params_Cp[1],fs_params_Cp[2],fs_params_Cp[3],fs_params_Cp[4],fs_params_Cp[5]) for Ti in T_data[ix_Tfrom:ix_Tto+1]]
        prop_data = TPs_calculated_dict[str_eos]['Cp']
        txt1 = '#T $C_P=P_0T^0+P_1T^1+P_2T^{-2}+P_3T^2+P_4T^{-.5}+P_5T^{-3}$\n'
        txt2 = '#T $C_P$\n'
    if window['--IC_fsprop2plt'+str_eos].get()=='alpha':
        prop2plt = [alpha2fit(Ti,fs_params_alpha[0],fs_params_alpha[1],fs_params_alpha[2],fs_params_alpha[3]) for Ti in T_data[ix_Tfrom:ix_Tto+1]]
        prop_data = TPs_calculated_dict[str_eos]['a']
        txt1 = '#T $alpha=Q_0T^0+Q_1T^1+Q_2T^{-1}+Q_3T^{-2}$\n'
        txt2 = '#T $alpha$\n'
    if window['--IC_fsprop2plt'+str_eos].get()=='1/K':
        prop2plt = [Ksinv2fit(Ti,fs_params_Ksinv[0],fs_params_Ksinv[1],fs_params_Ksinv[2],fs_params_Ksinv[3]) for Ti in T_data[ix_Tfrom:ix_Tto+1]]
        prop_data = [1/ks for ks in TPs_calculated_dict[str_eos]['Ks']]
        txt1 = '#T $1/Ks=R_0T^0+R_1T^1+R_2T^2+R_3T^3$\n'
        txt2 = '#T $1/Ks$\n'
    if window['--IC_fsprop2plt'+str_eos].get()=='dK/dP':
        prop2plt = [Ksp2fit(Ti,fs_params_Ksp[0],fs_params_Ksp[1]) for Ti in T_data[ix_Tfrom:ix_Tto+1]]
        prop_data = TPs_calculated_dict[str_eos]['Ksp']
        txt1 = '#T $dK/dP=S_0+S_1\cdot(T-298.15K)\ln(T/298.15K)$\n'
        txt2 = '#T $dK/dP$\n'

    initial_tabs_multilinetxt = {'t0':{'multiline':[]}}
    for Cpi,Ti in zip(prop2plt, T_data[ix_Tfrom:ix_Tto+1]):
        txt1 = txt1 + '%.9e %.9e'%(Ti, Cpi)+'\n'
    initial_tabs_multilinetxt['t1']={'multiline':txt1}

    for Cpi,Ti in zip(prop_data, T_data):
        txt2 = txt2 + '%.9e %.9e'%(Ti, Cpi)+'\n'
    initial_tabs_multilinetxt['t0']={'multiline':txt2}
    initial_lines_settings = {
                              'l0':{'plot':True,'label':0,'linestyle':'-','color':'mediumpurple','marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'mediumpurple','linewidth':2,'markersize':10},
                              'l1':{'plot':True,'label':0,'linestyle':'-','color':'purple', 'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'deepskyblue','linewidth':2,'markersize':10},
                              'l2':{'plot':True,'label':0,'linestyle':'-','color':'gray',        'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'aqua','linewidth':2,'markersize':10},
                              'l3':{'plot':True,'label':0,'linestyle':'-','color':'orchid',        'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'gray','linewidth':2,'markersize':10},
                              'l4':{'plot':True,'label':0,'linestyle':'-','color':'deepskyblue',          'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'C0','linewidth':2,'markersize':10},
                              'l5':{'plot':True,'label':0,'linestyle':'-','color':'pink',          'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'C3','linewidth':2,'markersize':10},
                              'l6':{'plot':True,'label':0,'linestyle':'-','color':'aqua',      'marker':'None',   'markerfacecolor':'None', 'markeredgecolor':'orange','linewidth':2,'markersize':10},
                              'l7':{'plot':True,'label':0,'linestyle':'-','color':'cornflowerblue',        'marker':'None','markerfacecolor':'None', 'markeredgecolor':'None','linewidth':2,'markersize':10},
                              'l8':{'plot':True,'label':0,'linestyle':'-','color':'C0',        'marker':'None','markerfacecolor':'None', 'markeredgecolor':'None','linewidth':2,'markersize':10},
                              }
    initial_fig_settings = {'figwidth':5.5,'figheight':4.5,'use_title':False,'title':'','titlexpos':.7,'titleypos':.9,
                            'titlesize':12,'use_xlabel':True,'use_ylabel':True,'xlabel':'T $\left[K\\right]$','ylabel':window['--IC_prop2plt'].get(),'labelxsize':13,
                            'labelysize':13,'auto_xlim':True,'auto_ylim':True,'limxmin':-0.5,'limxmax':110,'limymin':-1,'limymax':2,'use_legend':True,'legend_loc':'best',
                            'legendncol':1,'legendfontsize':11,'use_grid':True,'lmargin':0.14,'rmargin':0.98,'tmargin':0.95,'bmargin':0.12}
    plot.pop_window_simple(initial_tabs_multilinetxt,initial_lines_settings,initial_fig_settings)
#
# def open_fittin_tool(window, opened_dict, initial_compound_path, contcar_str):
#
#     initial_chk_selections ={eos_str:bool(opened_dict[eos_str]*window['--Chk_calc_params_'+eos_str].get()) for eos_str in opened_dict.keys()}
#     intial_cuttof_ndist = window['--I_cutoff'].get(), window['--I_ndists'].get()
#
#     strok, VDFT = eos_fitting_tools.pop_window(initial_compound_path, contcar_str, initial_chk_selections, intial_cuttof_ndist,True)
