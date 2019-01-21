import ROOT 

import numpy as np
import scipy.stats as stats
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axis as ax
from matplotlib_hep import histpoints
import sys

from root_numpy import root2array, rec2array, tree2rec
from root_pandas import read_root

from Used_Variables import *
from Used_Variables import Input_Data
from Useful_funcs import *

"""""""""""""""""""""""
Input data and MC: Variables and preselection

"""""""""""""""""""""""
workdir     = '/Users/mboubdir/Desktop/repository/MajoranaAnalysis/NewAna/'

MC_filesres = ['12MCDown_B2Norm_B2XMuMu_Str21_Truth_Resampled.root', '12MCUp_B2Norm_B2XMuMu_Str21_Truth_Resampled.root']

DATA_files  = ['12DATAUp_Norm_B2XMuMu_strip21.root', '12DATADown_Norm_B2XMuMu_strip21.root', \
               '11DATADown_Norm_B2XMuMu_strip21r1.root', '11DATAUp_Norm_B2XMuMu_strip21r1.root']

sweights    = 'Cuts2_v2all_sweights_12DATA.root'

tree_data   = 'PromptNeutrinoTupleTool/DecayTree'
tree_Lumi   = 'GetIntegratedLuminosity/LumiTuple'
tree_mc     = 'DecayTree'
tree_we     = 'SIG'

#SignalMassRange = '(B_MM <= 5350.) & (B_MM >= 5200.)'
var_DATA    = ['B_MM', 'B_PT', 'B_ETA', 'B_PT', 'nTracks', 'nSig_sw']

#Load DATA &  MC 

print "Loading DATA"

DATASNorm = read_root(
    [NormChan_path+sweights], 
    key=tree_we, 
    columns=['B_*', 'pi_*', 'mu_*', 'N_*', 'nTracks', 'nSig_sw'])

DATA12 = read_root(
    [NormChan_path+f for f in DATA_files] ,
    key=tree_data , 
    columns=variables + vars_PIDuncorr_v2)

MC12   = read_root(
    [NormChan_path+f for f in MC_filesres] ,
    key=tree_mc , 
    columns=variables + vars_PIDuncorr_v2 + vars_PIDcorr_v2)

print "Finished Loading DATA"

print("MC Read {} ".format(len(MC12)))
print("DATA Read {} ".format(len(DATA12)))
#print("Sweighted_data {} ".format(len(Wghts)))
print "Preselection: MC Vs. DATA"

mc_norm   = MC12.query(truth_string + '&'+ trig_string + '&' + Kin_Particle_Pre  + '&' + pid_string_corr_v2_new2 ).copy()
print "MC selected"
data_norm = DATA12.query(trig_string + '&' + Kin_Particle_Pre  + '&' + pid_string_v2_new2).copy()
print "DATA selected"

#print("MC raw after all selection: {}".format(len(mc_normraw)))
print("MC Read after Trigger- and Pre-Selection {} ".format(len(mc_norm)))
print("DATA Read after Trigger- and Pre-Selection {} ".format(len(data_norm)))
print("Sweighted_data {} ".format(len(DATASNorm)))

# Calculate weights
weights_nTracks = get_weights(mc_norm['nTracks'], DATASNorm['nTracks'], mc_norm['nTracks'], 100, weights_x=DATASNorm['nSig_sw'])
total_weights = weights_nTracks

weights_B_PT = get_weights(mc_norm['B_PT'], DATASNorm['B_PT'], mc_norm['B_PT'], 100, weights_x=DATASNorm['nSig_sw'])
total_weights = weights_nTracks * weights_B_PT

weights_B_ETA = get_weights(mc_norm['B_ETA'], DATASNorm['B_ETA'], mc_norm['B_ETA'], 100, weights_x=DATASNorm['nSig_sw'])
total_weights = weights_nTracks * weights_B_ETA

weights_B_ENDVTX = get_weights(mc_norm['B_ENDVERTEX_CHI2'], DATASNorm['B_ENDVERTEX_CHI2'], mc_norm['B_ENDVERTEX_CHI2'], 100, weights_x=DATASNorm['nSig_sw'])
total_weights = weights_nTracks * weights_B_ENDVTX

#weights_B_IPCHI2 = get_weights(mc_norm['B_IPCHI2_OWNPV'], DATASNorm['B_IPCHI2_OWNPV'], mc_norm['B_IPCHI2_OWNPV'], 100, weights_x=DATASNorm['nSig_sw'])
total_weights = weights_nTracks * weights_B_PT * weights_B_ETA * weights_B_ENDVTX

