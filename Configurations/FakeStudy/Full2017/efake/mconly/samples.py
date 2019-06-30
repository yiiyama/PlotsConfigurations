import os
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

subsamples = {
    'prompt': 'Electron_prompt',
    'bhadron': '!Electron_prompt && !Electron_conversion && Electron_hadronFlavour == 5',
    'chadron': '!Electron_prompt && !Electron_conversion && Electron_hadronFlavour == 4',
    'light': '!Electron_prompt && !Electron_conversion && Electron_hadronFlavour == 0',
    'conversion': '!Electron_prompt && Electron_conversion'
}

ttsemi = nanoGetSampleFiles(mcDirectory, 'TTToSemiLeptonic')
ttfull = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu')

samples['top'] = {
    'name': ttsemi + ttfull,
    'weight': '1',
    'FilesPerJob': 5,
    'subsamples': subsamples
}

dy50 = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50')
dy50noext = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50-noext')
dy50loext = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50-LO-ext1')
dy10 = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO')
dy50lo = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50-LO')

samples['dy'] = {
    'name': dy50 + dy50noext + dy50loext + dy10 + dy50lo,
    'weight': '1',
    'FilesPerJob': 5,
    'subsamples': subsamples
}

wj = nanoGetSampleFiles(mcDirectory, 'WJetsToLNu-LO')
wjext = nanoGetSampleFiles(mcDirectory, 'WJetsToLNu-LO-ext1')
w0j = nanoGetSampleFiles(mcDirectory, 'WJetsToLNu-0J')
w1j = nanoGetSampleFiles(mcDirectory, 'WJetsToLNu-1J')
w1jext = nanoGetSampleFiles(mcDirectory, 'WJetsToLNu-1J-ext1')
w2j = nanoGetSampleFiles(mcDirectory, 'WJetsToLNu-2J')

samples['wj'] = {
    'name': wj + wjext + w0j + w1j + w1jext + w2j,
    'weight': '1',
    'FilesPerJob': 5,
    'subsamples': subsamples
}
