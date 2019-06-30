import os
from LatinoAnalysis.Tools.commonTools import *

try:
    len(samples)
except NameError:
    import collections
    samples = collections.OrderedDict()

mcProduction = 'Fall2017_nAOD_v1_Full2017v2'
dataReco = 'Run2017_nAOD_v1_Full2017v2'
mcSteps = 'MCl1loose2017v2__MCCorr2017__fakeSkimMC'
dataSteps = 'DATAl1loose2017v2__DATACorr2017__fakeSkimDATA'

##############################################
###### Tree Directory according to site ######
##############################################

SITE = os.uname()[1]
xrootdPath=''
if 'iihe' in SITE :
  xrootdPath = 'dcap://maite.iihe.ac.be/'
  treeBaseDir = '/pnfs/iihe/cms/store/user/xjanssen/HWW2015/'
elif 'cern' in SITE :
  treeBaseDir = '/eos/cms/store/cmst3/group/hww/HWWNano/'

mcDirectory = os.path.join(treeBaseDir, mcProduction, mcSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)

DataRun = [
    ['B','Run2017B-31Mar2018-v1'],
    ['C','Run2017C-31Mar2018-v1'],
    ['D','Run2017D-31Mar2018-v1'],
    ['E','Run2017E-31Mar2018-v1'],
    ['F','Run2017F-31Mar2018-v1']
]

####################

def nanoGetSampleFiles(inputDir, Sample):
    return getSampleFiles(inputDir, Sample, False, 'nanoLatino_')

try:
    from common import tagCuts, jetIdx
except ImportError:
    confdir = os.getenv('CMSSW_BASE') + '/src/PlotsConfigurations/Configurations/FakeStudy/Full2017'
    sys.path.append(confdir)
    from common import tagCuts, jetIdx

promptFiles = \
    nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin01') + \
    nanoGetSampleFiles(mcDirectory, 'ZZTo4L')

samples['VV'] = {
    'name': promptFiles,
    'weight': 'XSWeight*skimWeight_2ME*(Electron_prompt && !Electron_tau)',
    'FilesPerJob': 5
}

dyFiles = \
    nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO') + \
    nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50')

samples['dy'] = {
    'name': dyFiles,
    'weight': 'XSWeight*skimWeight_2ME*(!Electron_tau)',
    'FilesPerJob': 5
}

samples['top'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu'),
    'weight': 'XSWeight*skimWeight_2ME*(!Electron_tau)',
    'FilesPerJob': 5
}

#samples['ww'] = {
#    'name': nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu'),
#    'weight': 'XSWeight*skimWeight_2ME*(!Electron_tau)',
#    'FilesPerJob': 5
#}

subsamples = {
    'prompt': 'Electron_prompt',
    'bhadron': '!Electron_prompt && !Electron_conversion && Electron_hadronFlavour == 5',
    'chadron': '!Electron_prompt && !Electron_conversion && Electron_hadronFlavour == 4',
    'light': '!Electron_prompt && !Electron_conversion && Electron_hadronFlavour == 0',
    'conversion': '!Electron_prompt && Electron_conversion'
}

samples['dy']['subsamples'] = subsamples
samples['top']['subsamples'] = subsamples
#samples['ww']['subsamples'] = subsamples

samples['DATA'] = {
    'name': [],
    'weight': '1',
    'isData': ['all'],
    'FilesPerJob': 5,
}

for _, sd in DataRun:
    files = nanoGetSampleFiles(dataDirectory, 'MuonEG_' + sd)
    samples['DATA']['name'].extend(files)