#sum_tot_weights = np.sum(total_weights)
mc_norm['weights_nTracks'] = weights_nTracks 
mc_norm['weights_B_ETA'] = weights_B_ETA
mc_norm['weights_B_PT'] = weights_B_PT
mc_norm['weights_B_ENDVERTEX_CHI2'] = weights_B_ENDVTX

sum_ev = total_weights.sum()
mc_norm['weights_tot'] = total_weights/sum_ev*(len(mc_norm))

#'B_ETA': '$\eta(B)$',
vars_to_reweight_dict = {
    'nTracks'   : ('$N$ tracks', 'N_Tracks'),
    'B_PT'      : ('$p_T(B)$', 'B_PT'),
    'B_ETA'     : ('$\eta(B)$', 'B_ETA'),
    'B_ENDVERTEX_CHI2'     : ('$\chi^2_{EndVtx}$ (B)', 'B_ENDVERTEX_CHI2') 
}

# Plot the reweighted variables
for id, col in enumerate(vars_Toreweight, 1):
    print id, col
    
    plt.figure()

    #if col=='B_PT':
    #    range =(0, 50000)
    #    #plt.xlim(0.0, 50000)
    #if col =='nTracks':
    #    range=(0,800)
    #if col == 'B_ENDVERTEX_CHI2':
    #    range=(0, 25) 
    
    data_col = DATASNorm[col].values
    mc_col   = mc_norm[col].values
    mc_rewcol= mc_norm['weights_{}'.format(col)].values

    range_x = (np.min(mc_norm[col]), np.max(DATASNorm[col]))
    range_y = (np.min(mc_norm[col]), np.max(mc_norm[col]))

    range_ = ()
    if np.max(mc_norm[col]) > np.max(mc_norm[col]):
        range_ = range_y
        print(range_x, range_)
    elif np.max(mc_norm[col]) > np.max(DATASNorm[col]):
        range_ = range_x
        print(range_y, range_)
        
    y_data, y_data, norm_data = histpoints(data_col, range=range_, color='black', normed=True, bins=100,
                                           label='sWeighted DATA', markersize=3. , marker='o', weights=DATASNorm['nSig_sw'])
    
    x_uncorr, y_uncorr, norm_uncorr = histpoints(mc_col, range=range_, color='red', normed=True, bins=100, label='MC', markersize=3., marker='o')
    
    x_corr, y_corr, norm_corr = histpoints(mc_col, range=range_, color= 'green', normed=True,  bins=100,
                                           weights=mc_norm['weights_{}'.format(col)], markersize=3., label='Reweighted MC', marker='o')
    

    plt.xlabel(vars_to_reweight_dict[col][0])
    plt.ylabel('Events')
    #plt.yscale('log')
    plt.legend(prop={'size': 10})
    plt.savefig('./output_pdf/{}.pdf'.format(vars_to_reweight_dict[col][1]), bbox_inches='tight')

    #plt.show()

#sys.exit(0)

#mc_norm.to_root('Weighted_Cuts2_Preselected_12MCNorm.root', key='DecayTree', mode='a')
#print("File with weights saved safelly")


#Resampled variables
varpid = {
          #'pi_MC12TuneV3_ProbNNpi_corr'    : ('MC12TuneV3_ProbNNpi($\pi$)', 'pi_MC12TuneV3_ProbNNpi'), 
          'pi_MC12TuneV2_ProbNNpi_corr'    : ('MC12TuneV2_ProbNNpi($\pi$)', 'pi_MC12TuneV2_ProbNNpi'), 
          #'pi_MC12TuneV3_ProbNNk_corr'     : ('MC12TuneV3_ProbNNk ($\pi$)', 'pi_MC12TuneV3_ProbNNk'),
          'pi_MC12TuneV2_ProbNNk_corr'     : ('MC12TuneV2_ProbNNk ($\pi$)','pi_MC12TuneV2_ProbNNk'),
          'mu_prim_MC12TuneV3_ProbNNk_corr': ('$\mu_\mathrm{prim}$_MC12TuneV3_ProbNNk','mu_prim_MC12TuneV3_ProbNNk'),
          'mu_prim_MC12TuneV3_ProbNNpi_corr': ('$\mu_\mathrm{prim}$_MC12TuneV3_ProbNNpi','mu_prim_MC12TuneV3_ProbNNpi'),
          'mu_prim_MC12TuneV3_ProbNNmu_corr' : ('$\mu_\mathrm{prim}$_MC12TuneV3_ProbNNmu','mu_prim_MC12TuneV3_ProbNNmu'),
          'mu_sec_MC12TuneV3_ProbNNpi_corr': ('$\mu_\mathrm{sec}$_MC12TuneV3_ProbNNpi','mu_sec_MC12TuneV3_ProbNNpi'),
          'mu_sec_MC12TuneV3_ProbNNmu_corr' : ('$\mu_\mathrm{sec}$_MC12TuneV3_ProbNNmu','mu_sec_MC12TuneV3_ProbNNmu'),
          'mu_sec_MC12TuneV3_ProbNNk_corr' : ('$\mu_\mathrm{sec}$_MC12TuneV3_ProbNNk','mu_sec_MC12TuneV3_ProbNNk' )
}



