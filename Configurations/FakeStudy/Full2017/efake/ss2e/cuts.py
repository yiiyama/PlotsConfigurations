import os
import sys
import re

#cuts = {}

# imported from samples.py:
# samples, signals, pthBins, njetBinning

try:
    from common import jetIdx
except ImportError:
    confdir = os.getenv('CMSSW_BASE') + '/src/PlotsConfigurations/Configurations/FakeStudy/Full2017'
    sys.path.append(confdir)
    from common import jetIdx

meesq = '2. * Electron_pt[leadE_SS2E] * Electron_pt[trailE_SS2E] * (TMath::CosH(Electron_eta[leadE_SS2E] - Electron_eta[trailE_SS2E]) - TMath::Cos(Electron_phi[leadE_SS2E] - Electron_phi[trailE_SS2E]))'

supercut = ' && '.join([
    'passSameSignDielectronSkim',
    'Electron_pt[leadE_SS2E] > 13.', 'Electron_pt[leadE_SS2E] < 53.', 'TMath::Abs(Electron_eta[leadE_SS2E]) < 2.5',
    'Electron_pt[trailE_SS2E] > 13.', 'Electron_pt[trailE_SS2E] < 53.', 'TMath::Abs(Electron_eta[trailE_SS2E]) < 2.5',
    '({meesq} < 75. * 75. || {meesq} > 105. * 105.)'.format(meesq=meesq)
])

jetIdxlt = jetIdx.replace('jetIdx', 'jetIdx[{lt}]')

jpt = 'Alt$(Jet_pt[{jetIdx}],0.)'.format(jetIdx=jetIdxlt)
jeta = 'Alt$(Jet_eta[{jetIdx}],10.)'.format(jetIdx=jetIdxlt)
subst = {
    'jptlead': jpt.format(lt='leadE_SS2E'),
    'jetalead': jeta.format(lt='leadE_SS2E'),
    'jpttrail': jpt.format(lt='trailE_SS2E'),
    'jetatrail': jeta.format(lt='trailE_SS2E'),
}
njet = 'Sum$(Jet_pt > 30. && TMath::Abs(Jet_eta) < 4.7) - ({jptlead} > 30. && TMath::Abs({jetalead}) < 4.7) - ({jpttrail} > 30. && TMath::Abs({jetatrail}) < 4.7)'.format(**subst)

cuts['inclusive'] = {
    'expr': '1',
    'categories': ['nojet', 'onejet', 'multijet'],
    'categorization': 'TMath::Min({njet}, 2)'.format(njet=njet)
}
