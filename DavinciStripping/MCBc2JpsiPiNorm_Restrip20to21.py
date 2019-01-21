# LHCb standard definitions
# -*- coding: utf-8 -*-
## from os import environ
## import math
import sys, os
from Gaudi.Configuration import *
from GaudiKernel.SystemOfUnits import MeV, GeV, mm
from GaudiConfUtils import ConfigurableGenerators
from Configurables import FilterDesktop, CombineParticles, TupleToolDecayTreeFitter, TupleToolDecay, OfflineVertexFitter
from PhysSelPython.Wrappers import Selection, SelectionSequence, DataOnDemand, AutomaticData
from Configurables import DecayTreeTuple, BTaggingTool, SubstitutePID, TrackScaleState, CheckPV, CondDB
from Configurables import TupleToolPid, TupleToolTrackInfo, TupleToolKinematic, TupleToolPropertime, TupleToolPrimaries, TupleToolEventInfo, TupleToolGeometry, TupleToolRecoStats, TupleToolTrackPosition, TupleToolMCBackgroundInfo , TupleToolMCTruth, MCTupleToolKinematic, MCTupleToolHierarchy , MCTupleToolEventType , MCTupleToolInteractions , TupleToolGeneration , MCTupleToolReconstructed, TupleToolTrigger, TupleToolTISTOS, TupleToolANNPID
from Configurables import DaVinci, HltSelReportsDecoder, HltVertexReportsDecoder, HltDecReportsDecoder, LoKi__Hybrid__TupleTool, TupleToolJets
from Configurables import PatSeeding, PatDownstream
from DecayTreeTuple.Configuration import *
from Configurables import LoKi__Hybrid__PlotTool as PlotTool
from Configurables import LoKi__VertexFitter as VertexFitter

#---------------------------------------------------------------
#Use default Stripping21 on MC
#---------------------------------------------------------------
eventNodeKiller = EventNodeKiller('Stripkiller')
eventNodeKiller.Nodes = [ '/Event/AllStreams', '/Event/Strip' ]

from StrippingConf.Configuration import StrippingConf
from StrippingConf.StrippingStream import StrippingStream

from StrippingArchive.Stripping21.StrippingB2XMuMu import B2XMuMuConf

from StrippingSettings.Stripping21.LineConfigDictionaries_RD import B2XMuMu
from PhysSelPython.Wrappers import AutomaticData, Selection, SelectionSequence


B2XMuMu['CONFIG']['HLT_FILTER'] = ""
B2XMuMuConf = B2XMuMuConf("B2XMuMu", B2XMuMu['CONFIG'])
B2XMuMuLines = B2XMuMuConf.lines()
for line in B2XMuMuLines:
    print "CL DEBUG", line
    print "CL DEBUG", line.name()
stripline = B2XMuMuLines[0]
    
sc = StrippingConf( HDRLocation = "DecReports"  )
sstream = StrippingStream("TestStream")
sstream.appendLines([  stripline  ] )
sstream.OutputLevel = 2
sc.appendStream( sstream )
            
Strip_Location1 = stripline.outputLocation()
print Strip_Location1
StripSel1 = AutomaticData(Location = Strip_Location1)
print StripSel1
print "ALL OK"


rootintes = "/Event/AllStreams"
#---------------------------
# Run fixing XmumuLine
#---------------------------
from Configurables import NeutrinoBuildTupleTool, PromptNeutrinoTupleTool

tuple = DecayTreeTuple('PromptNeutrinoTupleTool')
tuple.OutputLevel = INFO

stream = 'AllStreams'
stripping_line = 'B2XMuMu_Line'

tuple.Inputs = [StripSel1.outputLocation()]
tuple.Decay = "[B+  -> ^( J/psi(1S)  -> ^mu-  ^mu+ ) ^pi+]CC"
tuple.addBranches({
    "B"       : "[B+ -> ( J/psi(1S)  -> mu-  mu+ ) pi+ ]CC",
    "Jpsi"    : "[B+ -> ^(J/psi(1S)  -> mu-  mu+) pi+]CC",
    "mu_prim" : "[B+ -> (J/psi(1S) -> mu- ^mu+) pi+]CC",
    "mu_sec"  : "[B+ -> (J/psi(1S) -> ^mu- mu+) pi+]CC",
    "pi"      : "[B+ -> (J/psi(1S) -> mu- mu+) ^pi+]CC",
    })

tuple.ToolList = [
    "TupleToolKinematic",
    "TupleToolPid",
    "TupleToolGeometry",
    "TupleToolPrimaries",
    "TupleToolTrackInfo",
    "TupleToolEventInfo",
    "TupleToolIsolationTwoBody",
    "TupleToolRecoStats",
    "TupleToolAngles",
    "TupleToolANNPID",
    "TupleToolMCBackgroundInfo",
    "TupleToolMCTruth",
    "TupleToolTrigger",
    "TupleToolDira",
    "TupleToolEventInfo",
    "TupleToolPropertime",
    "TupleToolRecoStats",
    ]


