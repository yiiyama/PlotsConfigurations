tnames = ['ptag', 'btag', 'ctag', 'ltag', 'gtag']
snames = ['prompt', 'bhadron', 'chadron', 'light', 'conversion']

ptbinning = [13., 15., 17., 20., 25., 30., 53.]
etabinning = [0., 0.4, 0.8, 1.47, 2., 2.5]

nminus1tight = '&&'.join(['((Electron_vidNestedWPBitmap/{shift})%8)>=4'.format(shift=8**i) for i in [2, 5, 7]] + ['((Electron_vidNestedWPBitmap/{shift})%8)>=1'.format(shift=8**i) for i in [3, 4, 6]])
jetIdx = 'Electron_jetIdx*(Electron_jetIdx>=0)+999*(Electron_jetIdx<0)'
coverb = '(1. / (1. + Electron_btagDeepB / Electron_btagDeepC))'
coverl = 'Electron_btagDeepC/(1.-Electron_btagDeepB)'

tagCuts = {
    'ptag': ['Electron_isTight'],
#    'btag': ['Electron_cutBased != 0', 'Electron_jetIdx >= 0', 'Electron_btag'],
    'btag': ['Electron_cutBased != 0', 'Electron_jetIdx >= 0', 'Electron_btagDeepB > 0.35'],
    'ctag': ['Electron_cutBased != 0', 'Electron_pfRelIso03_all > 0.', 'Electron_lostHits == 0', 'Electron_jetIdx >= 0', '{0} > 0.33'.format(coverb), '{0} > 0.2'.format(coverl)],
    'ltag': ['Electron_cutBased != 0', 'Electron_pfRelIso03_all > 0.', 'Electron_lostHits == 0', 'Electron_jetIdx >= 0', 'Electron_btagDeepB <= 0.', '{0} <= 0.'.format(coverl), 'Jet_btagCSVV2[Electron_jetIdx*(Electron_jetIdx>=0)]*(Electron_jetIdx>=0) > 0.4'],
    'gtag': [nminus1tight, 'Electron_jetIdx >= 0', 'Electron_btagDeepB < 0.1', '((TMath::Abs(Electron_eta) < 1.479 && Electron_lostHits > 0) || (TMath::Abs(Electron_eta) > 1.479 && Electron_lostHits > 1) || !Electron_convVeto)']
}
