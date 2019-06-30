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

try:
    from common import ptbinning, etabinning
except ImportError:
    import os
    import sys
    
    confdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    sys.path.append(confdir)
    from common import ptbinning, etabinning

onZ = [ckey for ckey in cuts if ckey.startswith('onZ')]
wide = [ckey for ckey in cuts if not ckey.startswith('onZ')]

variables['nZ'] = {
    'name': ('TMath::Abs(Electron_eta)', 'Electron_pt'),
    'range': (ptbinning, etabinning),
    'xaxis': 'pt',
    'yaxis': '|eta|',
    'cuts': onZ
}

variables['mass'] = {
    'name': 'Electron_OS2E_mee',
    'range': (120, 0., 120.),
    'xaxis': 'mass',
    'cuts': wide
}
