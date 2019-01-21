import ROOT 
import os

import numpy as np
import scipy.stats as stats
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axis as ax
import sys

from root_pandas import read_root

"""""""""""""""""""""""
Input data and MC: VariablesOB and preselection

"""""""""""""""""""""""
workdir       =  os.getcwd()
file_path     = '/net/scratch_cms1b2/cms/user/boubdir/New_Output/NormChan/BKGs_Norm/'

tree          = 'PromptNeutrinoTupleTool/DecayTree'
BKG_Infos     = {
                  '12143001': ('B+ -> Jpsi(mu+ mu-) K+' , '2107141' , 'Stripping21' , 'sim9b', 'B_BKGCAT == 30'),
                  '12113001': ('B+ -> K+mu+mu-', '527247' , 'Stripping20', 'sim08a', 'B_BKGCAT = 30' ),
                  '12133011': ('B+ -> Psi(2S)(mu+ mu-) K+','2189968', 'Stripping21' ,'Sim09b' , 'B_BKGCAT == 30' ),
                  '13144014': ('Bs -> Jpsi(mu+ mu-) f0' , '1546495' , 'Stripping20' , 'sim08a', '(B_BKGCAT ==40 | B_BKGCAT ==50)'),
                  '12163061': ('B+ -> D0(pipi) pi+','2066287', 'Stripping21' ,'sim9b', 'B_BKGCAT == 30' ),
                  '12163031': ('B+ -> D0(pipi) K', '772249' , 'Stripping20', 'sim08a', 'B_BKGCAT == 30'  ),
                  '12113024': ('B+ -> pi+mu+mu-','1013648',  'Stripping20', 'sim08e', 'B_BKGCAT == 30' ),
                  '12143491': ('B+ -> Jpsi(mu+ mu-) rho+', '4837575', 'Stripping21', 'sim8i', '(B_BKGCAT ==40 | B_BKGCAT ==50)' ),
                  '11144008': ('B0 -> Jpsi(mu+ mu-) rho0', '536497', 'Stripping20', 'sim8a', '(B_BKGCAT ==40 | B_BKGCAT ==50)' ),
                  '11144001': ('B0 -> Jpsi(mu+ mu-) K*0', '20042482', 'Stripping21', 'sim9a', '(B_BKGCAT ==40 | B_BKGCAT ==50)'), #Up: 10042056
                  '11144061': ('B0 -> Jpsi(mu+ mu-) pipi (f0?)', ' 2008490', 'Stripping20', 'sim8a', '(B_BKGCAT ==40 | B_BKGCAT ==50)'), #Up: 1007493
                  '12143501': ('B+ -> Jpsi(mu+ mu-) K*(pipi0pi0)', '3268208' , 'Stripping21', 'sim09a', '(B_BKGCAT == 40 | B_BKGCAT ==50)' ),
                  '12103002': ('B+ -> pi+pi-pi+', '2028689', 'stripping20', 'sim8e', 'B_BKGCAT == 30'  ),
                  '12103012': ('B+ -> K+K-K+','2017779' ,'Stripping20', 'sim08e', 'B_BKGCAT == 30'  ),
                  '12103022': ('B+ -> pi+pi-K+', '2028990' , 'Stripping20','sim08b',  'B_BKGCAT == 30.' ), #Up sim8e also available , phsp
                  '12103032': ('B+ -> pi+K-K+','4006215' , 'Stripping21', 'sim09b', 'B_BKGCAT == 30.' )  #phsp
                }

BKG_files     = ['%s_BKG_MCNorm_B2XMuMu.root' % key for key in BKG_Infos]
print(BKG_files)
df_EventType  = ['%s_df' % key for key in BKG_Infos]
BKG_df_dict   = dict(zip(df_EventType, BKG_files))

