# LHCb= standard definitions
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

#---------------------------------------------------------------
#Use default Stripping21 on MC
#---------------------------------------------------------------

#from StrippingArchive.Stripping21.StrippingB2XuMuNu import B2XuMuNuBuilder
#from StrippingSettings.Stripping21.LineConfigDictionaries_Semileptonic import B2XuMuNu

#B2XuMuNuConf = B2XuMuNuBuilder('B2XuMuNuBuilder', B2XuMuNu['CONFIG'])
#B2XuMuNuLines = B2XuMuNuConf.lines()

#sc = StrippingConf( HDRLocation = "DecReports"  )

#sstream = StrippingStream("TestStream")
#sstream.appendLines( B2XuMuNuLines )
#sstream.OutputLevel = 2
#sc.appendStream( sstream )

#---------------------------
# Run fixing XmumuLine
#---------------------------
from StrippingConf.Configuration import StrippingConf, StrippingStream
from StrippingSettings.Utils import strippingConfiguration
from StrippingArchive.Utils import buildStreams
from StrippingArchive import strippingArchive
from Configurables import ProcStatusCheck

strip = 'stripping26'
streams = buildStreams(stripping=strippingConfiguration(strip), archive=strippingArchive(strip))

filterBadEvents=ProcStatusCheck()
custom_stream = StrippingStream('CustomStream')
custom_line =  'StrippingB2XMuMu_Line'

for stream in streams:
    for line in stream.lines:
        if line.name() == custom_line:
            custom_stream.appendLines([line])
            
#line = 'B2XMuMu_Line'

sc = StrippingConf(Streams=[custom_stream],MaxCandidates=1000,
                   AcceptBadEvents=False,
                   BadEventSelection=filterBadEvents)
                        
# The output is placed directly into Phys, so we only need to
# define the stripping line here
#line = 'B2Lambda0MuBu2LambdaSSMuLine'
line = 'B2XMuMu_Line'
tuple = DecayTreeTuple('PromptNeutrinoTupleTool')
#tuple = DecayTreeTuple('DetachedN')
tuple.OutputLevel = INFO

tuple.Inputs =  ['/Event/Phys/{0}/Particles'.format(line)]
tuple.Decay = "[B+  -> ^( J/psi(1S)  -> ^mu-  ^mu+ ) ^pi+]CC"
tuple.Branches = {
    "B"       : "[B+ -> ( J/psi(1S)  -> mu-  mu+ ) pi+ ]CC",
    "Jpsi"    : "[B+ -> ^(J/psi(1S)  -> mu-  mu+) pi+]CC",
    "mu_prim" : "[B+ -> (J/psi(1S) -> mu- ^mu+) pi+]CC",
    "mu_sec"  : "[B+ -> (J/psi(1S) -> ^mu- mu+) pi+]CC",
    "pi"      : "[B+ -> (J/psi(1S) -> mu- mu+) ^pi+]CC",
   }

#tuple.Decay = "[B- -> ^(Lambda0 -> ^mu- ^pi+) ^mu-]CC"
#tuple.addBranches({
#    "B"       : "[B- -> (Lambda0 -> mu- pi+) mu-]CC",
#    "N"       : "[B- -> ^(Lambda0 -> mu- pi+) mu-]CC",
#    "mu_prim" : "[B- -> (Lambda0 -> mu- pi+) ^mu-]CC",
#    "mu_sec"  : "[B- -> (Lambda0 -> ^mu- pi+) mu-]CC",
#    "pi"      : "[B- -> (Lambda0 -> mu- ^pi+) mu-]CC"
#        })