print(len(DATASNorm))
print(vars_PIDcorr_v2)
print(vars_PIDuncorr_v2)

for id, (var_corr, var_uncorr) in enumerate(zip(vars_PIDcorr_v2, vars_PIDuncorr_v2)):
    print id, var_corr, var_uncorr
        
    data_PIDuncorr = DATASNorm[var_uncorr].values
    mc_PIDuncorr = mc_norm[var_uncorr].values
    mc_PIDcorr = mc_norm[var_corr].values

    range_x = (np.min(data_PIDuncorr), np.max(data_PIDuncorr))
    range_y = (np.min(mc_PIDcorr), np.max(mc_PIDcorr))
    
    if np.max(data_PIDuncorr) > np.max(mc_PIDcorr):
        range_ = range_y
        print(range_x, range_)
    elif np.max(mc_PIDcorr) > np.max(data_PIDuncorr):
        range_ = range_x
        print(range_y, range_) 
    #print("uncorr variables {}".format(mc_PIDuncorr))
    #print("corr variables {}".format(mc_PIDcorr))

    x_data, y_data,  norm_data = histpoints(data_PIDuncorr, color='black',  normed=True, weights=DATASNorm['nSig_sw'] , bins=100, markersize=4, label='sWeighted DATA')
    #x_uncorr, y_uncorr,  norm_uncorr = histpoints(mc_PIDuncorr, color='red', normed=True, bins=100, markersize=4, label='MC')
    #x_corr, y_corr,  norm_corr = histpoints(mc_PIDcorr, color= 'blue', normed=True, bins=100, markersize=4, label='Resampled MC')
    x_rew_corr, y_rew_corr, norm_rew_corr = histpoints(mc_PIDcorr, color= 'green', normed=True, weights=mc_norm['weights_tot'],  bins=100, \
                                                        markersize=4, label='Resampled & reweighted MC')
    plt.xlabel(varpid[var_corr][0])
    plt.ylabel('Events')
    # plt.figure(id)
    plt.yscale('log')
    plt.title(varpid[var_corr][0])

    plt.legend(prop={'size': 8})
    plt.savefig('./output_pdf/{}.pdf'.format(varpid[var_corr][1]), bbox_inches='tight')
    #plt.show()

##################MORE VARIABLES######################

training_variables = ['B_TAU', 'B_log10FD',  'B_log10FDChi2', 'B_AcosDira', 'B_ProbChi2Ndf', \
                      'B_log10IPChi2','pi_PT', 'pi_log10IPChi2', \
                      'mu_prim_log10IPChi2', 'mu_sec_log10IPChi2']#, 'N_MM']

training_variables_ = ['B_TAU', 'B_FD_OWNPV',  'B_FDCHI2_OWNPV',
                      'B_IPCHI2_OWNPV', 'B_ENDVERTEX_CHI2', 
                      'B_ENDVERTEX_NDOF','B_DIRA_OWNPV', 'pi_PT', 'pi_IPCHI2_OWNPV',
                      'mu_prim_IPCHI2_OWNPV', 'mu_sec_IPCHI2_OWNPV']