variables     = ['B_MM', 'B_PT', 'B_TAU', 'B_ETA', 'B_PT', 'nTracks',  'B_L0MuonDecision_TOS', 'B_L0DiMuonDecision_TOS', 'B_Hlt1TrackMuonDecision_TOS', \
                 'B_Hlt1TrackAllL0Decision_TOS', 'B_Hlt2TopoMu2BodyBBDTDecision_TOS', 'B_Hlt2TopoMu3BodyBBDTDecision_TOS', \
                 'mu_sec_isMuon', 'mu_prim_isMuon', 'pi_ProbNNk', 'pi_ProbNNpi','B_TRUEID', \
                 'B_ENDVERTEX_CHI2', 'B_ENDVERTEX_NDOF', 'B_IPCHI2_OWNPV', 'B_DIRA_OWNPV', 'mu_sec_P', 'mu_prim_P','B_FD_OWNPV',\
                 'mu_sec_PT', 'mu_prim_PT', 'mu_sec_TRACK_CHI2NDOF', 'mu_prim_TRACK_CHI2NDOF', 'N_ENDVERTEX_CHI2', \
                 'N_IPCHI2_OWNPV', 'N_TAU', 'N_MM','N_PX', 'N_PY', 'N_PZ', 'N_PE','mu_prim_PX','mu_prim_PY', \
                 'mu_prim_PZ', 'mu_prim_PE', 'mu_sec_PX', 'mu_sec_PY', 'mu_sec_PZ', 'mu_sec_PE', 'mu_sec_M', 'mu_prim_M', \
                 'pi_PX', 'pi_PY', 'pi_PZ', 'pi_PE', 'pi_TRUEID', 'mu_sec_TRUEID', 'mu_prim_TRUEID', 'B_FDCHI2_OWNPV', \
                 'mu_prim_IPCHI2_OWNPV', 'mu_sec_IPCHI2_OWNPV', 'pi_IPCHI2_OWNPV',  'mu_sec_isMuon' ,'mu_prim_isMuon', 'mu_prim_TRACK_GhostProb',\
                 'mu_sec_TRACK_GhostProb', 'pi_TRACK_GhostProb', 'pi_isMuon', 'B_FD_OWNPV', 'B_FDCHI2_OWNPV', 'pi_PT',\
                 'mu_prim_PIDp','mu_sec_PIDp', 'mu_sec_PIDK', 'mu_prim_PIDK',  'pi_ProbNNk', 'pi_ProbNNpi','B_BKGCAT']
               
vars_PID     = ['mu_prim_PIDmu', 'mu_sec_PIDmu', 'pi_PIDmu', 'pi_PIDK', 'pi_PIDp', \
               'pi_MC12TuneV2_ProbNNk', 'mu_prim_MC12TuneV2_ProbNNk', 'mu_sec_MC12TuneV2_ProbNNk','pi_MC12TuneV3_ProbNNk', \
               'mu_prim_MC12TuneV3_ProbNNk', 'mu_sec_MC12TuneV3_ProbNNk',  'pi_MC12TuneV2_ProbNNpi',\
               'mu_prim_MC12TuneV2_ProbNNpi', 'mu_sec_MC12TuneV2_ProbNNpi','pi_MC12TuneV3_ProbNNpi', 'mu_prim_MC12TuneV3_ProbNNpi',\
               'mu_sec_MC12TuneV3_ProbNNpi', 'pi_PIDmu', 'pi_PIDK', 'pi_PIDp', 'mu_prim_MC12TuneV3_ProbNNmu','mu_sec_MC12TuneV3_ProbNNmu']

vars_PIDuncorr = ['pi_MC12TuneV2_ProbNNk', 'pi_MC12TuneV3_ProbNNk', 'mu_prim_MC12TuneV3_ProbNNk', \
                'mu_sec_MC12TuneV3_ProbNNk', 'pi_MC12TuneV2_ProbNNpi', 'pi_MC12TuneV3_ProbNNpi', \
                'mu_prim_MC12TuneV3_ProbNNpi','mu_sec_MC12TuneV3_ProbNNpi', \
                'pi_PIDmu', 'pi_PIDK', 'pi_PIDp',  'mu_prim_PIDmu', 'mu_sec_PIDmu',  \
                'mu_prim_MC12TuneV3_ProbNNmu','mu_sec_MC12TuneV3_ProbNNmu']