tuple.ToolList = [
        "TupleToolKinematic",
        "TupleToolPid",
        "TupleToolGeometry",
        "TupleToolPrimaries",
        "TupleToolTrackInfo",
        "TupleToolEventInfo",
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

trigger_list = [
    'L0MuonDecision'
    ,'L0DiMuonDecision'
    ,'L0HadronDecision'
    ,'Hlt1TrackAllL0Decision'
    ,'Hlt1TrackMuonDecision'
    ,'Hlt1TrackMVADecision'
    ,'Hlt1TwoTrackMVADecision'
    ,'Hlt1TrackMVALooseDecision'
    ,'Hlt1TwoTrackMVALooseDecision'
    ,'Hlt2TopoMu2BodyBBDTDecision'
    ,'Hlt2TopoMu3BodyBBDTDecision'
    ,'Hlt2Topo2BodyDecision'
    ,'Hlt2Topo3BodyDecision'
    ,'Hlt2TopoMu2BodyDecision'
    ,'Hlt2TopoMu3BodyDecision'
    ,'Hlt2TopoMuMu2BodyDecision'
    ,'Hlt2TopoMuMu3BodyDecision'
    ,'Hlt2Topo2BodyBBDTDecision'
    ,'Hlt2Topo3BodyBBDTDecision'
    ,'Hlt2Topo4BodyBBDTDecision'
    ,'Hlt2Topo2BodySimpleBBDTDecision'
    ,'Hlt2Topo3BodySimpleBBDTDecision'
    ]

#coneIso = tuple.addTupleTool("TupleToolTrackIsolation") # cone isolation
#coneIso.MinConeAngle() # Set the minimal deltaR of the cone (default = 0.5), in radians
#coneIso.MaxConeAngle() # Set the maximum deltaR of the cone (default = 1.0), in radians
#coneIso.StepSize() # Set the step of deltaR between two iterations (default = 0.1), in radians
#coneIso.TrackType() # Set the type of tracks which are considered inside the cone (default = 3)
#coneIso.FillAsymmetry() # Flag to fill the asymmetry variables (default = false)
#coneIso.FillDeltaAngles() # Flag to fill the delta angle variables (default = false) ")

# gregs isolation
#from Configurables import TupleToolApplyIsolation
#tuple.B.addTupleTool(TupleToolApplyIsolation, name="TupleToolApplyIsolationHard")
#tuple.B.TupleToolApplyIsolationHard.OutputSuffix="_Hard"
#tuple.B.TupleToolApplyIsolationHard.WeightsFile="weights_110614_Lc_pX.xml"
#tuple.B.ToolList+=["TupleToolApplyIsolation/TupleToolApplyIsolationHard"]


#trigger config
trigger = tuple.addTupleTool(TupleToolTISTOS)
trigger.TriggerList = trigger_list
trigger.Verbose = True
trigger.VerboseL0 = True
trigger.VerboseHlt1 = True
trigger.VerboseHlt2 = True



relinfolocation = '/Event/Phys/{0}'.format(line)

LoKiTool = tuple.addTupleTool("LoKi::Hybrid::TupleTool/LoKiTool")
LoKiTool.Variables = {
    "InAccMuon"            : "PPINFO(LHCb.ProtoParticle.InAccMuon, -1)",
    "ETA"                  : "ETA",
    "DIRA"                 : "BPVDIRA",
    "FDCHI2"               : "BPVVDCHI2",
    "IPChi2"               : "MIPCHI2DV(PRIMARY)",
    "LOKI_DTF_CTAU"        : "DTF_CTAU( 0, True  )",
    "LOKI_DTF_CTAUS"       : "DTF_CTAUSIGNIFICANCE( 0, True )",
    "LOKI_DTF_CHI2NDOF"    : "DTF_CHI2NDOF(  True )",
    "LOKI_DTF_CTAUERR"     : "DTF_CTAUERR( 0, True )",
    "LOKI_DTF_MASS"        : "DTF_FUN ( M , True )" ,
    "LOKI_DTF_VCHI2NDOF"   : "DTF_FUN ( VFASPF(VCHI2/VDOF) , True )"   ,
    #
    "CONEANGLE" : "RELINFO('"+relinfolocation+"/ConeIsoInfo', 'CONEANGLE', -1.)",
    "CONEMULT" : "RELINFO('"+relinfolocation+"/ConeIsoInfo', 'CONEMULT', -1.)",
    "CONEPTASYM" : "RELINFO('"+relinfolocation+"/ConeIsoInfo', 'CONEPTASYM', -1.)",
    "CONEPT" : "RELINFO('"+relinfolocation+"/ConeIsoInfo', 'CONEPT', -1.)",
    "CONEP" : "RELINFO('"+relinfolocation+"/ConeIsoInfo', 'CONEP', -1.)",
    "CONEPASYM" : "RELINFO('"+relinfolocation+"/ConeIsoInfo', 'CONEPASYM', -1.)",
    "CONEDELTAETA" : "RELINFO('"+relinfolocation+"/ConeIsoInfo', 'CONEDELTAETA', -1.)",
    "CONEDELTAPHI" : "RELINFO('"+relinfolocation+"/ConeIsoInfo', 'CONEDELTAPHI', -1.)",
    #
    "VTXISONUMVTX" : "RELINFO('"+relinfolocation+"/VtxIsoInfo', 'VTXISONUMVTX', -1.)",
    "VTXISODCHI2ONETRACK" : "RELINFO('"+relinfolocation+"/VtxIsoInfo', 'VTXISODCHI2ONETRACK', -1.)",
    "VTXISODCHI2MASSONETRACK" : "RELINFO('"+relinfolocation+"/VtxIsoInfo', 'VTXISODCHI2MASSONETRACK', -1.)",
    "VTXISODCHI2TWOTRACK" : "RELINFO('"+relinfolocation+"/VtxIsoInfo', 'VTXISODCHI2TWOTRACK', -1.)",
    "VTXISODCHI2MASSTWOTRACK" : "RELINFO('"+relinfolocation+"/VtxIsoInfo', 'VTXISODCHI2MASSTWOTRACK', -1.)",
    #
    "VTXISOBDTHARDFIRSTVALUE" : "RELINFO('"+relinfolocation+"/VtxIsoBDTInfo', 'VTXISOBDTHARDFIRSTVALUE', -1.)",
    "VTXISOBDTHARDSECONDVALUE" : "RELINFO('"+relinfolocation+"/VtxIsoBDTInfo', 'VTXISOBDTHARDSECONDVALUE', -1.)",
    "VTXISOBDTHARDTHIRDVALUE" : "RELINFO('"+relinfolocation+"/VtxIsoBDTInfo', 'VTXISOBDTHARDTHIRDVALUE', -1.)",
    "VTXISOBDTSOFTFIRSTVALUE" : "RELINFO('"+relinfolocation+"/VtxIsoBDTInfo', 'VTXISOBDTSOFTFIRSTVALUE', -1.)",
    "VTXISOBDTSOFTSECONDVALUE" : "RELINFO('"+relinfolocation+"/VtxIsoBDTInfo', 'VTXISOBDTSOFTSECONDVALUE', -1.)",
    "VTXISOBDTSOFTTHIRDVALUE" : "RELINFO('"+relinfolocation+"/VtxIsoBDTInfo', 'VTXISOBDTSOFTTHIRDVALUE', -1.)"
    }

'''
LoKiTool = tuple.addTupleTool("LoKi::Hybrid::TupleTool/LoKiTool")
LoKiTool.Variables = {
    "inMuon" : "switch(INMUON, 1, 0)",
    "ETA" : "ETA",
    "LOKI_DTF_CTAU"        : "DTF_CTAU( 0, True )",
    "LOKI_DTF_CTAUS"       : "DTF_CTAUSIGNIFICANCE( 0, True )",
    "LOKI_DTF_CHI2NDOF"    : "DTF_CHI2NDOF( True )",
    "LOKI_DTF_CTAUERR"     : "DTF_CTAUERR( 0, True )",
    "LOKI_DTF_MASS" : "DTF_FUN ( M , True )" ,
    "LOKI_DTF_VCHI2NDOF"   : "DTF_FUN ( VFASPF(VCHI2/VDOF) , True )"}
'''

#MC Information
MCTruth = TupleToolMCTruth()
MCTruth.addTool(MCTupleToolHierarchy())
MCTruth.addTool(MCTupleToolKinematic())
MCTruth.addTool(MCTupleToolReconstructed())
MCTruth.ToolList += ["MCTupleToolHierarchy", "MCTupleToolKinematic", "MCTupleToolReconstructed" ]

from Configurables import PromptNeutrinoTupleTool
tuple.addTool(TupleToolDecay(), name="B")
tuple.B.ToolList += ["PromptNeutrinoTupleTool"]

#---------------------------
# Configure DaVinci
#---------------------------

from Configurables import DaVinci
#DaVinci().appendToMainSequence([sc.sequence()])
DaVinci().UserAlgorithms += [tuple]

#DaVinci().InputType = 'LDST'
DaVinci().InputType = 'MDST'
DaVinci().DataType = '2016'
DaVinci().Simulation = True
DaVinci().Lumi = False

DaVinci().PrintFreq = 1000
DaVinci().EvtMax = -1


#Local test
DaVinci().TupleFile = '16MCDown_NormChan_B2XMuMu_strip28.root'
DaVinci().Input = ['/afs/cern.ch/user/m/mboubdir/scratch1/tools/Analysisfiles/DST_files/00057860_00000019_3.AllStreams.mdst']
