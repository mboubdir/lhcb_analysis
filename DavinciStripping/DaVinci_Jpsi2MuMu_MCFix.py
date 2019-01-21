from DecayTreeTuple.Configuration import *

Jpsi2MuMuTuple = DecayTreeTuple("Jpsi2MuMuTuple")
Jpsi2MuMuTuple.Inputs = ["/Event/AllStreams/Phys/FullDSTDiMuonJpsi2MuMuDetachedLine/Particles"]
Jpsi2MuMuTuple.Decay = "J/psi(1S) -> ^mu+ ^mu-"

from Configurables import TupleToolMCTruth
Jpsi2MuMuTuple.ToolList += [
        "TupleToolMCBackgroundInfo",
        "TupleToolMCTruth"
        ]

MCTruth = TupleToolMCTruth()
MCTruth.ToolList =  [
        "MCTupleToolAngles"
        , "MCTupleToolHierarchy"
        , "MCTupleToolKinematic"
        ]

# Work around for Turbo locations being included in the default list of
# relations table locations, which triggers Turbo unpacking and seg. faults
from Configurables import MCMatchObjP2MCRelator
default_rel_locs = MCMatchObjP2MCRelator().getDefaultProperty('RelTableLocations')
rel_locs = [loc for loc in default_rel_locs if 'Turbo' not in loc] 

MCTruth.addTool(MCMatchObjP2MCRelator)
MCTruth.MCMatchObjP2MCRelator.RelTableLocations = rel_locs 

Jpsi2MuMuTuple.addTool(MCTruth)        

from Configurables import DaVinci
DaVinci().EvtMax = -1                        # Number of events
DaVinci().HistogramFile = "DVHistos.root"
DaVinci().DataType  = "2016"
DaVinci().InputType = "DST"
DaVinci().Simulation = True
DaVinci().TupleFile = "Tuple.root"            # Ntuple
DaVinci().UserAlgorithms = [ Jpsi2MuMuTuple
                             ]  # The algorithms

# Get Luminosity
DaVinci().Lumi = False

from Configurables import MessageSvc
MessageSvc().setWarning = [ 'RFileCnv' ]

DaVinci().DDDBtag   = "dddb-20170721-3"
DaVinci().CondDBtag = "sim-20170721-2-vc-md100"

