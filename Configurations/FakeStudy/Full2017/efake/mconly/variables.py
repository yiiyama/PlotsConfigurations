import os

#variables = {}

# imported from cuts.py
# cuts
# imported from samples.py
# samples signals

try:
    variables
except NameError:
    import collections
    variables = collections.OrderedDict()
    cuts = []

variables['counts'] = {
    'linesToAdd': [
        'gSystem->Load("libLatinoAnalysisMultiDraw.so");',
        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/BTagCalibrationStandalone.cpp+' % os.getenv('CMSSW_BASE'),
        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/btagsf.cc+' % os.getenv('CMSSW_BASE')
    ],
    'name': 'Electron_isBaseline',
    'range': (1, 0.5, 1.5),
    'xaxis': '',
    'weight': {'class': 'BtagSF', 'args': 'deepcsv'}
}    

variables['ptrel'] = {
    'linesToAdd': [
        'gSystem->Load("libLatinoAnalysisMultiDraw.so");',
        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/ptrel.cc+' % os.getenv('CMSSW_BASE'),
    ],
    'class': 'PtRel',
    'range': (40, 0., 20.),
    'xaxis': 'p_{T}^{rel}'
}

variables['r9'] = {
    'name': 'Electron_r9',
    'range': (20, 0., 1.),
    'xaxis': 'R_{9}'
}

variables['epdiff'] = {
    'name': 'Electron_pt * TMath::CosH(Electron_eta) * Electron_eInvMinusPInv',
    'range': (20, -25., 5.),
    'xaxis': '1-E/p'
}

variables['btag'] = {
    'linesToAdd': [
        'gSystem->Load("libLatinoAnalysisMultiDraw.so");',
        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/BTagCalibrationStandalone.cpp+' % os.getenv('CMSSW_BASE'),
        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/btagsf.cc+' % os.getenv('CMSSW_BASE')
    ],
    'name': 'Electron_btagDeepB*(Electron_btagDeepB>0.)',
    'range': ([0. + 0.05 * x for x in range(12)] + [0.6 + 0.02 * x for x in range(21)],),
    'xaxis': 'score',
    'weight': {'class': 'BtagSF', 'args': 'deepcsv'}
}

variables['cvsb'] = {
    'name': '1. / (1. + Electron_btagDeepB / Electron_btagDeepC)',
    'range': ([0. + 0.02 * x for x in range(15)] + [0.3 + 0.05 * x for x in range(8)] + [0.7 + 0.02 * x for x in range(10)] + [0.9, 1.],),
    'xaxis': 'score'
}

variables['cvsl'] = {
    'name': 'Electron_btagDeepC / (1. - Electron_btagDeepB)',
    'range': ([-0.4] + [0. + 0.02 * x for x in range(15)] + [0.3 + 0.05 * x for x in range(10)] + [0.8 + 0.02 * x for x in range(11)],),
    'xaxis': 'score'
}

#variables['plrel'] = {
#    'name': 'Electron_jetRelPl / Electron_pt / TMath::CosH(Electron_eta)',
#    'range': (41, -1., 1.05),
#    'xaxis': 'p_{L}^{rel}'
#}
#
#variables['ptreldirect'] = {
#    'name': 'Electron_jetRelPtDirect',
#    'range': (40, 0., 20.),
#    'xaxis': 'p_{T}^{rel}'
#}
#
#variables['plreldirect'] = {
#    'name': 'Electron_jetRelPlDirect / Electron_pt / TMath::CosH(Electron_eta)',
#    'range': (41, 0., 1.025),
#    'xaxis': 'p_{L}^{rel}'
#}
#
#variables['prest'] = {
#    'linesToAdd': [
#        'gSystem->Load("libLatinoAnalysisMultiDraw.so");',
#        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/prest.cc+' % os.getenv('CMSSW_BASE')
#    ],
#    'class': 'PRest',
#    'range': (40, 0., 10.),
#    'xaxis': 'p'
#}

#variables['cmva'] = {
#    'linesToAdd': [
#        'gSystem->Load("libLatinoAnalysisMultiDraw.so");',
#        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/btag.cc+' % os.getenv('CMSSW_BASE'),
#        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/BTagCalibrationStandalone.cpp+' % os.getenv('CMSSW_BASE'),
#        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/btagsf.cc+' % os.getenv('CMSSW_BASE')
#    ],
#    'class': 'Btag',
#    'args': 'CMVA',
#    'range': ([-1. + 0.04 * x for x in range(10)] + [-0.6 + 0.2 * x for x in range(7)] + [0.8 + 0.04 * x for x in range(6)],),
#    'xaxis': 'p',
#    'weight': {'class': 'BtagSF', 'args': 'cmva'}
#}

variables['csvv2'] = {
    'linesToAdd': [
        'gSystem->Load("libLatinoAnalysisMultiDraw.so");',
        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/btag.cc+' % os.getenv('CMSSW_BASE'),
        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/BTagCalibrationStandalone.cpp+' % os.getenv('CMSSW_BASE'),
        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/btagsf.cc+' % os.getenv('CMSSW_BASE')
    ],
    'class': 'Btag',
    'args': 'CSVV2',
    'range': ([0.] + [0.1 + 0.02 * x for x in range(46)],), # -10 possible
    'xaxis': 'p',
    'weight': {'class': 'BtagSF', 'args': 'csvv2'}
}

#variables['deepflavb'] = {
#    'linesToAdd': [
#        'gSystem->Load("libLatinoAnalysisMultiDraw.so");',
#        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/btag.cc+' % os.getenv('CMSSW_BASE'),
#        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/BTagCalibrationStandalone.cpp+' % os.getenv('CMSSW_BASE'),
#        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/btagsf.cc+' % os.getenv('CMSSW_BASE')
#    ],
#    'class': 'Btag',
#    'args': 'DeepFlavB',
#    'range': ([0. + 0.02 * x for x in range(10)] + [0.2 + 0.1 * x for x in range(6)] + [0.8 + 0.02 * x for x in range(11)],),
#    'xaxis': 'p',
#    'weight': {'class': 'BtagSF', 'args': 'deepflavour'}
#}

#variables['deepflavc'] = {
#    'linesToAdd': [
#        'gSystem->Load("libLatinoAnalysisMultiDraw.so");',
#        '.L %s/src/PlotsConfigurations/Configurations/FakeStudy/Full2017/btag.cc+' % os.getenv('CMSSW_BASE')
#    ],
#    'class': 'Btag',
#    'args': 'DeepFlavC',
#    'range': (40, 0., 1.),
#    'xaxis': 'p'
#}
