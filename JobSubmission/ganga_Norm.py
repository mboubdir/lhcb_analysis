
import sys
import os

mport sys
import os

j= Job(backend=Dirac())
#DaVinci_dirname = './DaVinciDev_v42r6p1'
DaVinci_dirname = "."
if os.path.exists(DaVinci_dirname): myApp = GaudiExec()
else: myApp = prepareGaudiExec('DaVinci', 'v42r6p1', '/afs/cern.ch/user/m/mboubdir/DaVinciDev_v42r6p1')
myApp.directory = "."
j.application= myApp


j.name = 'MC16NormChan'

#pol = 'Up'
pol = 'Down'
BK_locations = []

#MC16_norm = '/MC/2016/12143010/Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping26NoPrescalingFlagged/ALLSTREAMS.MDST'

#MC16N_NormChan = 'MC/2016/Beam6500GeV-2016-MagUp-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping26NoPrescalingFlagged/12143010/ALLSTREAMS.MDST'
#for pol in pols:
if pol is 'Down':
    j.application.extraopts="DaVinci().CondDBtag = 'sim-20161124-2-vc-md100'"
    BK_locations= 'MC/2016/Beam6500GeV-2016-Mag'+pol+'-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping26NoPrescalingFlagged/12143010/ALLSTREAMS.MDST'
elif pol is 'Up':
    j.application.extraopts="DaVinci().CondDBtag = 'sim-20161124-2-vc-mu100'"
    BK_locations= '/MC/2016/Beam6500GeV-2016-Mag'+pol+'-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping26NoPrescalingFlagged/12143010/ALLSTREAMS.MDST'
else:
    print "CondDBtag missing"
    
j.application.extraopts="DaVinci().DDDBtag = 'dddb-20150724'"


data = BKQuery(filepath, dqflag=['All']).getDataset()
    
j.application.options = ['/afs/cern.ch/user/m/mboubdir/scratch1/tools/Analysisfiles/python_files/MC16RunStrip.py']

j.backend = Dirac()
j.name = '16MC_'+pol+'NormChan_strip28' 
j.inputdata = data
#j.inputfiles  = [LocalFile(local_dir + "/weights_110614_Lc_pX.xml")]

j.splitter = SplitByFiles(filesPerJob=5)
j.splitter.bulksubmit = False
j.do_auto_resubmit = True
#j.parallel_submit = True

#j.application.extraopts="DaVinci().TupleFile= '{}_B2LambdaMu.root'".format(EventType)
j.outputfiles = [LocalFile(namePattern='*.root')]

j.submit()
