
// Include files 

// from Gaudi
#include "GaudiKernel/ToolFactory.h" 

// local
#include "NeutrinoBuildTupleTool.h"

using namespace LHCb;

//-----------------------------------------------------------------------------
// Implementation file for class : NeutrinoBuildTupleTool
//
// 2017-04-10 : Christian Voss && Meriem Boubdir
//-----------------------------------------------------------------------------

// Declaration of the Tool Factory
DECLARE_TOOL_FACTORY( NeutrinoBuildTupleTool )


//=============================================================================
// Standard constructor, initializes variables
//=============================================================================
NeutrinoBuildTupleTool::NeutrinoBuildTupleTool( const std::string& type,
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
//inline NeutrinoBuildTupleTool::~NeutrinoBuildTupleTool() {} 
// NeutrinoBuildTupleTool::~NeutrinoBuildTupleTool() {}

//=============================================================================
StatusCode NeutrinoBuildTupleTool::initialize()
{
  if( ! TupleToolBase::initialize() ) return StatusCode::FAILURE;
  m_dva = Gaudi::Utils::getIDVAlgorithm ( contextSvc(), this ) ;
  if (0==m_dva) return Error("Couldn't get parent DVAlgorithm", StatusCode::FAILURE);
  
  m_Fit      = m_dva->vertexFitter();
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
  
  m_JpsiID      = JpsiInfo->particleID();
  m_muPlusID    = mupInfo->particleID();
  m_muMinusID   = munInfo->particleID();
  m_pimID       = pimInfo->particleID();
  m_pipID       = pipInfo->particleID();
  m_BpID        = BpInfo->particleID();
  m_BmID        = BmInfo->particleID();
  m_LambdaID    = LambdaInfo->particleID();
  m_LambdabarID = LambdaInfo->antiParticle()->particleID();

  return StatusCode::SUCCESS;
}
//=============================================================================
// Overwrite pure virtual void fill method for IParticleTupleTool
//=============================================================================
StatusCode NeutrinoBuildTupleTool::fill (const LHCb::Particle* top,
                                         const LHCb::Particle* part,
                                         const std::string& head,
                                         Tuples::Tuple &tuple)
{
  m_BPV = (const LHCb::Vertex*)m_dva->bestVertex(part);
  if ( 0 == m_BPV)
    warning() << "No PV accessable" << endmsg;
  
  m_Neutrino = NULL; m_BMeson = NULL; m_Pion = NULL; m_MuPlus = NULL; m_MuMinus = NULL;
  m_VtxBMeson = NULL; m_VtxNeutrino = NULL;
  
  StatusCode FoundChargedParticles =  NeutrinoBuildTupleTool::m_getCharedParticles(part);
  if ( FoundChargedParticles == StatusCode::FAILURE ){
    debug() << "==> Charge Check" << endmsg;
    NeutrinoBuildTupleTool::m_fillBlankVariables( tuple );
    return NeutrinoBuildTupleTool::m_cleanUp();
  }
  
  StatusCode GoodNeutrinoFit       =  NeutrinoBuildTupleTool::m_recoNeutrino();
  if ( GoodNeutrinoFit == StatusCode::FAILURE ){
    debug() << "==> Neutrino reco" << endmsg;
    NeutrinoBuildTupleTool::m_fillBlankVariables( tuple );
    return NeutrinoBuildTupleTool::m_cleanUp();
  }
    
  StatusCode GoodBFit              =  NeutrinoBuildTupleTool::m_recoBMeson();
  if ( GoodBFit == StatusCode::FAILURE ){
    debug() << "==> B Reco" << endmsg;
    NeutrinoBuildTupleTool::m_fillBlankVariables( tuple );
    return NeutrinoBuildTupleTool::m_cleanUp(); 
  }
  if ( FoundChargedParticles == StatusCode::SUCCESS )
    if ( GoodNeutrinoFit == StatusCode::SUCCESS )
      if ( GoodBFit == StatusCode::SUCCESS ){
        debug() << "==> Write Tuples" << endmsg;
        NeutrinoBuildTupleTool::m_fillVariables( tuple );
        return NeutrinoBuildTupleTool::m_cleanUp(); 
      }
  
  warning() << "Inconsistent Neutrino Substitution" << endmsg;
  return StatusCode::SUCCESS;
}
//=============================================================================
// Fill variables for valid Neutrino candidates
//=============================================================================
StatusCode NeutrinoBuildTupleTool::m_fillVariables( Tuples::Tuple& tuple )
{
  tuple->column( "N_ORIVX_CHI2", m_BMeson->endVertex()->chi2() );
  tuple->column( "N_ORIVX_NDOF", m_BMeson->endVertex()->nDoF() );
  tuple->column( "N_ORIVX_X",    m_BMeson->endVertex()->position().x() );
  tuple->column( "N_ORIVX_Y",    m_BMeson->endVertex()->position().y() );
  tuple->column( "N_ORIVX_Z",    m_BMeson->endVertex()->position().z() );

  tuple->column( "N_ENDVERTEX_CHI2", m_Neutrino->endVertex()->chi2() );
  tuple->column( "N_ENDVERTEX_NDOF", m_Neutrino->endVertex()->nDoF() );
  tuple->column( "N_ENDVERTEX_X",    m_Neutrino->endVertex()->position().x() );
  tuple->column( "N_ENDVERTEX_Y",    m_Neutrino->endVertex()->position().y() );
  tuple->column( "N_ENDVERTEX_Z",    m_Neutrino->endVertex()->position().z() );

  tuple->column( "N_M",  m_Neutrino->momentum().M() );
  tuple->column( "N_MM", m_Neutrino->measuredMass() );
  tuple->column( "N_PX", m_Neutrino->momentum().px() );
  tuple->column( "N_PY", m_Neutrino->momentum().py() );
  tuple->column( "N_PZ", m_Neutrino->momentum().pz() );
  tuple->column( "N_PE", m_Neutrino->momentum().E() );
  /*
  TVector3::TVector3 FlN, Np;  
  FlN.SetX( - (m_BMeson)->endVertex()->position().x() + (m_Neutrino)->endVertex()->position().x() );
  FlN.SetY( - (m_BMeson)->endVertex()->position().y() + (m_Neutrino)->endVertex()->position().y() );
  FlN.SetZ( - (m_BMeson)->endVertex()->position().z() + (m_Neutrino)->endVertex()->position().z() );
  Np.SetX( (m_Neutrino)->momentum().px() );
  Np.SetY( (m_Neutrino)->momentum().py() );
  Np.SetZ( (m_Neutrino)->momentum().pz() );
  
  double theta_DIRA =  Np.Angle(FlN);
  
  if ( isnan( theta_DIRA ) ){
    warning() << "NAN for Neutrino DIRA angle" << endmsg;
    tuple->column( "N_DIRA_ORIVX", -1e30 );
  }
  else
    tuple->column( "N_DIRA_ORIVX", cos(theta_DIRA ) );
  */
  double dist(-1e30), chi2(-1e30);
  m_DistCalc->distance ( m_Neutrino, m_BPV, dist, chi2);
  tuple->column( "N_IP_OWNPV", dist ) ;
  tuple->column( "N_IPCHI2_OWNPV", chi2  );
  debug() << "==> N lifetime" << endmsg;
  double pt(-1e30), ept(-1e30), ptchi2(-1e30);
  StatusCode sc = m_lifetime->fit ( *(m_BMeson->endVertex()), *(m_Neutrino) , pt, ept, ptchi2 );
  if( !sc ){
    Warning("The propertime fit failed").ignore();
    pt   = -1e30;
    ept  = -1e30;
    ptchi2 = -1e30;
  }
  
  tuple->column( "N_TAU" , pt ); // nanoseconds
  tuple->column( "N_TAUERR" , ept );
  tuple->column( "N_TAUCHI2" , chi2 );

  dist = -1e30;
  chi2 = -1e30;

  sc = m_DistCalc->distance( m_BMeson->endVertex(), m_Neutrino->endVertex(), dist, chi2 );
  if ( sc.isFailure() ){
    dist = -1e30;
    chi2 = -1e30;
  }
  tuple->column( "N_FD_ORIVX", dist );
  tuple->column( "N_FDCHI2_ORIVX", chi2 );

  return StatusCode::SUCCESS;
}
//=============================================================================
// Fill blank variables for failed Vertex fits
//=============================================================================
StatusCode NeutrinoBuildTupleTool::m_fillBlankVariables( Tuples::Tuple& tuple )
{
  tuple->column( "N_ORIVX_CHI2", -1e30 );
  tuple->column( "N_ORIVX_NDOF", -1e30 );
  tuple->column( "N_ORIVX_X",    -1e30 );
  tuple->column( "N_ORIVX_Y",    -1e30 );
  tuple->column( "N_ORIVX_Z",    -1e30 );

  tuple->column( "N_ENDVERTEX_CHI2", -1e30 );
  tuple->column( "N_ENDVERTEX_NDOF", -1e30 );
  tuple->column( "N_ENDVERTEX_X", -1e30 );
  tuple->column( "N_ENDVERTEX_Y", -1e30 );
  tuple->column( "N_ENDVERTEX_Z", -1e30 );
  
  tuple->column( "N_M", -1e30  );
  tuple->column( "N_MM", -1e30  );
  tuple->column( "N_PX", -1e30 );
  tuple->column( "N_PY", -1e30 );
  tuple->column( "N_PZ", -1e30 );
  tuple->column( "N_PE", -1e30 );
  
  //tuple->column( "N_DIRA_ORIVX", -1e30 );
  
  tuple->column( "N_IP_OWNPV", -1e30 ) ;
  tuple->column( "N_IPCHI2_OWNPV", -1e30 );

  tuple->column( "N_TAU" , -1e30 ); // nanoseconds
  tuple->column( "N_TAUERR" , -1e30 );
  tuple->column( "N_TAUCHI2" , -1e30 );
  
  tuple->column( "N_FD_ORIVX", -1e30 );
  tuple->column( "N_FDCHI2_ORIVX", -1e30 );
  
  return StatusCode::SUCCESS;
}
//=============================================================================
// Ceck for charged candidates
//=============================================================================
StatusCode NeutrinoBuildTupleTool::m_getCharedParticles(const LHCb::Particle* part)
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
        for( IterJpsi = JpsiDaughters.begin(); IterJpsi != JpsiDaughters.end(); ++IterJpsi){
          if ( (*IterJpsi)->particleID() == m_muPlusID )
            m_MuPlus = (*IterJpsi);
          if ( (*IterJpsi)->particleID() == m_muMinusID )
            m_MuMinus = (*IterJpsi);
        }
      }
    }
  }

  if ( m_Pion && m_MuPlus && m_MuMinus )
    return StatusCode::SUCCESS;
  else
    return StatusCode::FAILURE;
}
//=============================================================================
// Neutrino reconstruction
//=============================================================================
StatusCode NeutrinoBuildTupleTool::m_recoNeutrino()
{
  StatusCode NFit;
  // Search for N -> mu- pi +
  if ( m_Pion->particleID() == m_pipID ){
    m_Neutrino = new LHCb::Particle(m_LambdaID);
    m_VtxNeutrino = new LHCb::Vertex();
    NFit = m_Fit->fit(*m_Pion, *m_MuMinus, *m_VtxNeutrino, *m_Neutrino);
  }
  // Search for N -> mu+ pi -
  if ( m_Pion->particleID() == m_pimID ){
    m_Neutrino = new LHCb::Particle(m_LambdabarID);
    m_VtxNeutrino = new LHCb::Vertex();
    NFit = m_Fit->fit(*m_Pion, *m_MuPlus, *m_VtxNeutrino, *m_Neutrino);
  }
  if ( 0 == m_Neutrino->endVertex() )
    warning() << "No N endvertex" << endmsg;
  return NFit;
}
//=============================================================================
// B candidate reconstruction
//=============================================================================
StatusCode NeutrinoBuildTupleTool::m_recoBMeson()
{
  StatusCode BFit;
  // Search for B+ -> (N -> mu- pi+) mu +
  if ( m_Pion->particleID() == m_pipID ) {
    m_BMeson = new LHCb::Particle(m_BpID);
    m_VtxBMeson = new LHCb::Vertex();
    BFit = m_Fit->fit(*m_Neutrino, *m_MuPlus, *m_VtxBMeson, *m_BMeson);
  }
  // Search for B- -> (N -> mu+ pi-) mu -
  if ( m_Pion->particleID() == m_pimID ){
    m_BMeson = new LHCb::Particle(m_BmID);
    m_VtxBMeson = new LHCb::Vertex();
    BFit = m_Fit->fit(*m_Neutrino, *m_MuMinus, *m_VtxBMeson, *m_BMeson);
  }
  if ( 0 == m_BMeson->endVertex() )
    warning() << "No B endvertex" << endmsg; 
  return BFit;
}
//=============================================================================
// Clean and clear all pointer
//=============================================================================
StatusCode NeutrinoBuildTupleTool::m_cleanUp()
{
  //clean charged pointers
  if ( m_Pion )
    m_Pion = NULL;
  if ( m_MuPlus )
    m_MuPlus = NULL;
  if ( m_MuMinus )
    m_MuMinus = NULL;
  //clean composite pointers
  if ( m_Neutrino )
    delete m_Neutrino;
  if ( m_BMeson )
    delete m_BMeson;
  if ( m_VtxBMeson )
    delete m_VtxBMeson;
  if ( m_VtxNeutrino )
    delete m_VtxNeutrino;
  
  return StatusCode::SUCCESS;
}
//=============================================================================
