import os
import sys
import re

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

baseSel = ['Electron_isBaseline', 'Electron_isCaloIdLTrackIdLIsoVL', 'Electron_pt < %f' % ptbinning[-1]]

supercut = 'passJetElectronSkim && Sum$(%s) != 0' % (' && '.join(baseSel))

categorization = '+'.join(['(TMath::Abs(Electron_eta) > %f)' % th for th in etabinning[1:-1]])
categorization += '+%d*(%s)' % (netabins, '+'.join(['(Electron_pt > %f)' % th for th in ptbinning[1:-1]]))
categories = ['pt%d_eta%d' % (ipt, ieta) for ipt in range(nptbins) for ieta in range(netabins)]

#cuts['onejet'] = {
#    'expr': ' && '.join(baseSel + ['Electron_JE_njet == 1']),
#    'categories': categories,
#    'categorization': categorization
#}
#
#cuts['multijet'] = {
#    'expr': ' && '.join(baseSel + ['Electron_JE_njet > 1']),
#    'categories': categories,
#    'categorization': categorization
#}

cuts['nobjet'] = {
    'expr': ' && '.join(baseSel + ['Electron_JE_nbjet == 0']),
    'categories': categories,
    'categorization': categorization
}

cuts['bjets'] = {
    'expr': ' && '.join(baseSel + ['Electron_JE_nbjet > 0']),
    'categories': categories,
    'categorization': categorization
}

for tag, cut in tagCuts.iteritems():
    cuts['nobjet_' + tag] = {
        'expr': ' && '.join(baseSel + cut + ['Electron_JE_nbjet == 0']),
        'categories': categories,
        'categorization': categorization
    }

    cuts['bjets_' + tag] = {
        'expr': ' && '.join(baseSel + cut + ['Electron_JE_nbjet > 0']),
        'categories': categories,
        'categorization': categorization
    }
