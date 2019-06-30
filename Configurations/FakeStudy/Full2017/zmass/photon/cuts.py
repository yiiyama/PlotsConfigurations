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

def addcut(name, exprs):
    cuts[name] = {'expr': ' && '.join(exprs)}

baseSel = ['TMath::Odd(Photon_cutBasedBitmap / 2)', 'Photon_pt > 13.', 'Photon_pt < 53.', 'TMath::Abs(Photon_eta) < 2.5']
baseSel.extend(['Photon_2MG_minDRMu < 0.8', 'Photon_2MG_minDRMu > 0.1', 'Photon_2MG_mmmg + mmm_2MG < 185.'])
onZSel = ['Photon_2MG_mmmg > 80.', 'Photon_2MG_mmmg < 100.']

supercut = 'passDimuonPhotonSkim && Sum$(%s) != 0' % (' && '.join(baseSel))

categories = []
for ieta in range(0, len(etabinning) - 1):
    for ipt in range(0, len(ptbinning) - 1):
        categories.append('pt%d_eta%d' % (ipt, ieta))
        
categorization = ('-1+(Photon_pt>%f)*(1+' % ptbinning[0]) + '+'.join('(Photon_pt>%f)' % th for th in ptbinning[1:-1]) + ('+%d*(' % (len(ptbinning) - 1)) + '+'.join('(TMath::Abs(Photon_eta)>%f)' % th for th in etabinning[1:-1]) + '))'

addcut('base', baseSel)
addcut('basebinned', baseSel)
addcut('onZ', baseSel + onZSel)

cuts['basebinned']['categorization'] = categorization
cuts['basebinned']['categories'] = categories
