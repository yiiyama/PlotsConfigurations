#include "LatinoAnalysis/MultiDraw/interface/TTreeFunction.h"
#include "LatinoAnalysis/MultiDraw/interface/FunctionLibrary.h"

#include "BTagCalibrationStandalone.h"

#include "TSystem.h"

#include <string>
#include <unordered_map>
#include <iostream>

class BtagSF : public multidraw::TTreeFunction {
public:
  BtagSF(char const* algo);

  char const* getName() const override { return "BtagSF"; }
  TTreeFunction* clone() const override { return new BtagSF(algoName_.c_str()); }

  unsigned getNdata() override;
  double evaluate(unsigned) override;

protected:
  typedef std::array<std::unique_ptr<BTagCalibrationReader>, 3> Readers;
  static std::unordered_map<std::string, Readers> readersLib_;
  
  void bindTree_(multidraw::FunctionLibrary&) override;

  std::string algoName_{};
  Readers& readers_;

  UIntValueReader* nElectron{};
  IntArrayReader* Electron_jetIdx{};
  FloatArrayReader* Jet_pt{};
  FloatArrayReader* Jet_eta{};
  IntArrayReader* Jet_hadronFlavour{};
  FloatArrayReader* Jet_btag{};
};

std::unordered_map<std::string, BtagSF::Readers> BtagSF::readersLib_;

BtagSF::BtagSF(char const* algo) :
  TTreeFunction(),
  algoName_(algo),
  readers_(readersLib_[algoName_])
{
}

unsigned
BtagSF::getNdata()
{
  return *nElectron->Get();
}

double
BtagSF::evaluate(unsigned iE)
{
  int jetIdx(Electron_jetIdx->At(iE));
  if (jetIdx < 0)
    return 1.;

  BTagEntry::JetFlavor jf;
  
  switch (Jet_hadronFlavour->At(jetIdx)) {
  case 5:
    jf = BTagEntry::FLAV_B; // = 0
    break;
  case 4:
    jf = BTagEntry::FLAV_C; // = 1
    break;
  default:
    jf = BTagEntry::FLAV_UDSG; // = 2
    break;
  }
  
  return readers_[jf]->eval_auto_bounds("central", 
                                 jf,
                                 std::abs(Jet_eta->At(jetIdx)),
                                 Jet_pt->At(jetIdx),
                                 Jet_btag->At(jetIdx)); 
}

void
BtagSF::bindTree_(multidraw::FunctionLibrary& _library)
{
  std::string branchName;
  std::string fileName;
  
  if (algoName_ == "csvv2") {
    branchName = "Jet_btagCSVV2";
    fileName = std::string(gSystem->Getenv("CMSSW_BASE")) + "/src/PhysicsTools/NanoAODTools/data/btagSF/CSVv2_94XSF_V2_B_F.csv";
  }
  else if (algoName_ == "cmva") {
    branchName = "Jet_btagCMVA";
    fileName = std::string(gSystem->Getenv("CMSSW_BASE")) + "/src/PhysicsTools/NanoAODTools/data/btagSF/btagSF_cMVAv2_ichep2016.csv";
  }
  else if (algoName_ == "deepcsv") {
    branchName = "Jet_btagDeepB";
    fileName = std::string(gSystem->Getenv("CMSSW_BASE")) + "/src/PhysicsTools/NanoAODTools/data/btagSF/DeepCSV_94XSF_V1_B_F.csv";
  }
  else if (algoName_ == "deepflavour") {
    branchName = "Jet_btagDeepFlavB";
    fileName = std::string(gSystem->Getenv("CMSSW_BASE")) + "/src/PhysicsTools/NanoAODTools/data/btagSF/DeepFlavour_94XSF_V2_B_F.csv";
  }

  if (!readers_[0]) {
    std::cout << "Loading data for " << algoName_ << " from " << fileName << std::endl;
    // sets the static reader
    BTagCalibration calib(algoName_, fileName);
    for (auto& reader : readers_)
      reader.reset(new BTagCalibrationReader(BTagEntry::OP_RESHAPING, "central"));
    readers_[0]->load(calib, BTagEntry::FLAV_B, "iterativefit");
    readers_[1]->load(calib, BTagEntry::FLAV_C, "iterativefit");
    readers_[2]->load(calib, BTagEntry::FLAV_UDSG, "iterativefit");
    std::cout << "  done." << std::endl;
  }

  nElectron = &_library.getValue<UInt_t>("nElectron");
  Electron_jetIdx = &_library.getArray<Int_t>("Electron_jetIdx");
  Jet_pt = &_library.getArray<Float_t>("Jet_pt");
  Jet_eta = &_library.getArray<Float_t>("Jet_eta");
  Jet_hadronFlavour = &_library.getArray<Int_t>("Jet_hadronFlavour");
  Jet_btag = &_library.getArray<Float_t>(branchName.c_str());

}
