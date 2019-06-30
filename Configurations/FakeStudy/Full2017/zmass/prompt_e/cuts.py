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

baseSel = ['Electron_isBaseline', 'Electron_pt > 13.', 'Electron_pt < 53.', 'TMath::Abs(Electron_eta) < 2.5', 'Electron_OS2E_isProbe']
onZSel = ['Electron_OS2E_mee > 80.', 'Electron_OS2E_mee < 100.']
# cannot reliably use TrigObj because legs of the dielectron trigger are not saved
#targetSel = baseSel + ['Electron_OS2E_isCaloIdLTrackIdLIsoVL']
targetSel = baseSel + ['(run == 1 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)']

supercut = 'passOppositeSignDielectronSkim && Sum$(%s) != 0' % (' && '.join(baseSel))

categories = []
for ieta in range(0, len(etabinning) - 1):
    for ipt in range(0, len(ptbinning) - 1):
        categories.append('pt%d_eta%d' % (ipt, ieta))
        
categorization = ('-1+(Electron_pt>%f)*(1+' % ptbinning[0]) + '+'.join('(Electron_pt>%f)' % th for th in ptbinning[1:-1]) + ('+%d*(' % (len(ptbinning) - 1)) + '+'.join('(TMath::Abs(Electron_eta)>%f)' % th for th in etabinning[1:-1]) + '))'

addcut('base', baseSel)
addcut('basebinned', baseSel)
addcut('onZ', baseSel + onZSel)
addcut('onZ_trig', targetSel + onZSel)

cuts['basebinned']['categorization'] = categorization
cuts['basebinned']['categories'] = categories

addcut('lowpt', baseSel + ['Electron_pt < 30.'])
addcut('highpt', baseSel + ['Electron_pt > 30.'])
addcut('highishpt', baseSel + ['Electron_pt > 30. && Electron_pt < 40.'])

for tag, sel in tagCuts.iteritems():
    addcut('base_%s' % tag, targetSel + sel)
    addcut('basebinned_%s' % tag, targetSel + sel)
    addcut('onZ_%s' % tag, targetSel + onZSel + sel)

    cuts['basebinned_%s' % tag]['categorization'] = categorization
    cuts['basebinned_%s' % tag]['categories'] = categories
