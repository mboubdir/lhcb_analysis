# LHCb standard definitions
# -*- coding: utf-8 -*-
## from os import environ
## import math
from Gaudi.Configuration import *
from GaudiKernel.SystemOfUnits import MeV, GeV, mm
from GaudiConfUtils import ConfigurableGenerators
from Configurables import FilterDesktop, CombineParticles, TupleToolDecayTreeFitter, TupleToolDecay, OfflineVertexFitter
from PhysSelPython.Wrappers import Selection, SelectionSequence, DataOnDemand, AutomaticData
from Configurables import DecayTreeTuple, BTaggingTool, SubstitutePID, TrackScaleState, CheckPV, CondDB
from Configurables import TupleToolPid, TupleToolTrackInfo, TupleToolKinematic, TupleToolPropertime, TupleToolPrimaries, TupleToolEventInfo, TupleToolGeometry, TupleToolRecoStats, TupleToolTrackPosition, TupleToolMCBackgroundInfo , TupleToolMCTruth, MCTupleToolKinematic, MCTupleToolHierarchy , MCTupleToolEventType , MCTupleToolInteractions , TupleToolGeneration , MCTupleToolReconstructed, TupleToolTrigger, TupleToolTISTOS, TupleToolANNPID
from Configurables import DaVinci, HltSelReportsDecoder, HltVertexReportsDecoder, HltDecReportsDecoder, LoKi__Hybrid__TupleTool, TupleToolJets
from DecayTreeTuple.Configuration import *
from Configurables import LoKi__Hybrid__PlotTool as PlotTool
from Configurables import LoKi__VertexFitter as VertexFitter
from Configurables import AddRelatedInfo, RelInfoConeVariables, RelInfoTrackIsolationBDT, RelInfoVertexIsolationBDT, RelInfoVertexIsolation

from PhysSelPython.Wrappers import AutomaticData, Selection, SelectionSequence

from StrippingConf.Configuration import StrippingConf, StrippingStream
from StrippingSettings.Utils import strippingConfiguration
from StrippingArchive.Utils import buildStreams
from StrippingArchive import strippingArchive

#---------------------------------------------------------------
#Use  Stripping21r0p1 on MC for Run I
#---------------------------------------------------------------

from StrippingArchive.Stripping21r0p1.StrippingRD.StrippingB2Lambda0MuLines import B2Lambda0MuLines
from StrippingSettings.Stripping21r0p1.LineConfigDictionaries_RD import B2Lambda0Mu

#from StrippingArchive.Stripping23.StrippingRD.StrippingB2Lambda0MuLines import B2Lambda0MuLines
#from StrippingSettings.Stripping23r1.LineConfigDictionaries_RD import B2Lambda0Mu

B2Lambda0MuConf = B2Lambda0MuLines('B2Lambda0MuLines', B2Lambda0Mu['CONFIG'])
B2Lambda0MuLines = B2Lambda0MuConf.lines()

sc = StrippingConf( HDRLocation = "DecReports"  )

sstream = StrippingStream("TestStream")
sstream.appendLines( B2Lambda0MuLines )
sstream.OutputLevel = 2
sc.appendStream( sstream )

#---------------------------------------------------------------
#Use specific Stripping23r1 on MC for Run II
#---------------------------------------------------------------

## from StrippingArchive.Stripping23.StrippingRD.StrippingB2Lambda0MuLines import B2Lambda0MuLines
## from StrippingSettings.Stripping23r1.LineConfigDictionaries_RD import B2Lambda0Mu

## B2Lambda0MuConf = B2Lambda0MuLines('B2Lambda0MuLines', B2Lambda0Mu['CONFIG'])
## B2Lambda0MuLines = B2Lambda0MuConf.lines()

## ## stripline = B2Lambda0MuLines[0]
## sc = StrippingConf( HDRLocation = "DecReports"  )

## sstream = StrippingStream("TestStream")
## sstream.appendLines( B2Lambda0MuLines )
## sstream.OutputLevel = 2
## sc.appendStream( sstream )

#---------------------------
# Make Ntuples
#---------------------------
#from Configurables import PrintDecayTree, PrintDecayTreeTool

#printer = PrintDecayTree("Printer")
#printer.addTool( PrintDecayTreeTool, name = "PrintDecay" )
#printer.PrintDecay.Information = "Name M P Px Py Pz Pt chi2"
#printer.Inputs = TupleInputs

#---------------------------
# Configure lines and Decay
#---------------------------
tuple = DecayTreeTuple('DetachedN')
TupleInputs = []
for line in B2Lambda0MuLines :
    TupleInputs.append( line.outputLocation() )
tuple.Inputs = TupleInputs

tuple.OutputLevel = INFO

tuple.Decay = "[B- -> ^(Lambda0 -> ^mu- ^pi+) ^mu-]CC"
tuple.addBranches({
    "B"       : "[B- -> (Lambda0 -> mu- pi+) mu-]CC",
    "N"       : "[B- -> ^(Lambda0 -> mu- pi+) mu-]CC",
    "mu_prim" : "[B- -> (Lambda0 -> mu- pi+) ^mu-]CC",
    "mu_sec"  : "[B- -> (Lambda0 -> ^mu- pi+) mu-]CC",
    "pi"      : "[B- -> (Lambda0 -> mu- ^pi+) mu-]CC"
    })

#---------------------------
# Define nTuple Variables
#---------------------------

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

coneIso = tuple.addTupleTool("TupleToolTrackIsolation") # cone isolation
#coneIso.MinConeAngle() # Set the minimal deltaR of the cone (default = 0.5), in radians
#coneIso.MaxConeAngle() # Set the maximum deltaR of the cone (default = 1.0), in radians
#coneIso.StepSize() # Set the step of deltaR between two iterations (default = 0.1), in radians
#coneIso.TrackType() # Set the type of tracks which are considered inside the cone (default = 3)
#coneIso.FillAsymmetry() # Flag to fill the asymmetry variables (default = false)
#coneIso.FillDeltaAngles() # Flag to fill the delta angle variables (default = false) ")

# gregs isolation
from Configurables import TupleToolApplyIsolation
tuple.B.addTupleTool(TupleToolApplyIsolation, name="TupleToolApplyIsolationHard")
tuple.B.TupleToolApplyIsolationHard.OutputSuffix="_Hard"
tuple.B.TupleToolApplyIsolationHard.WeightsFile="weights_110614_Lc_pX.xml"
tuple.B.ToolList+=["TupleToolApplyIsolation/TupleToolApplyIsolationHard"]

#tuple.B.addTupleTool(TupleToolApplyIsolation, name="TupleToolApplyIsolationSoft")
#tuple.B.TupleToolApplyIsolationSoft.OutputSuffix="_Soft"
#tuple.B.TupleToolApplyIsolationSoft.WeightsFile="weightsSoft.xml"
#tuple.B.ToolList+=["TupleToolApplyIsolation/TupleToolApplyIsolationSoft"]


trigger_list = [
    'L0MuonDecision'
    ,'L0HadronDecision'
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

stripping_line = 'B2Lambda0MuBu2LambdaSSMuLine'
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

#---------------------------
# Configure DaVinci
#---------------------------

from Configurables import DaVinci
DaVinci().UserAlgorithms = [sc.sequence(), tuple]

DaVinci().InputType = 'DST'
DaVinci().DataType = '2012'
DaVinci().Simulation = True
DaVinci().Lumi = False

DaVinci().PrintFreq = 10000
DaVinci().EvtMax = -1

