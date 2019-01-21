#ifndef NEUTRINOBUILDTUPLETOOL_H 
#define NEUTRINOBUILDTUPLETOOL_H 1


// Include files
// from Gaudi
#include "GaudiAlg/GaudiTool.h"
#include "Kernel/IParticleTupleTool.h"            // Interface
#include "DecayTreeTupleBase/TupleToolBase.h"
#include "Event/RecVertex.h"
#include "Event/Particle.h"
#include "Kernel/ParticleID.h"
#include "Kernel/ParticleProperty.h"
#include "Kernel/IParticlePropertySvc.h"
#include "Kernel/IRelatedPVFinder.h"
#include "Kernel/IVertexFit.h"
#include "TROOT.h"
#include "TLorentzVector.h"
#include "TMath.h"

#include <Kernel/GetIDVAlgorithm.h>
#include <Kernel/IDVAlgorithm.h>
#include <Kernel/ILifetimeFitter.h>
#include <Kernel/IDistanceCalculator.h>

/** @class NeutrinoBuildTupleTool NeutrinoBuildTupleTool.h
 *  
 *
 *  @author Christian Voss && Meriem Boubdir
 *  @date   2017-04-10
 */
class NeutrinoBuildTupleTool : public TupleToolBase, virtual public IParticleTupleTool { 

public:
  /// Standard constructor
  NeutrinoBuildTupleTool( const std::string& type, 
                          const std::string& name,
                          const IInterface* parent);
  
  ~NeutrinoBuildTupleTool( ){} ; ///< Destructor

  StatusCode initialize() override;

  StatusCode fill         ( const LHCb::Particle*,
                                    const LHCb::Particle*,
                                    const std::string&,
                                    Tuples::Tuple&) override;
  
protected:

private:
  StatusCode m_fillVariables      ( Tuples::Tuple& tuple);
  StatusCode m_fillBlankVariables ( Tuples::Tuple& tuple);
  StatusCode m_getCharedParticles ( const LHCb::Particle* part);
  StatusCode m_recoNeutrino       ();
  StatusCode m_recoBMeson         ();
  StatusCode m_cleanUp            ();
  
  double m_pMass, m_piMass, m_KMass;
  const IVertexFit *m_Fit;
  LHCb::IParticlePropertySvc *m_ppSvc;
  LHCb::ParticleID m_JpsiID, m_muPlusID, mupInfo, m_muMinusID;
  LHCb::ParticleID m_pimID, m_pipID, m_BpID, m_BmID;
  LHCb::ParticleID m_LambdaID, m_LambdabarID;

  LHCb::Particle *m_Neutrino, *m_BMeson;
  const LHCb::Particle *m_Pion, *m_MuPlus, *m_MuMinus;
  const LHCb::Vertex *m_BPV;
  bool m_Normaliation;
  const IRelatedPVFinder *m_PVFinder;
  const IDistanceCalculator *m_DistCalc;
  const ILifetimeFitter *m_lifetime;
  IDVAlgorithm* m_dva;
  std::string m_DataPVLocation, m_VertexFitterName, m_Particle2PVRelatorName;

  LHCb::Vertex *m_VtxBMeson;
  LHCb::Vertex *m_VtxNeutrino;

};

#endif // NEUTRINOBUILDTUPLETOOL_H
