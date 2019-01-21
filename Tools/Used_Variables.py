###########################################################
###########Define variables and Cuts needed################
###########################################################

import ROOT
import pandas as pd
import numpy as np


#########################################################
################Files to read############################
#########################################################
Data_year        = ['11', '12', '15', '16']
Polarity         = ['Up', 'Down']
selection       = ['NormChan', 'PromptN', 'DetachedN']

NormChan_path    = '/Users/mboubdir/Desktop/repository/MajoranaAnalysis/ROOT_Files/'+selection[0]+'/'
PromptN_path     = '/Users/mboubdir/Desktop/repository/MajoranaAnalysis/ROOT_Files/'+selection[1]+'/'
DetachedN_path   = '/Users/mboubdir/Desktop/repository/MajoranaAnalysis/ROOT_Files/'+selection[2]+'/'

def Input_Data(file_path, year, selec):
    input_ = []
    for x in year:
        if '11' in year:
            input_ = file_path+'DATA/'+year+'DATA_' + selec + '_strip21r1.root'
        elif '12' in year:
            input_.append(file_path+'DATA/'+year+'DATA_' + selec + '_strip21.root')
        elif '15' in year:
            input_.append(file_path+'DATA/'+year+'DATA_' + selec + '_strip24.root')
        else:
            input_.append(file_path+'DATA/'+year+'DATA_' + selec + '_strip28.root')

    return input_

var_SDATA    = ['B_MM', 'B_PT', 'B_ETA', 'B_PT', 'nTracks', 'nSig_sw']

vars_Toreweight = ['nTracks', 'B_PT', 'B_ETA', 'B_ENDVERTEX_CHI2']
        
variables     = ['B_MM', 'B_PT', 'B_TAU', 'B_ETA', 'B_PT', 'nTracks',  'B_L0MuonDecision_TOS', 'B_L0DiMuonDecision_TOS', 'B_Hlt1TrackMuonDecision_TOS', \
                 'B_Hlt1TrackAllL0Decision_TOS', 'B_Hlt2TopoMu2BodyBBDTDecision_TOS', 'B_Hlt2TopoMu3BodyBBDTDecision_TOS', \
                 'mu_sec_isMuon', 'mu_prim_isMuon', 'pi_ProbNNk', 'pi_ProbNNpi','B_TRUEID', \
                 'B_ENDVERTEX_CHI2', 'B_ENDVERTEX_NDOF', 'B_IPCHI2_OWNPV', 'B_DIRA_OWNPV', 'mu_sec_P', 'mu_prim_P','B_FD_OWNPV',\
                 'mu_sec_PT', 'mu_prim_PT', 'mu_sec_TRACK_CHI2NDOF', 'mu_prim_TRACK_CHI2NDOF', 'mu_prim_PX','mu_prim_PY', \
                 'mu_prim_PZ', 'mu_prim_PE', 'mu_sec_PX', 'mu_sec_PY', 'mu_sec_PZ', 'mu_sec_PE', 'mu_sec_M', 'mu_prim_M', \
                 'pi_PX', 'pi_PY', 'pi_PZ', 'pi_PE', 'pi_TRUEID', 'mu_sec_TRUEID', 'mu_prim_TRUEID', 'B_FDCHI2_OWNPV', \
                 'mu_prim_IPCHI2_OWNPV', 'mu_sec_IPCHI2_OWNPV', 'pi_IPCHI2_OWNPV',  'mu_sec_isMuon' ,'mu_prim_isMuon', 'mu_prim_TRACK_GhostProb',\
                 'mu_sec_TRACK_GhostProb', 'pi_TRACK_GhostProb', 'pi_isMuon', 'B_FD_OWNPV', 'B_FDCHI2_OWNPV', 'pi_PT','pi_InAccMuon',\
                 'mu_prim_PIDp','mu_sec_PIDp', 'mu_sec_PIDK', 'mu_prim_PIDK',  'pi_ProbNNk', 'pi_ProbNNpi','B_BKGCAT', 'B_ETA', 'nSPDHits']


