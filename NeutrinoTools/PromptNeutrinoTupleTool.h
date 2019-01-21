#ifndef PROMPTNEUTRINOTUPLETOOL_H 
#define PROMPTNEUTRINOTUPLETOOL_H 1

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

/** @class PromptNeutrinoTupleTool PromptNeutrinoTupleTool.h
 *  
 *
 *  @author Christian Voss && Meriem Boubdir
 *  @date   2017-04-13
 */

class PromptNeutrinoTupleTool : public TupleToolBase, virtual public IParticleTupleTool {
public: 
  /// Standard constructor
  PromptNeutrinoTupleTool( const std::string& type, 
                           const std::string& name,
                           const IInterface* parent);

  virtual ~PromptNeutrinoTupleTool( ); ///< Destructor

  virtual StatusCode initialize();

  virtual StatusCode fill         ( const LHCb::Particle *top,
                                    const LHCb::Particle *part,
                                    const std::string &head,
                                    Tuples::Tuple &tuple);

protected:

private:

  StatusCode m_fillVariables      ( Tuples::Tuple &tuple,
                                    std::string name,
                                    LHCb::Particle& Neutrino,
                                    LHCb::Particle& BMeson);

  StatusCode m_fillBlankVariables ( Tuples::Tuple &tuple,
                                    std::string name );

  StatusCode m_getCharedParticles ( const LHCb::Particle *part );

  StatusCode m_recoNeutrino       ( const LHCb::Particle *Mu_Sec,
                                    LHCb::Particle& Neutrino,
                                    LHCb::Vertex& VtxNeutrino);
  
  StatusCode m_recoBMeson         ( const LHCb::Particle *Mu_Prim,
                                    LHCb::Particle& Neutrino,
                                    LHCb::Particle& BMeson,
                                    LHCb::Vertex& VtxBMeson );
  
  StatusCode m_cleanUp            ();
  
  double m_pMass, m_piMass, m_KMass;
  const IVertexFit *m_Fit;
  LHCb::IParticlePropertySvc *m_ppSvc;
  LHCb::ParticleID m_JpsiID, m_muPlusID, mupInfo, m_muMinusID;
  LHCb::ParticleID m_pimID, m_pipID, m_BpID, m_BmID;
  LHCb::ParticleID m_LambdaID, m_LambdabarID;
  LHCb::ParticleID m_DeltaID, m_antiDeltaID;
  
  const LHCb::Particle *m_Pion;
  const LHCb::Particle *m_MuOne, *m_MuTwo;
  const LHCb::Vertex *m_BPV;
  bool m_Normaliation;
  const IRelatedPVFinder *m_PVFinder;
  const IDistanceCalculator *m_DistCalc;
  const ILifetimeFitter *m_lifetime;
  IDVAlgorithm* m_dva;
  std::string m_DataPVLocation, m_VertexFitterName, m_Particle2PVRelatorName;

  LHCb::Particle Neutrino_1; LHCb::Particle BMeson_1;
  LHCb::Particle Neutrino_2; LHCb::Particle BMeson_2;
  LHCb::Vertex VtxBMeson_1; LHCb::Vertex VtxNeutrino_1;
  LHCb::Vertex VtxBMeson_2; LHCb::Vertex VtxNeutrino_2;
  

};
#endif // PROMPTNEUTRINOTUPLETOOL_H