#Calc Related Info Variables:
coneIso = tuple.addTupleTool("TupleToolTrackIsolation")

tuple.addTool(TupleToolDecay, name = 'B')
# gregs isolation

from Configurables import TupleToolApplyIsolation
tuple.B.addTupleTool(TupleToolApplyIsolation, name="TupleToolApplyIsolationHard")
tuple.B.TupleToolApplyIsolationHard.OutputSuffix="_Hard"
tuple.B.TupleToolApplyIsolationHard.WeightsFile="/afs/cern.ch/user/m/mboubdir/scratch1/tools/Analysisfiles/python_files/weights_110614_Lc_pX.xml"
tuple.B.ToolList+=["TupleToolApplyIsolation/TupleToolApplyIsolationHard"]


trigger_list = [
        'L0MuonDecision'
       ,'L0DiMuonDecision'
       ,'Hlt1TrackAllL0Decision'
       ,'Hlt1TrackMuonDecision'
       ,'Hlt2TopoMu2BodyBBDTDecision'
       ,'Hlt2TopoMu3BodyBBDTDecision'
       ,'Hlt2TopoMu4BodyBBDTDecision'
       ,'Hlt2Topo2BodyBBDTDecision'
       ,'Hlt2Topo3BodyBBDTDecision'
       ,'Hlt2Topo4BodyBBDTDecision'
       ,'Hlt2Topo2BodySimpleBBDTDecision'
       ,'Hlt2Topo3BodySimpleBBDTDecision'
       ,'Hlt2Topo4BodySimpleBBDTDecision'
    ]

#trigger config
trigger = tuple.addTupleTool(TupleToolTISTOS)
trigger.TriggerList = trigger_list
trigger.Verbose = True
trigger.VerboseL0 = True
trigger.VerboseHlt1 = True
trigger.VerboseHlt2 = True


stripping_line = 'B2XMuMu_Line'
stream = 'AllStreams'

LoKiTool = tuple.addTupleTool("LoKi::Hybrid::TupleTool/LoKiTool")
LoKiTool.Variables = {
    "InAccMuon"            : "PPINFO(LHCb.ProtoParticle.InAccMuon, -1)",
    "ETA" : "ETA",
    "LOKI_DTF_CTAU"        : "DTF_CTAU( 0, True )",
    "LOKI_DTF_CTAUS"       : "DTF_CTAUSIGNIFICANCE( 0, True )",
    "LOKI_DTF_CHI2NDOF"    : "DTF_CHI2NDOF( True )",
    "LOKI_DTF_CTAUERR"     : "DTF_CTAUERR( 0, True )",
    "LOKI_DTF_MASS" : "DTF_FUN ( M , True )" ,
    "LOKI_DTF_VCHI2NDOF"   : "DTF_FUN ( VFASPF(VCHI2/VDOF) , True )"}

#MC Information#
MCTruth = TupleToolMCTruth()
MCTruth.addTool(MCTupleToolHierarchy())
MCTruth.addTool(MCTupleToolKinematic())
MCTruth.addTool(MCTupleToolReconstructed())
MCTruth.ToolList += ["MCTupleToolHierarchy", "MCTupleToolKinematic", "MCTupleToolReconstructed" ]

#tuple.addTool(TupleToolDecay(), name="B")
#tuple.B.ToolList += ["NeutrinoBuildTupleTool"]

#relAlgos = [ sc.sequence() ]
#relAlgos.append(tuple)

#---------------------------
# Configure DaVinci
#---------------------------

from Configurables import DaVinci
DaVinci().UserAlgorithms += [ eventNodeKiller ]
DaVinci().UserAlgorithms += [ sc.sequence(), tuple ]

DaVinci().InputType = 'DST'
DaVinci().DataType = '2012'
DaVinci().Simulation = True
DaVinci().Lumi = False

DaVinci().PrintFreq = 1000
DaVinci().EvtMax = -1

LHCbApp().DDDBtag = 'Sim08-20130503-1'
DaVinci().CondDBtag = 'Sim08-20130503-1-vc-md100'
#DaVinci().CondDBtag = 'Sim08-20130503-1-vc-mu100'

DaVinci().TupleFile = '12MCDown_Bc2Norm_B2XMuMu_strip21.root'


#from GaudiConf import IOHelper
#IOHelper('ROOT').inputFiles([ '/afs/cern.ch/user/m/mboubdir/scratch1/tools/Analysisfiles/DST_files/00029350_00000019_1.allstreams.dst'], clear=True)
