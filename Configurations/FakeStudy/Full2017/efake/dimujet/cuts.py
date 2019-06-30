import os
import sys

#cuts = {}

# imported from samples.py:
# samples, signals, pthBins, njetBinning

try:
    from common import ptbinning, etabinning
except ImportError:
    confdir = os.getenv('CMSSW_BASE') + '/src/PlotsConfigurations/Configurations/FakeStudy/Full2017'
    sys.path.append(confdir)
    from common import ptbinning, etabinning

nptbins = len(ptbinning) - 1
netabins = len(etabinning) - 1

supercut = 'passDimuonElectronSkim'

baseSel = ['Electron_isBaseline', 'Electron_2ME_minDRMu > 0.8']

categorization = '+'.join(['(TMath::Abs(Electron_eta) > %f)' % th for th in etabinning[1:-1]])
categorization += '+%d*(%s)' % (netabins, '+'.join(['(Electron_pt > %f)' % th for th in ptbinning[1:-1]]))
categories = ['pt%d_eta%d' % (ipt, ieta) for ipt in range(nptbins) for ieta in range(netabins)]

cuts['nojet'] = {
    'expr': ' && '.join(baseSel + ['mmm_2ME > 80.', 'mmm_2ME < 100.', 'Electron_2ME_njet == 0']),
    'categories': categories,
    'categorization': categorization
}

cuts['jets'] = {
    'expr': ' && '.join(baseSel + ['mmm_2ME > 80.', 'mmm_2ME < 100.', 'Electron_2ME_njet != 0']),
    'categories': categories,
    'categorization': categorization
}

cuts['top'] = {
    'expr': ' && '.join(baseSel + ['(mmm_2ME < 80. || mmm_2ME > 100.)', 'Electron_2ME_nbjet != 0']),
    'categories': categories,
    'categorization': categorization
}