training_vars_dict_ = {'B_TAU'         : ('$\tau(B)$', 'B_TAU'),
                     'B_FD_OWNPV'    : ('$(FD)(B)$','B_FD'),
                     'B_FDCHI2_OWNPV': ('$(\chi^{2}(FD)(B)$', 'B_FDChi2'),
                     'B_DIRA_OWNPV'  : ('$(DIRA(B)$', 'B_Dira'),
                     'B_ENDVERTEX_NDOF' : ('$ENDVERTEX_{NDOF}(B)$', 'B_ENDVERTEX_NDOF'),
                     'B_ENDVERTEX_CHI2' : ('$ENDVERTEX_{\chi^{2}}(B)$', 'B_ENDVERTEX_CHI2'), 
                     'B_IPCHI2_OWNPV' : ('$(IP_{\chi^{2}}(B)$', 'B_IPChi2'),
                     #'B_VTXISOBDTHARDFIRSTVALUE': ('$VTXISOBDTHARDFIRSTVALUE(B)$', 'B_VTXISOBDTHARDFIRSTVALUE'),
                     'pi_PT': ('$P_{T}(\pi)$', 'pi_PT'),
                     'pi_IPCHI2_OWNPV': ('$IP_{\chi^{2}(\pi)}$', 'pi_IPChi2'),
                     'mu_prim_IPCHI2_OWNPV': ('$IP_{\chi^{2}} (\mu_{prim})$', 'mu_prim_IPChi2' ),
                     'mu_sec_IPCHI2_OWNPV': ( '$IP_{\chi^{2}} (\mu_{sec})$', 'mu_sec_IPChi2')
                     }

def process(df):
    df['B_PT'] = df['B_PT']
    df['B_log10Tau'] = np.log10(df['B_TAU'])
    df['B_log10FD'] = np.log10(df['B_FD_OWNPV'])
    df['B_log10FDChi2'] = np.log10(df['B_FDCHI2_OWNPV'])
    df['B_log10IPChi2'] = np.log10(df['B_IPCHI2_OWNPV'])
    df['mu_prim_log10IPChi2'] = np.log10(df['mu_prim_IPCHI2_OWNPV'])
    df['mu_sec_log10IPChi2'] = np.log10(df['mu_sec_IPCHI2_OWNPV'])
    df['pi_log10IPChi2'] = np.log10(df['pi_IPCHI2_OWNPV'])
    df['B_ProbChi2Ndf'] = stats.chi2.sf(df['B_ENDVERTEX_CHI2'], df['B_ENDVERTEX_NDOF'])
    df['B_AcosDira'] = np.arccos(df['B_DIRA_OWNPV'])



    
training_vars_dict= {'B_TAU': ('$\tau(B)$', 'B_TAU'),
                     'B_log10FD': ('$log_{10}(FD)(B)$','B_log10FD'),
                     'B_log10FDChi2': ('$log_{10}(\chi^{2}(FD)(B)$', 'B_log10FDChi2'),
                     'B_AcosDira': ('$Acos(DIRA(B))$', 'B_AcosDira'),
                     'B_ProbChi2Ndf': ('$Prob(\chi^{2}/Ndf)(B)$', 'B_ProbChi2Ndf'),
                     'B_log10IPChi2': ('$log_{10}(IP_{\chi^{2}})(B)$', 'B_log10IPChi2'),
                     #'B_VTXISOBDTHARDFIRSTVALUE': ('$VTXISOBDTHARDFIRSTVALUE(B)$', 'B_VTXISOBDTHARDFIRSTVALUE'),
                     'pi_PT': ('$P_{T}(\pi)$', 'pi_PT'),
                     'pi_log10IPChi2': ('$log_{10}(IP_{\chi^{2})(\pi)}$', 'pi_log10IPChi2'),
                     'mu_prim_log10IPChi2': ('$log_{10}(IP_{\chi^{2}}) (\mu_{prim})$', 'mu_prim_log10IPChi2' ),
                     'mu_sec_log10IPChi2': ( '$log_{10}(IP_{\chi^{2}}) (\mu_{sec})$', 'mu_sec_log10IPChi2')
                     }

process(DATASNorm)
process(mc_norm)

for id, col in enumerate(training_variables_, 1):
    
    plt.figure()

    data_col = DATASNorm[col].values
    mc_col   = mc_norm[col].values

    range_x = (np.min(data_col), np.max(data_col))
    range_y = (np.min(mc_col), np.max(mc_col))

    if np.max(data_col) > np.max(mc_col):
        range_ = range_y
        print(range_x, range_)
    elif np.max(mc_col) > np.max(data_col):
        range_ = range_x
        print(range_y, range_)
    y_data, y_data, norm_data = histpoints(data_col, range=range_, color='black', normed=True, bins=100,  label='sWeighted DATA',
                                           markersize=3. , marker='o', weights=DATASNorm['nSig_sw'])
    
    #x_uncorr, y_uncorr, norm_uncorr = histpoints(mc_col, range=range_, color='red', normed=True, bins=100, label='MC', markersize=3., marker='o')
    
    x_corr, y_corr, norm_corr = histpoints(mc_col, range=range_, color= 'green', normed=True,  bins=100, weights=mc_norm['weights_tot'], markersize=3., \
                                           label='Reweighted MC', marker='o')
    
    
    plt.xlabel(training_vars_dict_[col][0])
    plt.ylabel('Events')
    #plt.yscale('log')
    plt.legend(prop={'size': 10})
    plt.title(training_vars_dict_[col][0],  fontsize=14)
    plt.savefig('./output_pdf/{}_Reweighted_NormChan.pdf'.format(training_vars_dict_[col][1]), bbox_inches='tight')
    #plt.show()
    
