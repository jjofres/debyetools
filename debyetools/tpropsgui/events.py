# import re
import numpy as np
import debyetools.tpropsgui.toolbox as tbox
import debyetools.tpropsgui.plotter as plot
from debyetools.fs_compound_db import Cp2fit, alpha2fit, Ksinv2fit, Ksp2fit
#
def fbrowser_fill_browser(window,event):
    str_I_compound = window['--I_compound'].get()
    str_folderbrowser = window[event].get()
    if str_folderbrowser == '': str_folderbrowser = str_I_compound

    window['--I_compound'].update(str_folderbrowser)
    window['--I_compound'].update(move_cursor_to='end')
    return str_folderbrowser
#
def fbrowser_update_fields(window,window7,contcar_str,mws_dict,str_folderbrowser,opened_EOS_dict,EOS_long_lst,EOS_str_lst,checked_EOS_dict,bool_anh):

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
    window['--I_Tm'].update('1000')
    window['--I_Ti'].update('0.1')
    window['--I_Pi'].update('0')
    window['--I_Tf'].update(window['--I_Tm'].get())
    window['--I_ntemps'].update(10)
    window['--I_Tm'].update(disabled=False)
    window['--I_mass'].update(disabled=False)
    window['--M_minF_output'].update('')
    window['--LBx_EOS_listbox'].update(disabled=False)
    window['--LBx_EOS_listbox'].set_value([False for k in window['--LBx_EOS_listbox'].get()])
    add_EOS(window, opened_EOS_dict,EOS_long_lst)
    for eos in EOS_str_lst:
        window['--I_params_'+eos].update('0, 0, 0, 0')
    window['--I_nu'].update('')
    window['--I_p_el'].update('0, 0, 0, 0')
    window['--I_p_evac'].update('8')
    window['--I_p_svac'].update('2')
    window['--I_Tm'].update('1000')
    window['--I_p_intanh'].update('0, 1')
    window['--Chk_el'].update(False)
    window['--I_p_el'].update(disabled= not bool(window['--Chk_el'].get()))
    window['||B_calc_el'].update(disabled= not bool(window['--Chk_el'].get()))
    window['--Chk_def'].update(False)
    window['--I_p_evac'].update(disabled= not bool(window['--Chk_def'].get()))
    window['--I_p_svac'].update(disabled= not bool(window['--Chk_def'].get()))
    window['--I_Tm'].update(disabled= not bool(window['--Chk_def'].get()))
    window['--Chk_intanh'].update(False)
    window['--I_p_intanh'].update(disabled= not bool(window['--Chk_intanh'].get()))
    window['--Chk_anhxc'].update(False)
    window['--I_p_anhxc'].update(disabled= not bool(window['--Chk_anhxc'].get()))

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
    window['||B_eval_anh'].update(disabled=True)
    window['||B_run_fs_params'].update(disabled=True)

    window['--IC_prop2plt'].update('')

    checked_EOS_dict = update_diabled(window,window7,opened_EOS_dict,EOS_str_lst,checked_EOS_dict, bool_anh)
    return checked_EOS_dict

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
    bool_run_eos_fitting = any([all([True,bool_dict_EOS[stri]]) for stri in opened_dict.keys()])
    bool_mode = any([window['--Chk_mode_'+stri].get() for stri in ['jjsl', 'jjdm', 'jjfv',
                                                                   # 'DM', 'Sl', 'VZ', 'mfv'
                                                                   ]])


    return bool_run_eos_fitting, bool_dict_params_EOS, bool_mode
def add_EOS(window, opened_EOS_dict,EOS_long_lst):
    for k in opened_EOS_dict.keys():
        opened_EOS_dict[k]=False
    for k in window['--LBx_EOS_listbox'].get():
        opened_EOS_dict[EOS_long_lst[k]]=True
    # print(opened_EOS_dict)

    chk_eos(window,opened_EOS_dict)