Cuts_variables = ['B_L0MuonDecision_TOS', 'B_L0DiMuonDecision_TOS', 'B_Hlt1TrackMuonDecision_TOS',\
                  'B_Hlt1TrackAllL0Decision_TOS', 'B_Hlt2TopoMu2BodyBBDTDecision_TOS', 'B_Hlt2TopoMu3BodyBBDTDecision_TOS',\
                  'mu_sec_isMuon', 'mu_prim_isMuon', 'pi_isMuon', 'pi_InAccMuon', 'B_DIRA_OWNPV']

Prompt_N_vars = ['N_1_TAU', 'N_1_MM', 'N_2_TAU', 'N_2_MM',  'N_1_PX', 'N_1_PY', 'N_1_PZ', 'N_1_PE', 'N_2_PX', 'N_2_PY', 'N_2_PZ', 'N_2_PE', \
                 'B_VTXISOBDTHARDFIRSTVALUE']

NormChan_N_vars = ['N_TAU', 'N_MM','N_PX', 'N_PY', 'N_PZ', 'N_PE','B_VTXISOBDTHARDFIRSTVALUE']

Detached_N_vars = ['B_ISOLATION_BDT_Hard']

vars_PID     = ['pi_MC12TuneV3_ProbNNpi', 'pi_MC12TuneV3_ProbNNk',\
                'mu_prim_MC12TuneV3_ProbNNk', 'mu_sec_MC12TuneV3_ProbNNk', \
                'mu_prim_MC12TuneV2_ProbNNpi', 'mu_sec_MC12TuneV2_ProbNNpi',\
                'mu_prim_MC12TuneV3_ProbNNpi','mu_sec_MC12TuneV3_ProbNNpi', \
                'mu_prim_MC12TuneV3_ProbNNmu','mu_sec_MC12TuneV3_ProbNNmu',\
                'mu_prim_PIDmu', 'mu_sec_PIDmu', 'pi_PIDmu', 'pi_PIDK', 'pi_PIDp']

vars_PIDuncorr = ['pi_MC12TuneV3_ProbNNpi', 'pi_MC12TuneV3_ProbNNk', \
                  'mu_prim_MC12TuneV3_ProbNNk', 'mu_sec_MC12TuneV3_ProbNNk', \
                  'mu_prim_MC12TuneV3_ProbNNpi','mu_sec_MC12TuneV3_ProbNNpi', \
                  'mu_prim_MC12TuneV3_ProbNNmu','mu_sec_MC12TuneV3_ProbNNmu']

vars_PIDcorr   = ['pi_MC12TuneV3_ProbNNpi_corr', 'pi_MC12TuneV3_ProbNNk_corr', \
                  'mu_prim_MC12TuneV3_ProbNNk_corr', 'mu_sec_MC12TuneV3_ProbNNk_corr', \
                  'mu_prim_MC12TuneV3_ProbNNpi_corr','mu_sec_MC12TuneV3_ProbNNpi_corr', \
                  'mu_prim_MC12TuneV3_ProbNNmu_corr','mu_sec_MC12TuneV3_ProbNNmu_corr']

vars_PIDcorr_v2 = ['pi_MC12TuneV3_ProbNNpi_corr', 
                     'pi_MC12TuneV3_ProbNNk_corr', 
                     'pi_MC12TuneV2_ProbNNpi_corr', 
                     'pi_MC12TuneV2_ProbNNk_corr', 
                     'mu_prim_MC12TuneV3_ProbNNk_corr',
                     'mu_prim_MC12TuneV3_ProbNNpi_corr',
                     'mu_prim_MC12TuneV3_ProbNNmu_corr',
                     'mu_sec_MC12TuneV3_ProbNNmu_corr',
                     'mu_sec_MC12TuneV3_ProbNNpi_corr',
                     'mu_sec_MC12TuneV3_ProbNNk_corr']
                     
vars_PIDuncorr_v2 = list(map(lambda x: x.replace('_corr', ''), vars_PIDcorr_v2))

trig_string  = '((B_L0MuonDecision_TOS == True) | (B_L0DiMuonDecision_TOS == True)) \
                & ((B_Hlt1TrackMuonDecision_TOS == True) | (B_Hlt1TrackAllL0Decision_TOS ==True)) \
                & ((B_Hlt2TopoMu2BodyBBDTDecision_TOS == True) | (B_Hlt2TopoMu3BodyBBDTDecision_TOS == True))'

