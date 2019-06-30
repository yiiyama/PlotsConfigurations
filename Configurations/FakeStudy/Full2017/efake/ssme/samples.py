import os
import re
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

zz = nanoGetSampleFiles(mcDirectory, 'ZZTo4L')
wz = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin01')

samples['prompt'] = {
    'name': zz + wz,
    'weight': 'XSWeight * (Electron_prompt && !Electron_tau) * skimWeight_SSME',
    'FilesPerJob': 5
}

dy10 = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO')
dy50 = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50')
wg = nanoGetSampleFiles(mcDirectory, 'Wg_MADGRAPHMLM')

samples['conversion'] = {
    'name': dy10 + dy50 + wg,
    'weight': 'XSWeight * (!Electron_prompt && !Electron_tau && Electron_conversion) * skimWeight_SSME',
    'FilesPerJob': 5
}

ttsemi = nanoGetSampleFiles(mcDirectory, 'TTToSemiLeptonic')
wj = nanoGetSampleFiles(mcDirectory, 'WJetsToLNu-LO')

samples['fake'] = {
    'name': ttsemi + wj,
    'weight': 'XSWeight * (!Electron_prompt && !Electron_tau && !Electron_conversion) * skimWeight_SSME',
    'FilesPerJob': 5,
}
samples['fake']['subsamples'] = {
    'bhadron': 'Electron_hadronFlavour == 5',
    'chadron': 'Electron_hadronFlavour == 4',
    'light': 'Electron_hadronFlavour == 0'
}

samples['DATA'] = {
    'name': [],
    'weight': '1',
    'isData': ['all'],
    'FilesPerJob': 5,
}

for _, sd in DataRun:
    files = nanoGetSampleFiles(dataDirectory, 'MuonEG_' + sd)
    samples['DATA']['name'].extend(files)

myconfig = ''
if myconfig == 'mc':
    samples.pop('DATA')
elif myconfig == 'data':
    for key in samples.keys():
        if key != 'DATA':
            samples.pop(key)
