// Include files 

// from Gaudi
#include "GaudiKernel/ToolFactory.h" 

// local
#include "PromptNeutrinoTupleTool.h"

//-----------------------------------------------------------------------------
// Implementation file for class : PromptNeutrinoTupleTool
//
// 2017-04-13 : Christian Voss && Meriem Boubdir
//-----------------------------------------------------------------------------

// Declaration of the Tool Factory
DECLARE_TOOL_FACTORY( PromptNeutrinoTupleTool )


//=============================================================================
// Standard constructor, initializes variables
//=============================================================================
PromptNeutrinoTupleTool::PromptNeutrinoTupleTool( const std::string& type,
                                                  const std::string& name,
                                                  const IInterface* parent )
  : TupleToolBase ( type, name , parent )
{
  declareInterface<IParticleTupleTool>(this);
  declareProperty("DoNormalisation"   , m_Normaliation = true );
  declareProperty("PVLocation"        , m_DataPVLocation = "/Event/Rec/Vertex/Primary" );
  declareProperty("VertexFitter"      , m_VertexFitterName = "OfflineVertexFitter" );
  declareProperty("Particle2PVRelator", m_Particle2PVRelatorName = "GenericParticle2PVRelator" );
}
//=============================================================================
// Destructor
//=============================================================================
PromptNeutrinoTupleTool::~PromptNeutrinoTupleTool() {} 