truth_string = '((B_TRUEID == 541.) | (B_TRUEID == -541.)|(B_TRUEID == -521.)|(B_TRUEID == -521.))\
                & ((pi_TRUEID == 211.) | (pi_TRUEID == -211.))\
                & ((mu_prim_TRUEID == -13.)|(mu_prim_TRUEID == 13.))\
                & ((mu_sec_TRUEID == -13.)|(mu_sec_TRUEID == 13.)) & (B_BKGCAT <= 20.0) '


truth_stringrho0  = '((B_TRUEID == 511.) | (B_TRUEID == -511.)) & ((pi_TRUEID == 211.) | (pi_TRUEID == -211.))\
                    &((mu_prim_TRUEID == -13.)|(mu_prim_TRUEID == 13.)) & ((mu_sec_TRUEID == -13.)|(mu_sec_TRUEID == 13.))\
                    &((B_BKGCAT == 40.0) | (B_BKGCAT == 50.0))'

Kin_Particle_Pre = '((mu_prim_isMuon == 1.0) & (mu_sec_isMuon == 1.0) & (pi_isMuon == 0.0) & (pi_InAccMuon == 1.0) & (B_DIRA_OWNPV > 0.999))'

pid_string   = '(mu_prim_MC12TuneV3_ProbNNmu > 0.2) & (mu_sec_MC12TuneV3_ProbNNmu > 0.2) \
               & (mu_prim_MC12TuneV3_ProbNNpi < 0.4) & (mu_sec_MC12TuneV3_ProbNNpi < 0.4) \
               & (mu_prim_MC12TuneV3_ProbNNk < 0.4) & (mu_sec_MC12TuneV3_ProbNNk < 0.4) \
               & (pi_MC12TuneV3_ProbNNpi >0.4) & (pi_MC12TuneV3_ProbNNk < 0.1)'


pid_string_corr_Loose = '((mu_prim_MC12TuneV3_ProbNNmu_corr >  0.2) & (mu_sec_MC12TuneV3_ProbNNmu_corr >  0.2) \
                      & (mu_prim_MC12TuneV3_ProbNNpi_corr < 0.4) & (mu_sec_MC12TuneV3_ProbNNpi_corr < 0.4) \
                      & (mu_prim_MC12TuneV3_ProbNNk_corr < 0.4) & (mu_sec_MC12TuneV3_ProbNNk_corr < 0.4) \
                      & (pi_MC12TuneV3_ProbNNpi_corr > 0.2) & (pi_MC12TuneV3_ProbNNk_corr < 0.4))'

pid_string_corr_new1 = '((mu_prim_MC12TuneV3_ProbNNmu_corr >  0.2) & (mu_sec_MC12TuneV3_ProbNNmu_corr >  0.2) \
                      & (mu_prim_MC12TuneV3_ProbNNpi_corr < 0.4) & (mu_sec_MC12TuneV3_ProbNNpi_corr < 0.4) \
                      & (mu_prim_MC12TuneV3_ProbNNk_corr < 0.4) & (mu_sec_MC12TuneV3_ProbNNk_corr < 0.4) \
                      & (pi_MC12TuneV3_ProbNNpi_corr > 0.4) & (pi_MC12TuneV3_ProbNNk_corr < 0.2))'



pid_string_corr_new1_5 = '((mu_prim_MC12TuneV3_ProbNNmu_corr >  0.2) & (mu_sec_MC12TuneV3_ProbNNmu_corr >  0.2) \
                      & (mu_prim_MC12TuneV3_ProbNNpi_corr < 0.4) & (mu_sec_MC12TuneV3_ProbNNpi_corr < 0.4) \
                      & (mu_prim_MC12TuneV3_ProbNNk_corr < 0.4) & (mu_sec_MC12TuneV3_ProbNNk_corr < 0.4) \
                      & (pi_MC12TuneV3_ProbNNpi_corr > 0.4) & (pi_MC12TuneV3_ProbNNk_corr < 0.15))'

