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
from Configurables import PromptNeutrinoTupleTool, NeutrinoBuildTupleTool

stripping_line = 'B2XMuMu_Line'
stream = 'Leptonic'

tuple = DecayTreeTuple('PromptNeutrinoTupleTool')
tuple.OutputLevel = INFO

#tuple.Inputs = [ B2XuMuNuLines[0].outputLocation() ]
tuple.Inputs =  ['/Event/{0}/Phys/{1}/Particles'.format(stream, stripping_line)]
tuple.Decay = "[B+  -> ^( J/psi(1S)  -> ^mu-  ^mu- ) ^pi+]CC"
tuple.Branches = {
    "B"       : "[B+ -> ( J/psi(1S)  -> mu-  mu- ) pi+ ]CC",
    "Jpsi"    : "[B+ -> ^(J/psi(1S)  -> mu-  mu-) pi+]CC",
    "mu_prim" : "[B+ -> (J/psi(1S) -> mu- ^mu-) pi+]CC",
    "mu_sec"  : "[B+ -> (J/psi(1S) -> ^mu- mu-) pi+]CC",
    "pi"      : "[B+ -> (J/psi(1S) -> mu- mu-) ^pi+]CC",
    }

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

#trigger config
trigger = tuple.addTupleTool(TupleToolTISTOS)
trigger.TriggerList = trigger_list
trigger.Verbose = True
trigger.VerboseL0 = True
trigger.VerboseHlt1 = True
trigger.VerboseHlt2 = True

relinfolocation = '/Event/{0}/Phys/B2XMuMu_Line'.format(stream)

LoKiTool = tuple.addTupleTool("LoKi::Hybrid::TupleTool/LoKiTool")
LoKiTool.Variables = {
#    "isMuon"               : "switch(ISMUON, 1, 0)",
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

#MC Information
MCTruth = TupleToolMCTruth()
MCTruth.addTool(MCTupleToolHierarchy())
MCTruth.addTool(MCTupleToolKinematic())
MCTruth.addTool(MCTupleToolReconstructed())
MCTruth.ToolList += ["MCTupleToolHierarchy", "MCTupleToolKinematic", "MCTupleToolReconstructed" ]

tuple.addTool(TupleToolDecay(), name="B")
tuple.B.ToolList += ["PromptNeutrinoTupleTool"]

#---------------------------
# Configure DaVinci
#---------------------------

from Configurables import DaVinci
DaVinci().UserAlgorithms = [tuple]

DaVinci().RootInTES ='/Event/{0}'.format(stream)
DaVinci().InputType = 'MDST'
DaVinci().DataType = '2015'
DaVinci().Simulation = False
DaVinci().Lumi = True

DaVinci().PrintFreq = 10000
DaVinci().EvtMax = -1

DaVinci().TupleFile= '15DATADown_PromptN_B2XMuMu_strip24.root'

#DATA 2012 stripping 21 leptonic mdst
#DaVinci().Input = ['/afs/cern.ch/user/m/mboubdir/scratch1/tools/Analysisfiles/DST_files/00060047_00004462_1.leptonic.mdst']