#
def update_diabled(window,window7,opened_dict,eos_available,bool_dict_params_EOS, bool_anh):
    bool_run_eos_fitting, bool_dict_params_EOS, bool_mode = bool_chks(window,opened_dict)
    # window['||B_run_eos_fitting'].update(disabled=not bool_run_eos_fitting)

    bool_minF = bool_run_eos_fitting and (True if window['--I_nu'].get()!='' else False) and bool_mode

    window['||B_run_minF'].update(disabled=not bool_minF)

    window['--I_nu'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['||B_calc_nu'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--Chk_el'].update(disabled=True if window['--I_compound'].get()=='' else False)


    for str_eos in eos_available:
        window['||B_plotter_fsprop2plt'+str_eos].update(disabled=True if window['--IC_fsprop2plt'+str_eos].get()== '' else False)

    window['||B_add_EOS'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['||B_run_eos_fitting'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['||B_PlotfittingEOS'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--Chk_def'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--Chk_intanh'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--Chk_anhxc'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--I_Ti'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--I_Pi'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--I_Tf'].update(disabled=True if window['--I_compound'].get()=='' else False)
    #window['--I_Tm'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['--I_ntemps'].update(disabled=True if window['--I_compound'].get()=='' else False)
    window['||B_plotter_tprops'].update(disabled=True if window['--IC_prop2plt'].get()== '' else False)
    if bool_anh:
        window7['||B_plotter_anh'].update(disabled=True if window7['--IC_anh2plt'].get() == '' else False)
    else:
        pass
    window['--I_cutoff_MP'].update(disabled=False)
    window['--I_ndists_MP'].update(disabled=False)

    return bool_dict_params_EOS
#
def eos_write_params(window,EOSStr,pEOS):
        window['--I_params_'+EOSStr].update(', '.join(['%.9e' for i in pEOS])%tuple(pEOS))
        pEOS2=pEOS
        # if EOSStr not in ['EAM', 'MP']:
        #     pEOS2[0]=pEOS2[0]/(0.160218e-18 * 6.02214e23)
        #     pEOS2[1] = pEOS2[1] / (1e-30 * 6.02e23)
        # print(EOSStr,':',', '.join(['%.9e' for i in pEOS])%tuple(pEOS))
##
def chk_el(window,event):
    window['--I_p_el'].update(disabled= not bool(window[event].get()))
    window['||B_calc_el'].update(disabled= not bool(window[event].get()))
#
def chk_def(window,event):
    window['--I_p_evac'].update(disabled= not bool(window[event].get()))
    window['--I_p_svac'].update(disabled= not bool(window[event].get()))
    window['--I_Tm'].update(disabled= not bool(window[event].get()))
##
def chk_intanh(window,event):
    window['--I_p_intanh'].update(disabled= not bool(window[event].get()))
def chk_anhxc(window,event):
    window['--I_p_anhxc'].update(disabled= not bool(window[event].get()))
#
def minF_enable_nexts(window):
    window['||B_plotter'].update(disabled=False)
    window['||B_eval_tprops'].update(disabled=False)
    # window['||B_eval_anh'].update(disabled=False)
#
def tprops_enable_nexts(window):
    window['||B_run_fs_params'].update(disabled=False)
    window['--I_fs_Tfrom'].update('298.15')
    window['--I_fs_Tto'].update(window['--I_Tf'].get())
    window['--I_fs_Tfrom'].update(disabled=False)
    window['--I_fs_Tto'].update(disabled=False)
    window['||B_eval_anh'].update(disabled=False)
    window['--Tab_'].update(visible=False)
#
def plot_EvV(window, eosobj_dict, opened_EOS_dict,jx):
    pots_str_lst = [k for k in opened_EOS_dict if opened_EOS_dict[k]]
    # print(pots_str_lst)
    V_DFT = eosobj_dict['V_DFT']
    E_DFT = eosobj_dict['E_DFT']
    tab3_str='#V          DFT         '+'          '.join(['%s' for i in pots_str_lst])%tuple(pots_str_lst)+'\n'
    for Vi, Ei in zip(V_DFT, E_DFT):
        Emi = [eosobj_dict[k].E0(Vi) for k in pots_str_lst]
        tab3_str= tab3_str + '%.10e   %.10e  '%(Vi,Ei) + '  '.join(['%.10e' for i in Emi])%tuple(Emi)+'\n'
    # print(tab3_str)
    initial_tabs_multilinetxt = {'t0':{'multiline':tab3_str}}
    initial_lines_settings = {
                              'l0': {'plot':True,'label':0,'linestyle':'None','color':'mediumpurple',  'marker':'o',   'markerfacecolor':'black', 'markeredgecolor':'mediumpurple',  'linewidth':2,'markersize':10},
                              'l1': {'plot':True,'label':0,'linestyle':'None','color':'purple',        'marker':'+',   'markerfacecolor':'None', 'markeredgecolor':'purple',         'linewidth':2,'markersize':10},
                              'l2': {'plot':True,'label':0,'linestyle':'None','color':'gray',          'marker':'x',   'markerfacecolor':'None', 'markeredgecolor':'gray',           'linewidth':2,'markersize':10},
                              'l3': {'plot':True,'label':0,'linestyle':'None','color':'orchid',        'marker':'s',   'markerfacecolor':'None', 'markeredgecolor':'orchid',         'linewidth':2,'markersize':10},
                              'l4': {'plot':True,'label':0,'linestyle':'None','color':'deepskyblue',   'marker':'^',   'markerfacecolor':'None', 'markeredgecolor':'deepskyblue',    'linewidth':2,'markersize':10},
                              'l5': {'plot':True,'label':0,'linestyle':'None','color':'pink',          'marker':'>',   'markerfacecolor':'None', 'markeredgecolor':'pink',           'linewidth':2,'markersize':10},
                              'l6': {'plot':True,'label':0,'linestyle':'None','color':'aqua',          'marker':'1',   'markerfacecolor':'None', 'markeredgecolor':'aqua',           'linewidth':2,'markersize':10},
                              'l7': {'plot':True,'label':0,'linestyle':'None','color':'cornflowerblue','marker':'<',   'markerfacecolor':'None', 'markeredgecolor':'cornflowerblue', 'linewidth':2,'markersize':10},
                              'l8': {'plot':True,'label':0,'linestyle':'None','color':'C0',            'marker':'2',   'markerfacecolor':'None', 'markeredgecolor':'C0',             'linewidth':2,'markersize':10},
                              'l9': {'plot':True,'label':0,'linestyle':'None','color':'mediumpurple',  'marker':'.',   'markerfacecolor':'None', 'markeredgecolor':'mediumpurple',             'linewidth':2,'markersize':10},
                              'l11':{'plot':True,'label':0,'linestyle':'None','color':'purple',        'marker':'p',   'markerfacecolor':'None', 'markeredgecolor':'purple',             'linewidth':2,'markersize':10},
                              'l10':{'plot':True,'label':0,'linestyle':'None','color':'gray',          'marker':'4',   'markerfacecolor':'None', 'markeredgecolor':'gray',             'linewidth':2,'markersize':10},
                              'l12':{'plot':True,'label':0,'linestyle':'None','color':'orchid',        'marker':'d',   'markerfacecolor':'None', 'markeredgecolor':'orchid',             'linewidth':2,'markersize':10},
                              'l13':{'plot':True,'label':0,'linestyle':'None','color':'deepskyblue',   'marker':'+',   'markerfacecolor':'None', 'markeredgecolor':'deepskyblue',             'linewidth':2,'markersize':10},
                              'l14':{'plot':True,'label':0,'linestyle':'None','color':'pink',          'marker':'x',   'markerfacecolor':'None', 'markeredgecolor':'pink',             'linewidth':2,'markersize':10},
                              'l15':{'plot':True,'label':0,'linestyle':'None','color':'aqua',          'marker':'+',   'markerfacecolor':'None', 'markeredgecolor':'aqua',             'linewidth':2,'markersize':10},
                              }
    initial_fig_settings = {'figwidth':5.5,'figheight':4.5,'use_title':False,'title':'','titlexpos':.7,'titleypos':.9,
                            'titlesize':12,'use_xlabel':True,'use_ylabel':True,'xlabel':r'Volume $\left[\frac{m^3}{mol-at}\right]$','ylabel':r'$E~\left[\frac{J}{mol-at}\right]$','labelxsize':13,
                            'labelysize':13,'auto_xlim':True,'auto_ylim':True,'limxmin':-0.5,'limxmax':110,'limymin':-1,'limymax':2,'use_legend':True,'legend_loc':'best',
                            'legendncol':2,'legendfontsize':14,'use_grid':True,'lmargin':0.2,'rmargin':0.98,'tmargin':0.95,'bmargin':0.12, 'scalex':1,'scaley':1}

    data4plot = plot.pop_window(initial_tabs_multilinetxt,initial_lines_settings,initial_fig_settings,jx)

    return data4plot

def plot_EvV_full(window, eosobj_dict, opened_EOS_dict,jx):
    pots_str_lst = [k for k in opened_EOS_dict if opened_EOS_dict[k]]
    # print(pots_str_lst)
    V_DFT = eosobj_dict['V_DFT']
    E_DFT = eosobj_dict['E_DFT']
    tab3_str='#V          DFT         '+'          '.join(['%s' for i in pots_str_lst])%tuple(pots_str_lst)+'\n'
    for Vi, Ei in zip(V_DFT, E_DFT):
        Emi = [eosobj_dict[k].E0(Vi) for k in pots_str_lst]
        tab3_str= tab3_str + '%.10e   %.10e  '%(Vi,Ei) + '  '.join(['%.10e' for i in Emi])%tuple(Emi)+'\n'
    # print(tab3_str)
    initial_tabs_multilinetxt = {'t0':{'multiline':tab3_str}}
    initial_lines_settings = {
                              'l0': {'plot':True,'label':0,'linestyle':'None','color':'mediumpurple',  'marker':'o',   'markerfacecolor':'black', 'markeredgecolor':'mediumpurple',  'linewidth':2,'markersize':10},
                              'l1': {'plot':True,'label':0,'linestyle':'None','color':'purple',        'marker':'+',   'markerfacecolor':'None', 'markeredgecolor':'purple',         'linewidth':2,'markersize':10},
                              'l2': {'plot':True,'label':0,'linestyle':'None','color':'gray',          'marker':'x',   'markerfacecolor':'None', 'markeredgecolor':'gray',           'linewidth':2,'markersize':10},
                              'l3': {'plot':True,'label':0,'linestyle':'None','color':'orchid',        'marker':'s',   'markerfacecolor':'None', 'markeredgecolor':'orchid',         'linewidth':2,'markersize':10},
                              'l4': {'plot':True,'label':0,'linestyle':'None','color':'deepskyblue',   'marker':'^',   'markerfacecolor':'None', 'markeredgecolor':'deepskyblue',    'linewidth':2,'markersize':10},
                              'l5': {'plot':True,'label':0,'linestyle':'None','color':'pink',          'marker':'>',   'markerfacecolor':'None', 'markeredgecolor':'pink',           'linewidth':2,'markersize':10},
                              'l6': {'plot':True,'label':0,'linestyle':'None','color':'aqua',          'marker':'1',   'markerfacecolor':'None', 'markeredgecolor':'aqua',           'linewidth':2,'markersize':10},
                              'l7': {'plot':True,'label':0,'linestyle':'None','color':'cornflowerblue','marker':'<',   'markerfacecolor':'None', 'markeredgecolor':'cornflowerblue', 'linewidth':2,'markersize':10},
                              'l8': {'plot':True,'label':0,'linestyle':'None','color':'C0',            'marker':'2',   'markerfacecolor':'None', 'markeredgecolor':'C0',             'linewidth':2,'markersize':10},
                              'l9': {'plot':True,'label':0,'linestyle':'None','color':'mediumpurple',  'marker':'.',   'markerfacecolor':'None', 'markeredgecolor':'mediumpurple',             'linewidth':2,'markersize':10},
                              'l11':{'plot':True,'label':0,'linestyle':'None','color':'purple',        'marker':'p',   'markerfacecolor':'None', 'markeredgecolor':'purple',             'linewidth':2,'markersize':10},
                              'l10':{'plot':True,'label':0,'linestyle':'None','color':'gray',          'marker':'4',   'markerfacecolor':'None', 'markeredgecolor':'gray',             'linewidth':2,'markersize':10},
                              'l12':{'plot':True,'label':0,'linestyle':'None','color':'orchid',        'marker':'d',   'markerfacecolor':'None', 'markeredgecolor':'orchid',             'linewidth':2,'markersize':10},
                              'l13':{'plot':True,'label':0,'linestyle':'None','color':'deepskyblue',   'marker':'+',   'markerfacecolor':'None', 'markeredgecolor':'deepskyblue',             'linewidth':2,'markersize':10},
                              'l14':{'plot':True,'label':0,'linestyle':'None','color':'pink',          'marker':'x',   'markerfacecolor':'None', 'markeredgecolor':'pink',             'linewidth':2,'markersize':10},
                              'l15':{'plot':True,'label':0,'linestyle':'None','color':'aqua',          'marker':'+',   'markerfacecolor':'None', 'markeredgecolor':'aqua',             'linewidth':2,'markersize':10},
                              }
    initial_fig_settings = {'figwidth':5.5,'figheight':4.5,'use_title':False,'title':'','titlexpos':.7,'titleypos':.9,
                            'titlesize':12,'use_xlabel':True,'use_ylabel':True,'xlabel':'Volume $\left[m^3/mol-at\\right]$','ylabel':'$E~\left[J/mol-at\\right]$','labelxsize':13,
                            'labelysize':13,'auto_xlim':True,'auto_ylim':True,'limxmin':-0.5,'limxmax':110,'limymin':-1,'limymax':2,'use_legend':True,'legend_loc':'best',
                            'legendncol':2,'legendfontsize':14,'use_grid':True,'lmargin':0.2,'rmargin':0.98,'tmargin':0.95,'bmargin':0.12, 'scalex':1,'scaley':1}

    data4plot = plot.pop_window(initial_tabs_multilinetxt,initial_lines_settings,initial_fig_settings,jx)

    return data4plot

def plot_VvT(window,jx):
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
                              'l9':{'plot':True,'label':0,'linestyle':'-','color':'C1',        'marker':'None','markerfacecolor':'None', 'markeredgecolor':'None','linewidth':2,'markersize':10},
                              }

    initial_fig_settings = {'figwidth':5.5,'figheight':4.5,'use_title':False,'title':'','titlexpos':.7,'titleypos':.9,
                            'titlesize':12,'use_xlabel':True,'use_ylabel':True,'xlabel':'T $\left[K\\right]$','ylabel':'$V~\left[m^3/atom\\right]$','labelxsize':13,
                            'labelysize':13,'auto_xlim':True,'auto_ylim':True,'limxmin':-0.5,'limxmax':110,'limymin':-1,'limymax':2,'use_legend':True,'legend_loc':'best',
                            'legendncol':2,'legendfontsize':14,'use_grid':True,'lmargin':0.14,'rmargin':0.98,'tmargin':0.95,'bmargin':0.12, 'scalex':1,'scaley':1}

    data4plot = plot.pop_window(initial_tabs_multilinetxt,initial_lines_settings,initial_fig_settings,jx)

    return data4plot
#
def plot_tprops(window,minF_header,jx):
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
                              'l9':{'plot':True,'label':0,'linestyle':'-','color':'C1',        'marker':'None','markerfacecolor':'None', 'markeredgecolor':'None','linewidth':2,'markersize':10},
                              }
    initial_fig_settings = {'figwidth':5.5,'figheight':4.5,'use_title':False,'title':'','titlexpos':.7,'titleypos':.9,
                            'titlesize':12,'use_xlabel':True,'use_ylabel':True,'xlabel':'T $\left[K\\right]$','ylabel':window['--IC_prop2plt'].get(),'labelxsize':13,
                            'labelysize':13,'auto_xlim':True,'auto_ylim':True,'limxmin':-0.5,'limxmax':110,'limymin':-1,'limymax':2,'use_legend':True,'legend_loc':'best',
                            'legendncol':2,'legendfontsize':14,'use_grid':True,'lmargin':0.14,'rmargin':0.98,'tmargin':0.95,'bmargin':0.12, 'scalex':1,'scaley':1}
    # plot.pop_window_simple(initial_tabs_multilinetxt,initial_lines_settings,initial_fig_settings)
    data4plot = plot.pop_window(initial_tabs_multilinetxt,initial_lines_settings,initial_fig_settings,jx)
    return data4plot

def plot_anh(window,minF_header,jx):
    initial_tabs_multilinetxt = {'t0':{'multiline':[]}}
    for ix, k in enumerate(minF_header):
        window['--M_anh_'+str(k)].get()
        datas_dict = tbox.txt2dict(window['--M_anh_'+str(k)].get())
        txt2M = '#T    '+k+'\n'
        for valsi in np.c_[datas_dict['T'].T,datas_dict[window['--IC_anh2plt'].get()].T]:
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
                              'l9':{'plot':True,'label':0,'linestyle':'-','color':'C1',        'marker':'None','markerfacecolor':'None', 'markeredgecolor':'None','linewidth':2,'markersize':10},
                              }
    initial_fig_settings = {'figwidth':5.5,'figheight':4.5,'use_title':False,'title':'','titlexpos':.7,'titleypos':.9,
                            'titlesize':12,'use_xlabel':True,'use_ylabel':True,'xlabel':'T $\left[K\\right]$','ylabel':window['--IC_anh2plt'].get()+'$_{EOS}$'+'$-$'+window['--IC_anh2plt'].get()+'$_{Murnaghan}$','labelxsize':13,
                            'labelysize':13,'auto_xlim':True,'auto_ylim':True,'limxmin':-0.5,'limxmax':110,'limymin':-1,'limymax':2,'use_legend':True,'legend_loc':'best',
                            'legendncol':2,'legendfontsize':14,'use_grid':True,'lmargin':0.14,'rmargin':0.98,'tmargin':0.95,'bmargin':0.12, 'scalex':1,'scaley':1}
    # plot.pop_window_simple(initial_tabs_multilinetxt,initial_lines_settings,initial_fig_settings)
    data4plot = plot.pop_window(initial_tabs_multilinetxt,initial_lines_settings,initial_fig_settings,jx)
    return data4plot
#
def plot_fsprops(window,event,fs_params,Tfrom,Tto,TPs_calculated_dict,jx):
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
                              'l9':{'plot':True,'label':0,'linestyle':'-','color':'C1',        'marker':'None','markerfacecolor':'None', 'markeredgecolor':'None','linewidth':2,'markersize':10},
                              }
    initial_fig_settings = {'figwidth':5.5,'figheight':4.5,'use_title':False,'title':'','titlexpos':.7,'titleypos':.9,
                            'titlesize':12,'use_xlabel':True,'use_ylabel':True,'xlabel':'T $\left[K\\right]$','ylabel':window['--IC_prop2plt'].get(),'labelxsize':13,
                            'labelysize':13,'auto_xlim':True,'auto_ylim':True,'limxmin':-0.5,'limxmax':110,'limymin':-1,'limymax':2,'use_legend':True,'legend_loc':'best',
                            'legendncol':1,'legendfontsize':11,'use_grid':True,'lmargin':0.14,'rmargin':0.98,'tmargin':0.95,'bmargin':0.12, 'scalex':1,'scaley':1}
    data4plot = plot.pop_window(initial_tabs_multilinetxt,initial_lines_settings,initial_fig_settings,jx)
    return data4plot

#