vars_PIDcorr = ['pi_MC12TuneV2_ProbNNk_corr', 'pi_MC12TuneV3_ProbNNk_corr', 'mu_prim_MC12TuneV3_ProbNNk_corr', \
                'mu_sec_MC12TuneV3_ProbNNk_corr', 'pi_MC12TuneV2_ProbNNpi_corr', 'pi_MC12TuneV3_ProbNNpi_corr', \
                'mu_prim_MC12TuneV3_ProbNNpi_corr','mu_sec_MC12TuneV3_ProbNNpi_corr', \
                'pi_PIDmu_corr', 'pi_PIDK_corr', 'pi_PIDp_corr',  'mu_prim_PIDmu_corr', 'mu_sec_PIDmu_corr',  \
                'mu_prim_MC12TuneV3_ProbNNmu_corr','mu_sec_MC12TuneV3_ProbNNmu_corr']

trig_string  = '((B_L0MuonDecision_TOS == True) | (B_L0DiMuonDecision_TOS == True)) \
                & ((B_Hlt1TrackMuonDecision_TOS == True) | (B_Hlt1TrackAllL0Decision_TOS ==True)) \
                & ((B_Hlt2TopoMu2BodyBBDTDecision_TOS == True) | (B_Hlt2TopoMu3BodyBBDTDecision_TOS == True))'

truth_string = '((B_TRUEID == 541.) | (B_TRUEID == -541.)|(B_TRUEID == -521.)|(B_TRUEID == -521.))\
                & ((pi_TRUEID == 211.) | (pi_TRUEID == -211.))\
                & ((mu_prim_TRUEID == -13.)|(mu_prim_TRUEID == 13.))\
                & ((mu_sec_TRUEID == -13.)|(mu_sec_TRUEID == 13.)) & (B_BKGCAT <= 20.0) '

truth_stringrho0  = '((B_TRUEID == 511.) | (B_TRUEID == -511.)) &  ((pi_TRUEID == 211.) | (pi_TRUEID == -211.))\
                    &((mu_prim_TRUEID == -13.)|(mu_prim_TRUEID == 13.)) & ((mu_sec_TRUEID == -13.)|(mu_sec_TRUEID == 13.))\
                    &((B_BKGCAT == 40.0) | (B_BKGCAT == 50.0))'

truth_string = '((B_TRUEID == 541.) | (B_TRUEID == -541.)|(B_TRUEID == -521.)|(B_TRUEID == -521.))\
                & ((pi_TRUEID == 321.) | (pi_TRUEID == -321.))\
                & ((mu_prim_TRUEID == -13.)|(mu_prim_TRUEID == 13.))\
                & ((mu_sec_TRUEID == -13.)|(mu_sec_TRUEID == 13.))'

preselection = '((mu_prim_isMuon == 1.0) & (mu_sec_isMuon == 1.0) & (pi_isMuon == 0.0) ) \
               & (mu_prim_PT > 300.0) & (mu_sec_PT > 300.0) & (pi_PT > 300.0) & (B_PT > 300.0) '

pid_string   = '(pi_MC12TuneV3_ProbNNk < 0.04) & (mu_prim_MC12TuneV3_ProbNNmu > 0.2) & (mu_sec_MC12TuneV3_ProbNNmu > 0.2) \
                & (mu_prim_MC12TuneV3_ProbNNk < 0.4) & (mu_sec_MC12TuneV3_ProbNNk < 0.4) '


"""""""""""""""""""""""
Load DATA &  MC 

"""""""""""""""""""""""

print "Loading DATA"

for f in BKG_Files:
    try:
        file_path = f.resolve()
    except FileNotFoundError:
        print("File doesn't exist yet")
    else:
        mc_read = read_root(file_path+str(f) , key = treeraw, columns = variables+vars_uncorrPID)
        print("mc_read: {}".format(len(mc_read)))
        for key, values in BKG_Files.iteritems():
            mc_selected = mc_read.query(trig_string + '&' + preselection + '&' + pid_string + '&' + values[4]).copy()
            print("DATA Read after Trigger- and Pre-Selection {} ".format(len(mc_selected)))
            mc_selected.to_root('Preselected_{}'.format(f), key='DecayTree', mode='a')

    