//=============================================================================
StatusCode PromptNeutrinoTupleTool::initialize()
{
  if( ! TupleToolBase::initialize() ) return StatusCode::FAILURE;
  m_dva = Gaudi::Utils::getIDVAlgorithm ( contextSvc(), this ) ;
  if (0==m_dva) return Error("Couldn't get parent DVAlgorithm", StatusCode::FAILURE);
  
  m_Fit      = m_dva->vertexFitter();
  // m_Fit      = tool<IVertexFit>(m_VertexFitterName, this);
  m_DistCalc = m_dva->distanceCalculator();
  m_lifetime = m_dva->lifetimeFitter();
  
  m_ppSvc    = svc<LHCb::IParticlePropertySvc>("LHCb::ParticlePropertySvc",true);
  
  const LHCb::ParticleProperty* JpsiInfo   = m_ppSvc->find( "J/psi(1S)" ) ;
  const LHCb::ParticleProperty* pipInfo    = m_ppSvc->find( "pi+" );
  const LHCb::ParticleProperty* pimInfo    = m_ppSvc->find( "pi-" );
  const LHCb::ParticleProperty* BpInfo     = m_ppSvc->find( "B+" );  
  const LHCb::ParticleProperty* BmInfo     = m_ppSvc->find( "B-" );
  const LHCb::ParticleProperty* mupInfo    = m_ppSvc->find( "mu+" ) ;
  const LHCb::ParticleProperty* munInfo    = m_ppSvc->find( "mu-" ) ;
  const LHCb::ParticleProperty* LambdaInfo = m_ppSvc->find( "Lambda0" ) ;
  const LHCb::ParticleProperty* DeltaInfo  = m_ppSvc->find( "Delta++" ) ;
  
  m_JpsiID      = JpsiInfo->particleID();
  m_muPlusID    = mupInfo->particleID();
  m_muMinusID   = munInfo->particleID();
  m_pimID       = pimInfo->particleID();
  m_pipID       = pipInfo->particleID();
  m_BpID        = BpInfo->particleID();
  m_BmID        = BmInfo->particleID();
  m_LambdaID    = LambdaInfo->particleID();
  m_LambdabarID = LambdaInfo->antiParticle()->particleID();

  m_DeltaID     = DeltaInfo->particleID();
  m_antiDeltaID = DeltaInfo->antiParticle()->particleID();
  
  return StatusCode::SUCCESS;
}
//=============================================================================
// Overwrite pure virtual void fill method for IParticleTupleTool
//=============================================================================
StatusCode PromptNeutrinoTupleTool::fill (const LHCb::Particle *top,
                                         const LHCb::Particle *part,
                                         const std::string &head,
                                         Tuples::Tuple &tuple)
{
  m_BPV = (const LHCb::Vertex*)m_dva->bestVertex(part);
  if ( 0 == m_BPV)
    warning() << "No PV accessable" << endmsg;

  m_Pion = NULL; m_MuOne = NULL; m_MuTwo = NULL;
  
  debug() << "==> Begin Process" << endmsg;

  StatusCode GlobalFilter(StatusCode::FAILURE);

  StatusCode FoundChargedParticles =  PromptNeutrinoTupleTool::m_getCharedParticles(part);
  if ( msgLevel(MSG::DEBUG) && !m_Pion )  debug() << "Nullpointer Pion" << endmsg;
  if ( msgLevel(MSG::DEBUG) && !m_MuOne ) debug() << "Nullpointer Mu_One" << endmsg;
  if ( msgLevel(MSG::DEBUG) && !m_MuTwo ) debug() << "Nullpointer Mu_Two" << endmsg;

  if ( FoundChargedParticles == StatusCode::FAILURE ){
    warning() << "==> Charge Check failed" << endmsg;
    PromptNeutrinoTupleTool::m_fillBlankVariables( tuple, "N_1" );
    PromptNeutrinoTupleTool::m_fillBlankVariables( tuple, "N_2" );
    GlobalFilter = PromptNeutrinoTupleTool::m_cleanUp();
  }
  StatusCode GoodNeutrinoFit(StatusCode::FAILURE), GoodBFit(StatusCode::FAILURE);

  //Reconstruction for the first Neutrino containing MuOne
  GoodNeutrinoFit = PromptNeutrinoTupleTool::m_recoNeutrino( m_MuOne, Neutrino_1, VtxNeutrino_1 );

  if ( GoodNeutrinoFit == StatusCode::FAILURE ){
    debug() << "==> Neutrino reco I failed" << endmsg;
    PromptNeutrinoTupleTool::m_fillBlankVariables( tuple, "N_1" );
    // GlobalFilter = PromptNeutrinoTupleTool::m_cleanUp();
  }
  //Reconstruction for the first B Meson using MuTwo
  if ( GoodNeutrinoFit == StatusCode::SUCCESS )
    GoodBFit = PromptNeutrinoTupleTool::m_recoBMeson( m_MuTwo,
                                                      Neutrino_1,
                                                      BMeson_1,
                                                      VtxBMeson_1);
  if ( GoodBFit == StatusCode::FAILURE ){
    debug() << "==> B Reco failed" << endmsg;
    PromptNeutrinoTupleTool::m_fillBlankVariables( tuple, "N_1" );
    // GlobalFilter = PromptNeutrinoTupleTool::m_cleanUp(); 
  }
  //Write Events for MuOne
  if ( FoundChargedParticles == StatusCode::SUCCESS )
    if ( GoodNeutrinoFit == StatusCode::SUCCESS )
      if ( GoodBFit == StatusCode::SUCCESS ){
        debug() << "==> Write Tuples" << endmsg;
        PromptNeutrinoTupleTool::m_fillVariables( tuple, "N_1", Neutrino_1, BMeson_1);
      }
  debug() << "==> Second B decay" << endmsg;
  //Reconstruction for the second Neutrino containing MuTwo
  GoodNeutrinoFit = StatusCode::FAILURE;
  GoodBFit        = StatusCode::FAILURE;
  GoodNeutrinoFit = PromptNeutrinoTupleTool::m_recoNeutrino( m_MuTwo, Neutrino_2, VtxNeutrino_2 );
  
  if ( GoodNeutrinoFit == StatusCode::FAILURE ){
    debug() << "==> Neutrino reco II failed" << endmsg;
    PromptNeutrinoTupleTool::m_fillBlankVariables( tuple, "N_2" );
  }
  
  debug() << "==> Second Candidate" << endmsg;
  //Reconstruction for the second B Meson using MuOne
  if ( GoodNeutrinoFit == StatusCode::SUCCESS )
    GoodBFit = PromptNeutrinoTupleTool::m_recoBMeson( m_MuOne,
                                                      Neutrino_2,
                                                      BMeson_2,
                                                      VtxBMeson_2);
  if ( GoodBFit == StatusCode::FAILURE ){
    debug() << "==> B Reco failed" << endmsg;
    PromptNeutrinoTupleTool::m_fillBlankVariables( tuple, "N_2" );
  }
  //Write Events for MuTwo
  if ( FoundChargedParticles == StatusCode::SUCCESS )
    if ( GoodNeutrinoFit == StatusCode::SUCCESS )
      if ( GoodBFit == StatusCode::SUCCESS ){
        debug() << "==> Write Tuples" << endmsg;
        PromptNeutrinoTupleTool::m_fillVariables( tuple, "N_2", Neutrino_2, BMeson_2);
      }

  debug() << "Switching to next B Candidate" << endmsg;
  
  return PromptNeutrinoTupleTool::m_cleanUp(); 
}
//=============================================================================
// Fill variables for valid Neutrino candidates
//=============================================================================
StatusCode PromptNeutrinoTupleTool::m_fillVariables( Tuples::Tuple &tuple,
                                                     std::string name,
                                                     LHCb::Particle& Neutrino,
                                                     LHCb::Particle& BMeson)
{
  if ( !BMeson.endVertex() || !Neutrino.endVertex() )
    warning() << "Bugger no vertices" << endmsg;

  debug() << "Filling regular tuple" << endmsg;
  
  tuple->column( name + "_ORIVX_CHI2", BMeson.endVertex()->chi2() );
  tuple->column( name + "_ORIVX_NDOF", BMeson.endVertex()->nDoF() );
  tuple->column( name + "_ORIVX_X",    BMeson.endVertex()->position().x() );
  tuple->column( name + "_ORIVX_Y",    BMeson.endVertex()->position().y() );
  tuple->column( name + "_ORIVX_Z",    BMeson.endVertex()->position().z() );

  tuple->column( name + "_ENDVERTEX_CHI2", Neutrino.endVertex()->chi2() );
  tuple->column( name + "_ENDVERTEX_NDOF", Neutrino.endVertex()->nDoF() );
  tuple->column( name + "_ENDVERTEX_X",    Neutrino.endVertex()->position().x() );
  tuple->column( name + "_ENDVERTEX_Y",    Neutrino.endVertex()->position().y() );
  tuple->column( name + "_ENDVERTEX_Z",    Neutrino.endVertex()->position().z() );

  tuple->column( name + "_M",  Neutrino.momentum().M() );
  tuple->column( name + "_MM", Neutrino.measuredMass() );
  tuple->column( name + "_PX", Neutrino.momentum().px() );
  tuple->column( name + "_PY", Neutrino.momentum().py() );
  tuple->column( name + "_PZ", Neutrino.momentum().pz() );
  tuple->column( name + "_PE", Neutrino.momentum().E() );

  info() << "Tuple Fill Mass = " << Neutrino.momentum().M() << endmsg;
  
  /*
  TVector3 FlN, Np;  
  FlN.SetX( - (BMeson).endVertex()->position().x() + (Neutrino).endVertex()->position().x() );
  FlN.SetY( - (BMeson).endVertex()->position().y() + (Neutrino).endVertex()->position().y() );
  FlN.SetZ( - (BMeson).endVertex()->position().z() + (Neutrino).endVertex()->position().z() );
  Np.SetX( (Neutrino).momentum().px() );
  Np.SetY( (Neutrino).momentum().py() );
  Np.SetZ( (Neutrino).momentum().pz() );
  
  double theta_DIRA =  Np.Angle(FlN);
  
  if ( isnan( theta_DIRA ) ){
    warning() << "NAN for Neutrino DIRA angle" << endmsg;
    tuple->column( name + "_DIRA_ORIVX", -1e30 );
  }
  else
    tuple->column( name + "_DIRA_ORIVX", cos(theta_DIRA ) );
  */
  double dist(-1e30), chi2(-1e30);
  m_DistCalc->distance ( &Neutrino, m_BPV, dist, chi2);
  tuple->column( name + "_IP_OWNPV", dist ) ;
  tuple->column( name + "_IPCHI2_OWNPV", chi2  );
  debug() << "==> lifetime" << endmsg;
  double pt(-1e30), ept(-1e30), ptchi2(-1e30);
  if ( 0 ==  BMeson.endVertex() )
    warning() << "==> lifetime missing B Vertex" << endmsg;
  StatusCode sc = m_lifetime->fit ( *(BMeson.endVertex()), (Neutrino) , pt, ept, ptchi2 );
  if( !sc ){
    Warning("The propertime fit failed").ignore();
    pt   = -1e30;
    ept  = -1e30;
    ptchi2 = -1e30;
  }
  
  tuple->column( name + "_TAU" , pt ); // nanoseconds
  tuple->column( name + "_TAUERR" , ept );
  tuple->column( name + "_TAUCHI2" , chi2 );

  dist = -1e30;
  chi2 = -1e30;

  debug() << "==> IP stuff" << endmsg;
  sc = m_DistCalc->distance( BMeson.endVertex(), Neutrino.endVertex(), dist, chi2 );
  if ( sc.isFailure() ){
    dist = -1e30;
    chi2 = -1e30;
  }
  tuple->column( name + "_FD_ORIVX", dist );
  tuple->column( name + "_FDCHI2_ORIVX", chi2 );

  debug() << "==> Finished Cand Block" << endmsg;

  return StatusCode::SUCCESS;
}
//=============================================================================
// Fill blank variables for failed Vertex fits
//=============================================================================
StatusCode PromptNeutrinoTupleTool::m_fillBlankVariables( Tuples::Tuple &tuple,
							  std::string name )
{
  debug() << "Filling blank tuple" << endmsg;

  tuple->column( name + "_ORIVX_CHI2", -1e30 );
  tuple->column( name + "_ORIVX_NDoF", -1e30 );
  tuple->column( name + "_ORIVX_X",    -1e30 );
  tuple->column( name + "_ORIVX_Y",    -1e30 );
  tuple->column( name + "_ORIVX_Z",    -1e30 );

  tuple->column( name + "_ENDVERTEX_CHI2", -1e30 );
  tuple->column( name + "_ENDVERTEX_NDoF", -1e30 );
  tuple->column( name + "_ENDVERTEX_X", -1e30 );
  tuple->column( name + "_ENDVERTEX_Y", -1e30 );
  tuple->column( name + "_ENDVERTEX_Z", -1e30 );
  
  tuple->column( name + "_M", -1e30  );
  tuple->column( name + "_MM", -1e30  );
  tuple->column( name + "_PX", -1e30 );
  tuple->column( name + "_PY", -1e30 );
  tuple->column( name + "_PZ", -1e30 );
  tuple->column( name + "_PE", -1e30 );
  
  //tuple->column( name + "_DIRA_ORIVX", -1e30 );
  
  tuple->column( name + "_IP_OWNPV", -1e30 ) ;
  tuple->column( name + "_IPCHI2_OWNPV", -1e30 );

  tuple->column( name + "_TAU" , -1e30 ); // nanoseconds
  tuple->column( name + "_TAUERR" , -1e30 );
  tuple->column( name + "_TAUCHI2" , -1e30 );
  
  tuple->column( name + "_FD_ORIVX", -1e30 );
  tuple->column( name + "_FDCHI2_ORIVX", -1e30 );
  
  return StatusCode::SUCCESS;
}
//=============================================================================
// Ceck for charged candidates
//=============================================================================
StatusCode PromptNeutrinoTupleTool::m_getCharedParticles(const LHCb::Particle *part)
{
  LHCb::Particle::ConstVector::const_iterator IterDau,IterJpsi;
  
  if ( ((part)->particleID() == m_BpID) || ((part)->particleID() == m_BmID) ){
    LHCb::Particle::ConstVector BDaughters = (part)->daughtersVector();
    if ( msgLevel(MSG::DEBUG) ) debug() << "Found charged B Meson" << endmsg;
    for (IterDau = BDaughters.begin(); IterDau != BDaughters.end(); IterDau++){
      if ( ( (*IterDau)->particleID() == m_pimID )
           || ( (*IterDau)->particleID() == m_pipID ) )
        m_Pion = (*IterDau);
      
      if ( (*IterDau)->particleID() ==  m_JpsiID ){
        LHCb::Particle::ConstVector JpsiDaughters = (*IterDau)->daughtersVector();
        m_MuOne = JpsiDaughters.at(0);
        m_MuTwo = JpsiDaughters.at(1);
        }
      }
    }

  if ( msgLevel(MSG::DEBUG) && m_Pion )  debug() << "Found charged Pion" << endmsg;
  if ( msgLevel(MSG::DEBUG) && m_MuOne ) debug() << "Found first Muon" << endmsg;
  if ( msgLevel(MSG::DEBUG) && m_MuTwo ) debug() << "Found second Muon" << endmsg;
  
  if ( m_Pion && m_MuOne && m_MuTwo )
    return StatusCode::SUCCESS;
  else
    return StatusCode::FAILURE;
}
//=============================================================================
// Neutrino reconstruction
//=============================================================================
StatusCode PromptNeutrinoTupleTool::m_recoNeutrino( const LHCb::Particle *Mu_Sec,
                                                    LHCb::Particle& Neutrino,
                                                    LHCb::Vertex& VtxNeutrino )
{
  StatusCode NFit; 
  // Search for N -> mu- pi +
  if ( m_Pion->particleID() == m_pipID ){
    Neutrino = LHCb::Particle(m_LambdaID);
    NFit = m_Fit->fit(*m_Pion, *Mu_Sec, VtxNeutrino, Neutrino);
  }
  // Search for N -> mu+ pi -
  if ( m_Pion->particleID() == m_pimID ){
    Neutrino = LHCb::Particle(m_LambdabarID);
    NFit = m_Fit->fit(*m_Pion, *Mu_Sec, VtxNeutrino, Neutrino);
  }
  if ( 0 == Neutrino.endVertex() ){
    warning() << "No N endvertex" << endmsg;
    return StatusCode::FAILURE;
  }
  info() << "Build Mass = " << Neutrino.momentum().M() << endmsg;
  
  return NFit;
}
//=============================================================================
// B candidate reconstruction
//=============================================================================
StatusCode PromptNeutrinoTupleTool::m_recoBMeson( const LHCb::Particle *Mu_Prim,
                                                  LHCb::Particle& Neutrino,
                                                  LHCb::Particle& BMeson,
                                                  LHCb::Vertex& VtxBMeson )
{
  StatusCode BFit;
  // Search for B- -> (N -> mu- pi+) mu -
  if ( m_Pion->particleID() == m_pipID ) {
    debug() << "B- Vertex Fit" << endmsg;
    BMeson = LHCb::Particle(m_BmID);
    BFit = m_Fit->fit(Neutrino, *Mu_Prim, VtxBMeson, BMeson);
  }
  // Search for B+ -> (N -> mu+ pi-) mu +
  if ( m_Pion->particleID() == m_pimID ){
    debug() << "B+ Vertex Fit" << endmsg;
    BMeson = LHCb::Particle(m_BpID);
    BFit = m_Fit->fit(Neutrino, *Mu_Prim, VtxBMeson, BMeson);
  }
  if ( 0 == BMeson.endVertex() ){
    warning() << "No B endvertex" << endmsg;
    return StatusCode::FAILURE;
  }

  return BFit;
}
//=============================================================================
// Clean and clear all pointer
//=============================================================================
StatusCode PromptNeutrinoTupleTool::m_cleanUp()
{
  debug() << "==> clean charged pointers" << endmsg;
  if ( m_Pion )
    m_Pion = NULL;
  if ( m_MuOne )
    m_MuOne = NULL;
  if ( m_MuTwo )
    m_MuTwo = NULL;
  //clean composite pointers
  // if ( m_Neutrino_1 )
  //   delete m_Neutrino_1;
  // if ( m_BMeson_1 )
  //   delete m_BMeson_1;
  // if ( m_VtxBMeson_1 )
  //   delete m_VtxBMeson_1;
  // if ( m_VtxNeutrino_1 )
  //   delete m_VtxNeutrino_1;

  // if ( m_Neutrino_2 )
  //   delete m_Neutrino_2;
  // if ( m_BMeson_2 )
  //   delete m_BMeson_2;
  // if ( m_VtxBMeson_2 )
  //   delete m_VtxBMeson_2;
  // if ( m_VtxNeutrino_2 )
  //   delete m_VtxNeutrino_2;
  debug() << "==> Finished cleaning Pointers" << endmsg;
  return StatusCode::SUCCESS;
}
//=============================================================================