pid_string_corr_new2 = '((mu_prim_MC12TuneV3_ProbNNmu_corr >  0.2) & (mu_sec_MC12TuneV3_ProbNNmu_corr >  0.2) \
                      & (mu_prim_MC12TuneV3_ProbNNpi_corr < 0.4) & (mu_sec_MC12TuneV3_ProbNNpi_corr < 0.4) \
                      & (mu_prim_MC12TuneV3_ProbNNk_corr < 0.4) & (mu_sec_MC12TuneV3_ProbNNk_corr < 0.4) \
                      & (pi_MC12TuneV2_ProbNNpi_corr > 0.4) & (pi_MC12TuneV2_ProbNNk_corr < 0.1))'

pid_string_corr_v2_new2 = '((mu_prim_MC12TuneV3_ProbNNmu_corr >  0.2) & (mu_sec_MC12TuneV3_ProbNNmu_corr >  0.2) \
                      & (mu_prim_MC12TuneV3_ProbNNpi_corr < 0.4) & (mu_sec_MC12TuneV3_ProbNNpi_corr < 0.4) \
                      & (mu_prim_MC12TuneV3_ProbNNk_corr < 0.4) & (mu_sec_MC12TuneV3_ProbNNk_corr < 0.4) \
                      & (pi_MC12TuneV2_ProbNNpi_corr > 0.4) & (pi_MC12TuneV2_ProbNNk_corr < 0.1))'

pid_string_corr_new3 = '((mu_prim_MC12TuneV3_ProbNNmu_corr >  0.2) & (mu_sec_MC12TuneV3_ProbNNmu_corr >  0.2) \
                      & (mu_prim_MC12TuneV3_ProbNNpi_corr < 0.4) & (mu_sec_MC12TuneV3_ProbNNpi_corr < 0.4) \
                      & (mu_prim_MC12TuneV3_ProbNNk_corr < 0.4) & (mu_sec_MC12TuneV3_ProbNNk_corr < 0.4) \
                      & (pi_MC12TuneV3_ProbNNpi_corr > 0.4) & (pi_MC12TuneV3_ProbNNk_corr < 0.05))'

pid_string_Loose = pid_string_corr_Loose.replace('_corr', '')
pid_string_new1 = pid_string_corr_new1.replace('_corr', '')
pid_string_new1_5 = pid_string_corr_new1_5.replace('_corr', '')
pid_string_new2 = pid_string_corr_new2.replace('_corr', '')
pid_string_v2_new2 = pid_string_corr_v2_new2.replace('_corr', '')
pid_string_new3 = pid_string_corr_new3.replace('_corr', '')

PromptN_SIG_dict  = {
                  '12113008': ('$B^{+} \; -> \;  N(3GeV, 0ps) \mu^{+} $' , '528121' , 'Stripping21' , 'sim9a', 'B_BKGCAT <= 20.'),
                  #'12113013': ('$B^{+} \; -> \;  N(1GeV, 0ps) \mu^{+} $' , 570697 , 'Stripping21' , 'sim9a', 'B_BKGCAT <= 20.'),
                  '12113014': ('$B^{+} \; -> \;  N(2GeV, 0ps) \mu^{+} $' , '503892' , 'Stripping21' , 'sim9b', 'B_BKGCAT <= 20.'),
                  '12113015': ('$B^{+} \; -> \;  N(4GeV, 0ps) \mu^{+} $' , '511234' , 'Stripping21' , 'sim9b', 'B_BKGCAT <= 20.'),
                  '12113016': ('$B^{+} \; -> \;  N(4.5GeV, 0ps) \mu^{+} $' , 506502 , 'Stripping21' , 'sim9b', 'B_BKGCAT <= 20.'),
                  '12113017': ('$B^{+} \; -> \;  N(5GeV, 0ps) \mu^{+} $' , 554221 , 'Stripping21' , 'sim9b', 'B_BKGCAT <= 20.'),
                  #'14113002': ('$ B_{c}^{+} \; -> \;  N(1GeV, 0ps) \mu^{+} $' , 562341 , 'Stripping21' , 'sim9a', 'B_BKGCAT <= 20.'),
                  '14113003': ('$ B_{c}^{+} \; -> \;  N(2GeV, 0ps) \mu^{+} $' , 542465 , 'Stripping21' , 'sim9b', 'B_BKGCAT <= 20.'),
                  '14113004': ('$ B_{c}^{+} \; -> \;  N(3GeV, 0ps) \mu^{+} $' , 549742 , 'Stripping21' , 'sim9a', 'B_BKGCAT <= 20.'),
                  '14113008': ('$ B_{c}^{+} \; -> \;  N(4GeV, 0ps) \mu^{+} $' , 507304 , 'Stripping21' , 'sim9b', 'B_BKGCAT <= 20.'),
                  '14113009': ('$ B_{c}^{+} \; -> \;  N(5GeV, 0ps) \mu^{+} $' , 507734 , 'Stripping21' , 'sim9b', 'B_BKGCAT <= 20.'),
                  '14113010': ('$ B_{c}^{+} \; -> \;  N(5.5GeV, 0ps) \mu^{+} $' ,241276 , 'Stripping21' , 'sim9a', 'B_BKGCAT <= 20.'),
                  #'14113014': ('$ B_{c}^{+} \; -> \;  N(6GeV, 0ps) \mu^{+} $' , 'Requested' , 'Stripping21' , 'sim9b', 'B_BKGCAT <= 20.')
                }


