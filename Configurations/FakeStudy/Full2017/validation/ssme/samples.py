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

samples['DATA'] = {
    'name': [],
    'weight': '1',
    'isData': ['all'],
    'FilesPerJob': 5,
}

for _, sd in DataRun:
    files = nanoGetSampleFiles(dataDirectory, 'MuonEG_' + sd)
    samples['DATA']['name'].extend(files)