sys.exit(0)

'''


#Hep_ml bins Reweightes using 
#Bins reweighter 
from hep_ml import reweight
from sklearn.cross_validation import train_test_split
from hep_ml.metrics_utils import ks_2samp_weighted
hist_settings = {'bins': 100, 'normed': True, 'alpha': 0.7}

original_train, original_test = train_test_split(mc_norm)
target_train, target_test = train_test_split(DATASNorm)
original_weights = np.ones(len(mc_norm)) #original
original_weights_train = np.ones(len(original_train))
original_weights_test = np.ones(len(original_test))

def draw_distributions(original, target, new_original_weights):
    for id, column in enumerate(vars_Toreweight, 1):
        xlim = np.percentile(np.hstack([target[column]]), [0.01, 99.99])
        plt.subplot(2, 3, id)
        plt.hist(original[column],  range=xlim, **hist_settings)
        plt.hist(target[column], range=xlim, **hist_settings)
        plt.title(column)
        print 'KS over ', column, ' = ', ks_2samp_weighted(original[column], target[column], 
                                         weights1=new_original_weights, weights2=np.ones(len(target), dtype=float))
print(len(mc_norm), len(DATASNorm))
plt.figure(0)
draw_distributions(mc_norm[vars_Toreweight], DATASNorm[vars_Toreweight], original_weights)

print("train set")
plt.figure(1)
draw_distributions(original_train[vars_rewei], target_train[vars_rewei], original_weights_train)

print("test set")
plt.figure(2)
draw_distributions(original_test[vars_rewei], target_test[vars_rewei], original_weights_test)

###Gradient Boosted Reweighter
reweighter = reweight.GBReweighter(n_estimators=100, learning_rate=0.1, max_depth=3,
                                   min_samples_leaf=1000, gb_args={'subsample': 0.4})

reweighter.fit(original_train, target_train, target_weight=DATASNorm['nSig_sw'])
gb_weights_test = reweighter.predict_weights(original_test)
plt.figure(6)
draw_distributions(original_test, target_test, gb_weights_test)


plt.show()


#####

bins_reweighter = reweight.BinsReweighter(n_bins=100, n_neighs=1.)
bins_reweighter.fit(original_train[vars_rewei], target_train[vars_rewei])
bins_weights_test = bins_reweighter.predict_weights(original_test[vars_rewei])

#plt.figure(3)
draw_distributions(original_test[vars_rewei], target_test[vars_rewei], bins_weights_test)

def check_ks_of_expression(expression):
    col_original = original_test.eval(expression, engine='python')
    col_target = target_test.eval(expression, engine='python')
    w_target= np.ones(len(col_target), dtype = 'float')
    print(w_target)
    print 'Bins reweight KS:', ks_2samp_weighted(col_original, col_target, 
                                                 weights1=bins_weights_test, weights2=w_target)
    
print(check_ks_of_expression('B_ETA *B_PT  * nTracks'))
print(check_ks_of_expression('B_ETA *B_PT / nTracks'))

# PID variables plots
hist_settings2 = {'bins': 100, 'normed': True, 'alpha': 0.3}

def ratio(rew_var):
    for v in rew_var:
        print(v)
        mc_norm['{}_bin'.format(v)] = pd.cut(mc_norm[v],  bins=[0:100: 10], precision=4)
        data_norm['{}_bin'.format(v)] = pd.cut(data_norm[v],  bins=[0:100: 10], precision=4)
#        result = np.where(np.isnan(a), 0, a * b)
        print(mc_norm['{}_bin'.format(v)].shape[0])
        print(data_norm['{}_bin'.format(v)].shape[0])
        weights  = float(data_norm['{}_bin'.format(v)].shape[0]) / mc_norm['{}_bin'.format(v)].shape[0]
        print('weighst:')
        print(weights)
        #            reuslt   = np.where(np.isnan(weights), )
        #           print("Calculated weights: {}".format(weights))
        weights *= weights
#           print("multiplied weights: {}".format(weights))
        return(weights)
    
#        except:
#            return np.nan


'''
