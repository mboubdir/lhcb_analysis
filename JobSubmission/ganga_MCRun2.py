import sys
import os

local_dir = "/afs/cern.ch/user/m/mboubdir/scratch1/tools/Analysisfiles/python_files"

v = 'v41r3'
dv = DaVinci(version=v)
j = Job(application=DaVinci(version=v))

#Bu -> N(3GeV, 100ps) mu for 2016
#EventType = '12113011'

year = ['2015', '2016']
pols = ['Down', 'Up']
BK_locations = []

MC15_NormChan  = '/MC/2015/Beam6500GeV-2015-Mag'+pols[0]+'-Nu1.6-25ns-Pythia8/Sim09b/Trig0x411400a2/Reco15a/Turbo02/Stripping24NoPrescalingFlagged/12143010/ALLSTREAMS.DST'
MC16_NormChan  = 'MC/2016/Beam6500GeV-2016-Mag'+pols[0]+'-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/Turbo03/Stripping26NoPrescalingFlagged/12143010/ALLSTREAMS.MDST'

for pol in pols:
    if pol is 'Down':
        j.application.extraopts="DaVinci().CondDBtag = 'sim-20161124-2-vc-md100'"
        BK_locations= ['/MC/2016/Beam6500GeV-2016-Mag'+pol+'-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/12113011/LDST']
    elif pol is 'Up':
        j.application.extraopts="DaVinci().CondDBtag = 'sim-20161124-2-vc-mu100'"
        BK_locations.append('/MC/2016/Beam6500GeV-2016-Mag'+pol+'-Nu1.6-25ns-Pythia8/Sim09b/Trig0x6138160F/Reco16/12113011/LDST')
    else:
        print "CondDBtag missing"
    
j.application.extraopts="DaVinci().DDDBtag = 'dddb-20150724'"
j.name = 'MC%sNormChan'%year[0]

#Bu -> N(3GeV, 100ps) mu for 2016
data = LHCbDataset()
bk = BKQuery()
for path in BK_locations:
    bk.path = path
    tmp = bk.getDataset()
    print path , len(tmp.files)
    if len(tmp.files) > 0:
        data.extend(tmp)

print data

if len(data.files) < 1:
    sys.exit()
    
j.inputdata = data

j.application.optsfile = ['/afs/cern.ch/user/m/mboubdir/scratch1/tools/Analysisfiles/python_files/MC16RunStrip.py']

j.backend = Dirac()
j.inputdata = data
#j.inputfiles  = [LocalFile(local_dir + "/weights_110614_Lc_pX.xml")]

j.splitter = SplitByFiles(filesPerJob=5)
j.splitter.bulksubmit = False
j.do_auto_resubmit = True
j.parallel_submit = True

#j.application.extraopts="DaVinci().TupleFile= '{}_B2LambdaMu.root'".format(EventType)
j.outputfiles = [LocalFile(namePattern='*.root')]

j.submit()
