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
    from common import ptbinning, etabinning, tnames, snames
except ImportError:
    confdir = os.getenv('CMSSW_BASE') + '/src/PlotsConfigurations/Configurations/FakeStudy/Full2017'
    sys.path.append(confdir)
    from common import ptbinning, etabinning, tnames, snames

variables['counts_target'] = {
    'name': 'Electron_isBaseline',
    'range': (1, 0.5, 1.5),
    'xaxis': '',
    'cuts': ['ptag']
}

variables['dist_target'] = {
    'name': ('TMath::Abs(Electron_eta)', 'Electron_pt'),
    'range': (ptbinning, etabinning),
    'xaxis': '',
    'cuts': ['ptag']
}

fname = '/afs/cern.ch/work/y/yiiyama/hww/fakefinal/datatf.root'

for source in snames:
    if source == 'prompt':
        continue

    for tag in tnames:
        weight = {'source': '%s:%s_%s_weightmap' % (fname, source, tag), 'xexpr': 'Electron_pt', 'yexpr': 'TMath::Abs(Electron_eta)'}
        
        variables['counts_%s_%s' % (tag, source)] = {
            'name': 'Electron_isBaseline',
            'range': (1, 0.5, 1.5),
            'xaxis': '',
            'samples': ['DATA'],
            'cuts': [tag],
            'weight': weight
        }

        variables['dist_%s_%s' % (tag, source)] = {
            'name': ('TMath::Abs(Electron_eta)', 'Electron_pt'),
            'range': (ptbinning, etabinning),
            'xaxis': '',
            'samples': ['DATA'],
            'cuts': [tag],
            'weight': weight
        }
