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

variables['btag'] = {
    'name': 'Electron_btagDeepB*(Electron_btagDeepB>0.)',
    'range': (20, 0., 1.),
    'xaxis': 'score'
}

variables['cvsb'] = {
    'name': '1. / (1. + Electron_btagDeepB / Electron_btagDeepC)',
    'range': (20, 0., 1.),
    'xaxis': 'score'
}

variables['cvsl'] = {
    'name': 'Electron_btagDeepC / (1. - Electron_btagDeepB)',
    'range': (20, 0., 1.),
    'xaxis': 'score'
}
