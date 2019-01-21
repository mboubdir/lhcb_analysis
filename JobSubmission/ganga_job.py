import sys
import os

pol = 'Down'
#pol = 'Up'

j= Job(backend=Dirac())
DaVinci_dirname = './DaVinciDev_v42r6p1'
if os.path.exists(DaVinci_dirname): myApp = GaudiExec()
else: myApp = prepareGaudiExec('DaVinci', 'v42r6p1', '/afs/cern.ch/user/m/mboubdir/DaVinciDev_v42r6p1')
myApp.directory = "."
j.application= myApp
#j.application.platform = ['x86_64-centos7-gcc62-opt']
j.application.options = ['./RestripB2XMuMuLinePromptMajorana.py']


#DATA 2011 stripping 21r1
#filepath = '/LHCb/Collision11/Beam3500GeV-VeloClosed-Mag'+pol+'/Real Data/Reco14/Stripping21r1/90000000/LEPTONIC.MDST'
#DATA 2012 stripping 21
filepath = '/LHCb/Collision12/Beam4000GeV-VeloClosed-Mag'+pol+'/Real Data/Reco14/Stripping21/90000000/LEPTONIC.MDST'
#DATA 2015 stripping 24 / 24r1p1
#filepath = '/LHCb/Collision15/Beam6500GeV-VeloClosed-Mag'+pol+'/Real Data/Reco15a/Stripping24r1p1/90000000/LEPTONIC.MDST'
#filepath = '/LHCb/Collision15/Beam6500GeV-VeloClosed-Mag'+pol+'/Real Data/Reco15a/Stripping24r1p1/90000000/LEPTONIC.MDST'
#DATA 2016 stripping 28
#filepath  = '/LHCb/Collision16/Beam6500GeV-VeloClosed-Mag'+pol+'/Real Data/Reco16/Stripping28/90000000/LEPTONIC.MDST'

data = BKQuery(filepath, dqflag=['All']).getDataset()
#j.inputfiles  = [LocalFile(local_dir + "/weights_110614_Lc_pX.xml")]
j.inputdata = data
j.name = '12DATA'+pol+'Prompt_strip21'

j.splitter = SplitByFiles(filesPerJob=50)
j.splitter.bulksubmit = False 
j.do_auto_resubmit = True
j.parallel_submit = True
#j.application.extraOpts="DaVinci().TupleFile= '15DATA{}_Prompt_B2XMuMu_strip24r1p1.root'".format(pol)

j.outputfiles = [DiracFile(namePattern='*.root')]

j.submit()
