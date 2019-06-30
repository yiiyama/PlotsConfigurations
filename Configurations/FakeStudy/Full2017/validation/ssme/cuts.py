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

# uncomment once reskimmed
#baseSel = ['Electron_isBaseline', 'Electron_isCaloIdLTrackIdLIsoVL', 'Electron_pt < %f' % ptbinning[-1], 'Electron_pt < Muon_pt[tightMu_SSME]']
baseSel = ['Electron_isBaseline', 'Electron_pt < %f' % ptbinning[-1], 'Electron_pt < Muon_pt[tightMu_SSME]']

supercut = 'passSameSignMuonElectronSkim && Muon_pt[tightMu_SSME] > 25. && Sum$(%s) != 0' % (' && '.join(baseSel))

for tag, cut in tagCuts.iteritems():
    cuts[tag] = {
        'expr': ' && '.join(baseSel + cut)
    }

    if tag != 'ptag':
        cuts[tag]['samples'] = ['DATA']
