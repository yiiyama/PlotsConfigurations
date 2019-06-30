import os
import sys

#cuts = {}

# imported from samples.py:
# samples, signals, pthBins, njetBinning

try:
    from common import ptbinning, etabinning, tagCuts
except ImportError:
    confdir = os.getenv('CMSSW_BASE') + '/src/PlotsConfigurations/Configurations/FakeStudy/Full2017'
    sys.path.append(confdir)
    from common import ptbinning, etabinning, tagCuts

nptbins = len(ptbinning) - 1
netabins = len(etabinning) - 1

baseSel = ['Electron_isBaseline', '!Electron_tau', 'Electron_isCaloIdLTrackIdLIsoVL', 'Electron_pt < %f' % ptbinning[-1]]

supercut = 'passElectronSkim && Sum$(%s) != 0' % (' && '.join(baseSel))

categorization = '+'.join(['(TMath::Abs(Electron_eta) > %f)' % th for th in etabinning[1:-1]])
categorization += '+%d*(%s)' % (netabins, '+'.join(['(Electron_pt > %f)' % th for th in ptbinning[1:-1]]))
categories = ['pt%d_eta%d' % (ipt, ieta) for ipt in range(nptbins) for ieta in range(netabins)]

cuts['baseline'] = {
    'expr': ' && '.join(baseSel),
    'categories': categories,
    'categorization': categorization
}

for tag, sel in tagCuts.iteritems():
    cuts[tag] = {
        'expr': ' && '.join(baseSel + sel),
        'categories': categories,
        'categorization': categorization
    }
