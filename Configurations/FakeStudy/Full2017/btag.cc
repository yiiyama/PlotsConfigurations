#include "LatinoAnalysis/MultiDraw/interface/TTreeFunction.h"
#include "LatinoAnalysis/MultiDraw/interface/FunctionLibrary.h"

class Btag : public multidraw::TTreeFunction {
public:
  Btag(char const*);

  char const* getName() const override { return "Btag"; }
  TTreeFunction* clone() const override { return new Btag(tagName_); }

  unsigned getNdata() override;
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;

  TString tagName_{};
  double min_{0.};
  double max_{1.};

  UIntValueReader* nElectron{};
  IntArrayReader* Electron_jetIdx{};
  FloatArrayReader* Jet_btag{};
};

Btag::Btag(char const* name) :
  TTreeFunction(),
  tagName_(name)
{
  if (tagName_ == "CMVA")
    min_ = -1.;
}

unsigned
Btag::getNdata()
{
  return *nElectron->Get();
}

double
Btag::evaluate(unsigned iE)
{
  int jetIdx(Electron_jetIdx->At(iE));
  if (jetIdx < 0)
    return min_;

  double tag(Jet_btag->At(jetIdx));
  if (tag < min_)
    return min_;
  else if (tag > max_)
    return max_;
  else
    return tag;
}

void
Btag::bindTree_(multidraw::FunctionLibrary& _library)
{
  nElectron = &_library.getValue<UInt_t>("nElectron");
  Electron_jetIdx = &_library.getArray<Int_t>("Electron_jetIdx");
  Jet_btag = &_library.getArray<Float_t>("Jet_btag" + tagName_);
}
