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

def addcut(name, exprs):
    cuts[name] = {'expr': ' && '.join(exprs)}

# uncomment once reskimmed
#baseSel = ['Electron_isBaseline', 'Electron_pt > 13.', 'Electron_pt < 53.', 'TMath::Abs(Electron_eta) < 2.5', 'Electron_2ME_isCaloIdLTrackIdLIsoVL']
baseSel = ['Electron_isBaseline', 'Electron_pt > 13.', 'Electron_pt < 53.', 'TMath::Abs(Electron_eta) < 2.5']
baseSel += ['Electron_2ME_minDRMu < 0.8', 'Electron_2ME_minDRMu > 0.1', 'Electron_2ME_mmme + mmm_2ME < 185.']
onZSel = ['Electron_2ME_mmme > 80.', 'Electron_2ME_mmme < 100.']

supercut = 'passDimuonElectronSkim && Sum$(%s) != 0' % (' && '.join(baseSel))

categories = []
for ieta in range(0, len(etabinning) - 1):
    for ipt in range(0, len(ptbinning) - 1):
        categories.append('pt%d_eta%d' % (ipt, ieta))
        
categorization = ('-1+(Electron_pt>%f)*(1+' % ptbinning[0]) + '+'.join('(Electron_pt>%f)' % th for th in ptbinning[1:-1]) + ('+%d*(' % (len(ptbinning) - 1)) + '+'.join('(TMath::Abs(Electron_eta)>%f)' % th for th in etabinning[1:-1]) + '))'

addcut('base', baseSel)
addcut('basebinned', baseSel)
addcut('onZ', baseSel + onZSel)

cuts['basebinned']['categorization'] = categorization
cuts['basebinned']['categories'] = categories

for tag, sel in tagCuts.iteritems():
    addcut('base_%s' % tag, baseSel + sel)
    addcut('basebinned_%s' % tag, baseSel + sel)
    addcut('onZ_%s' % tag, baseSel + onZSel + sel)

    cuts['basebinned_%s' % tag]['categorization'] = categorization
    cuts['basebinned_%s' % tag]['categories'] = categories
