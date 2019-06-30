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

netabins = len(etabinning) - 1
nptbins = len(ptbinning) - 1

teta = '+'.join(['(TMath::Abs(Electron_eta[trailE_SS2E]) > %.1f)' % th for th in etabinning[1:-1]])
tpt = '%d*(%s)' % (netabins, '+'.join(['(Electron_pt[trailE_SS2E] > %.0f)' % th for th in ptbinning[1:-1]]))
leta = '%d*(%s)' % (nptbins * netabins, '+'.join(['(TMath::Abs(Electron_eta[leadE_SS2E]) > %.1f)' % th for th in etabinning[1:-1]]))
lpt = '%d*(%s)' % (nptbins * netabins * netabins, '+'.join(['(Electron_pt[leadE_SS2E] > %.0f)' % th for th in ptbinning[1:-1]]))

nbins = nptbins * nptbins * netabins * netabins

variables['counts'] = {
    'name': '%s+%s+%s+%s' % (teta, tpt, leta, lpt),
    'range': (nbins, 0., float(nbins)),
    'xaxis': 'ibin'
}