DetachedN_SIG_dict  = {
                  '12113009': ('$B^{+} \; -> \;  N(3GeV, 1ps) \mu^{+} $' , 507830 , 'Stripping21' , 'sim9b', 'B_BKGCAT < 20.', False),
                  '12113010': ('$B^{+} \; -> \;  N(3GeV, 10ps) \mu^{+} $' , 586874 , 'Stripping21' , 'sim9a', 'B_BKGCAT < 20.', False),
                  '12113011': ('$B^{+} \; -> \;  N(3GeV, 100ps) \mu^{+} $' , 511900 , 'Stripping21' , 'sim9b', 'B_BKGCAT < 20.', False),
                  '14113000': ('$ B_{c}^{+} \; -> \;  N(3GeV, 10ps) \mu^{+} $' , 540290 , 'Stripping21' , 'sim9a', 'B_BKGCAT < 20.', False),
                  '14113005': ('$ B_{c}^{+} \; -> \;  N(3GeV, 1ps) \mu^{+} $' , 503337 , 'Stripping21' , 'sim9b', 'B_BKGCAT < 20.', False),
                  '14113007': ('$ B_{c}^{+} \; -> \;  N(3GeV, 100ps) \mu^{+} $' , 608097 , 'Stripping21' , 'sim9b', 'B_BKGCAT < 20.', False),
                  '14113011': ('$ B_{c}^{+} \; -> \;  N(5.5GeV, 1ps) \mu^{+} $' , 508488 , 'Stripping21' , 'sim9b', 'B_BKGCAT < 20.', False),
                  '14113012': ('$ B_{c}^{+} \; -> \;  N(5.5GeV, 10ps) \mu^{+} $' , 1110234 , 'Stripping21' , 'sim9b', 'B_BKGCAT < 20.', False),
                  '14113013': ('$ B_{c}^{+} \; -> \;  N(5.5GeV, 100ps) \mu^{+} $' , 547894 , 'Stripping21' , 'sim9b', 'B_BKGCAT < 20.', False),
                 }

SIG_files_PromptN     = ['%s_B2XMuMu_strip21_Resampled.root' % key for key in PromptN_SIG_dict]
SIG_files_DetachedN   = ['%s_B2LambdaMu_strip21_Resampled.root' % key for key in DetachedN_SIG_dict]

df_EventType_PromptN  = ['%s_df_PrN' % key for key in PromptN_SIG_dict]
df_EventType_DetachedN  = ['%s_df_DeN' % key for key in DetachedN_SIG_dict]

SIG_df_dict_PromptN   = dict(zip(df_EventType_PromptN, SIG_files_PromptN))
SIG_df_dict_DetachedN   = dict(zip(df_EventType_DetachedN, SIG_files_DetachedN))


