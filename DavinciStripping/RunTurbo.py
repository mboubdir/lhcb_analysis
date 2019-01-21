the_year = '2016'

rootInTES = '/Event/Turbo'
the_line  = 'B2XMuMu_Line/Particles'

## use pre-filters to speedup
from PhysConf.Filters import LoKi_Filters
fltrs = LoKi_Filters (
        VOID_Code = """
            0 < CONTAINS('%s/%s')
                """ % ( rootInTES , the_line )
            )
from Configurables import DstConf, TurboConf

DstConf().Turbo = True
TurboConf().PersistReco = True

##################Resstrping###################################

from Configurables import EventNodeKiller
eventNodeKiller = EventNodeKiller('Stripkiller')
eventNodeKiller.Nodes = [ '/Event/AllStreams', '/Event/Strip' ]

from StrippingConf.Configuration import StrippingConf
from StrippingConf.StrippingStream import StrippingStream

from StrippingArchive.Stripping28.StrippingRD.StrippingB2XMuMu import B2XMuMuConf

from StrippingSettings.Stripping28.LineConfigDictionaries_RD import B2XMuMu
from PhysSelPython.Wrappers import AutomaticData, Selection, SelectionSequence
#from Configurables import DstConf, TurboConf

B2XMuMuConf = B2XMuMuConf("B2XMuMu", B2XMuMu['CONFIG'])
B2XMuMuLines = B2XMuMuConf.lines()
for line in B2XMuMuLines:
        print "CL DEBUG", line
        print "CL DEBUG", line.name()
stripline = B2XMuMuLines[0]

sstream = StrippingStream("TestStream")
sstream.appendLines([stripline])
sstream.OutputLevel = 2

sc = StrippingConf(
	  Streams=[sstream],
	    HDRLocation="DecReports",
	  )

Strip_Location1 = stripline.outputLocation()
print Strip_Location1
StripSel1 = AutomaticData(Location = Strip_Location1)
print StripSel1
print StripSel1.outputLocation()
print "ALL OK"
            
###########################################################
decay     = "[B+  -> ^( J/psi(1S)  -> ^mu-  ^mu+) ^pi+]CC"
############################################################

## (1) read data from Turbo: 
from PhysConf.Selections import AutomaticData
Bu = AutomaticData(the_line)

## (2) get pions form PersistReco 
from StandardParticles import StdAllNoPIDsMuons as muons
## I.3.1   IMPOTANT: need to rebuild it!!
from PhysConf.Selections import RebuildSelection
muons = RebuildSelection ( muons )

#PROBNNmu not available in 2015 Turbo(++)

from Configurables import CondDB
CondDB ( LatestGlobalTagByDataType = the_year ) 

## (5) fill tuple
from Configurables import DecayTreeTuple, TupleToolPrimaries
tuple = DecayTreeTuple("DecayTree")
tuple.Inputs = [StripSel1.outputLocation()]
tuple.Decay = decay
tuple.ToolList = [
    "TupleToolKinematic",
    "TupleToolPid",
    "TupleToolANNPID",
    "TupleToolPropertime",
    "TupleToolGeometry",
    "TupleToolPrimaries",
    "TupleToolTrackInfo",
    "TupleToolEventInfo",
    "TupleToolRecoStats"#,
    ]
tuple.Branches = {
    "B"       : "[B+ -> ( J/psi(1S)  -> mu-  mu+ ) pi+ ]CC",
    "Jpsi"    : "[B+ -> ^(J/psi(1S)  -> mu-  mu+) pi+]CC",
    "mu_prim" : "[B+ -> (J/psi(1S) -> mu- ^mu+) pi+]CC",
    "mu_sec"  : "[B+ -> (J/psi(1S) -> ^mu- mu+) pi+]CC",
    "pi"      : "[B+ -> (J/psi(1S) -> mu- mu+) ^pi+]CC",
        }
########################################################################
from Configurables import TupleToolGeometry
tuple.addTool( TupleToolGeometry, name = "TupleToolGeometry" )
tuple.TupleToolGeometry.Verbose = True

from Configurables import TupleToolRecoStats
tuple.addTool(TupleToolRecoStats, name="TupleToolRecoStats")
tuple.TupleToolRecoStats.Verbose = True

from Configurables import TupleToolDecay
tuple.addTool(TupleToolDecay, name = 'Bu')
from Configurables import LoKi__Hybrid__TupleTool
#tuple.Bu.ToolList =  ["LoKi::Hybrid::TupleTool/LoKi_All0"]
###################################################################
'''
LoKiTuple0 = LoKi__Hybrid__TupleTool("LoKi_All0")
LoKiTuple0.Variables =  {
    "M_DTF_PV":"DTF_FUN( M, True )"
    ,"CHI2NDOF_DTF_PV":"DTF_CHI2NDOF(True)"
    ,"M12_DTF_Ds_PV":"DTF_FUN( M12, True, strings( 'D_s+') )"
    ,"M13_DTF_Ds_PV":"DTF_FUN( M13, True, strings( 'D_s+') )"
    ,"M23_DTF_Ds_PV":"DTF_FUN( M23, True, strings( 'D_s+') )"
    ,"CHI2NDOF_DTF_Ds_PV":"DTF_CHI2NDOF(True, strings( 'D_s+'))"
    ,"BPVVDCHI2":"BPVVDCHI2"
    ,"HelKst" :"COSPOL('[D_s+ -> K+ ^K- pi+]CC', '[D_s+ -> K+ K- ^pi+]CC', False)"
    ,"HelPhi" :"COSPOL('[D_s+ -> ^K+ K- pi+]CC', '[D_s+ -> K+ ^K- pi+]CC', False)"
    ,"HelKst_DTF_PV" :"DTF_FUN(COSPOL('[D_s+ -> K+ ^K- pi+]CC', '[D_s+ -> K+ K- ^pi+]CC', False), True)"
    ,"HelPhi_DTF_PV" :"DTF_FUN(COSPOL('[D_s+ -> ^K+ K- pi+]CC', '[D_s+ -> K+ ^K- pi+]CC', False), True)"
    ,"HelKst_DTF_Ds_PV" :"DTF_FUN(COSPOL('[D_s+ -> K+ ^K- pi+]CC', '[D_s+ -> K+ K- ^pi+]CC', False), True , strings( 'D_s+'))"
    ,"HelPhi_DTF_Ds_PV" :"DTF_FUN(COSPOL('[D_s+ -> ^K+ K- pi+]CC', '[D_s+ -> K+ ^K- pi+]CC', False), True, strings( 'D_s+'))"
    }
tuple.Ds.addTool(LoKiTuple0)
'''

## (6) build the final selection sequence
from PhysConf.Selections import SelectionSequence

## (7) configure DaVinci
from Configurables import DaVinci 
dv = DaVinci(
    DataType   = the_year       ,
    InputType  = 'MDST'         , ## ATTENTION! 
    RootInTES  = rootInTES      , ## ATTENTION! 
    ##
    #EventPreFilters = fltrs.filters('FILTER') , 
    Lumi       = False           , 
    Simulation = True          ,
    ## 
    TupleFile  = 'test.root'   , 
    #Turbo      = True      
 )

## (8) insert our sequence into DaVinci 
dv.UserAlgorithms = [ eventNodeKiller, sc.sequence(), tuple ]

## (9) number of event and input data

dv.EvtMax = 2000

## Local test ## 
DaVinci().Input = ['/afs/cern.ch/user/m/mboubdir/scratch1/tools/Analysisfiles/DST_files/00057864_00000016_3.AllStreams.mdst']


