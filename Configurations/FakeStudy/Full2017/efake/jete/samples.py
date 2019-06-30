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
mcSteps = 'fakeSkimJetElectronMC'
dataSteps = 'fakeSkimJetElectronDATA'

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

dy10 = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO')
dy50 = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50')
wj = nanoGetSampleFiles(mcDirectory, 'WJetsToLNu-LO')

samples['prompt'] = {
    'name': dy10 + dy50 + wj,
    'weight': 'Electron_prompt && !Electron_tau',
    'weights': [],
    'FilesPerJob': 5
}
for _ in range(len(dy10)):
    samples['prompt']['weights'].append('0.4712626')
for _ in range(len(dy50)):
    samples['prompt']['weights'].append('genWeight*1.9109e-06')
for _ in range(len(wj)):
    samples['prompt']['weights'].append('1.8619779')

gj40 = nanoGetSampleFiles(mcDirectory, 'GJets_HT40To100-ext1') + nanoGetSampleFiles(mcDirectory, 'GJets_HT40To100')
gj100 = nanoGetSampleFiles(mcDirectory, 'GJetsDR04_HT100To200')
gj200 = nanoGetSampleFiles(mcDirectory, 'GJetsDR04_HT200To400')
gj400 = nanoGetSampleFiles(mcDirectory, 'GJetsDR04_HT400To600')
gj600 = nanoGetSampleFiles(mcDirectory, 'GJetsDR04_HT600ToInf')

samples['conversion'] = {
    'name': gj40 + gj100 + gj200 + gj400 + gj600,
    'weight': '!Electron_prompt && !Electron_tau && Electron_conversion',
    'weights': [],
    'FilesPerJob': 5
}

gj40weight = 18740. / (15965137 + 4754796)
for _ in range(len(gj40)):
    samples['conversion']['weights'].append(str(gj40weight))
for _ in range(len(gj100)):
    samples['conversion']['weights'].append('0.3371814')
for _ in range(len(gj200)):
    samples['conversion']['weights'].append('0.0235910')
for _ in range(len(gj400)):
    samples['conversion']['weights'].append('0.0099347')
for _ in range(len(gj600)):
    samples['conversion']['weights'].append('0.0052922')

samples['DATA'] = {
    'name': [],
    'weight': '1',
    'isData': ['all'],
    'FilesPerJob': 5,
}

for _, sd in DataRun:
    files = nanoGetSampleFiles(dataDirectory, 'SingleElectron_' + sd)
    samples['DATA']['name'].extend(files)

myconfig = ''
if myconfig == 'mc':
    samples.pop('DATA')
elif myconfig == 'data':
    for key in samples.keys():
        if key != 'DATA':
            samples.pop(key)

