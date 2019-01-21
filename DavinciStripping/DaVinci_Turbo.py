from Configurables import CombineParticles
MakeLb = CombineParticles("MakeLb")
MakeLb.Inputs = [ "/Event/Turbo/Hlt2CharmHadXicpToPpKmPipTurbo/Particles",
                 "Phys/StdAllNoPIDsPions/Particles"
]
MakeLb.DecayDescriptor =  "[ Lambda_b0 -> Lambda_c+ pi- ]cc"
MakeLb.DaughtersCuts = { "pi+"  : "(PT>250*MeV) & (MIPCHI2DV(PRIMARY)>1.0)" }
MakeLb.MotherCut = "(VFASPF(VCHI2/VDOF)<100)"

# Turbo++
from Configurables import DstConf, TurboConf # necessary for DaVinci v40r1 onwards
TurboConf().PersistReco=True
DstConf().Turbo=True

year = "2016"

from Configurables import DaVinci
DaVinci().EvtMax = 10000                         # Number of events
DaVinci().SkipEvents = 0                       # Events to skip
DaVinci().PrintFreq = 1000
DaVinci().DataType =  year
DaVinci().Simulation    = False
DaVinci().HistogramFile = "DVHistos.root"      # Histogram file
DaVinci().TupleFile = "Tuple.root"             # Ntuple
DaVinci().UserAlgorithms = [  MakeLb                            
                             ]        # The algorithms
# MDST
DaVinci().InputType = "MDST"

# Get Luminosity
DaVinci().Lumi = True

# database
from Configurables import CondDB
CondDB( LatestGlobalTagByDataType = year )

# InputData
DaVinci().Input = [
    'PFN:root://v40-8.grid.sara.nl:1094/pnfs/grid.sara.nl/data/lhcb/LHCb/Collision16/CHARMMULTIBODY.MDST/00053752/0000/00053752_00000020_1.charmmultibody.mdst'
    ]
