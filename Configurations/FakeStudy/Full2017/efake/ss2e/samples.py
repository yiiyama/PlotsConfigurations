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
  treeBaseDir = '/eos/cms/store/user/yiiyama/HWWNano/'

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
    from common import tnames, tagCuts
except ImportError:
    confdir = os.getenv('CMSSW_BASE') + '/src/PlotsConfigurations/Configurations/FakeStudy/Full2017'
    sys.path.append(confdir)
    from common import tnames, tagCuts

mcweight = 'skimWeight_SS2E'
mcweight += '*(Electron_prompt[leadE_SS2E] && !Electron_tau[leadE_SS2E])'
mcweight += '*(Electron_prompt[trailE_SS2E] && !Electron_tau[trailE_SS2E])'
mcweight += '*(%s)' % re.sub('(Electron_[0-9a-zA-Z_]+)', r'\1[leadE_SS2E]', ' && '.join(tagCuts['ptag']))
mcweight += '*(%s)' % re.sub('(Electron_[0-9a-zA-Z_]+)', r'\1[trailE_SS2E]', ' && '.join(tagCuts['ptag']))

wz = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin01')
zz = nanoGetSampleFiles(mcDirectory, 'ZZTo4L')

samples['prompt'] = {
    'name': wz + zz,
    'weight': mcweight,
    'FilesPerJob': 5,
    'weights': []
}
for _ in range(len(wz)):
    samples['prompt']['weights'].append('0.0001033319235*genWeight')
for _ in range(len(zz)):
    samples['prompt']['weights'].append('0.0001312854128*genWeight')

dy10 = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO')
dy50 = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50')
tt = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu')

samples['qflip'] = {
    'name': dy10 + dy50 + tt,
    'weight': mcweight + '*0.8404',
    'FilesPerJob': 5,
    'weights': []
}
for _ in range(len(dy10)):
    samples['qflip']['weights'].append('0.4712626')
for _ in range(len(dy50)):
    samples['qflip']['weights'].append('genWeight*1.9109e-06')
for _ in range(len(tt)):
    samples['qflip']['weights'].append('genWeight*0.0001391372418')

#fakeFiles = \
#
#samples['fake'] = {
#    'name': fakeFiles,
#    'weight': 'XSWeight*skimWeight_2ME*(!Electron_prompt && !Electron_tau)',
#    'FilesPerJob': 5
#}
#
#samples['fake']['subsamples'] = {
#    'bhadron': '!Electron_conversion && (Jet_hadronFlavour[{jetIdx}] == 5 || Electron_bhadron)'.format(jetIdx=jetIdx),
#    'chadron': '!Electron_conversion && (Jet_hadronFlavour[{jetIdx}] == 4 || (!Electron_bhadron && Electron_chadron))'.format(jetIdx=jetIdx),
#    'light': '!Electron_conversion && (Jet_hadronFlavour[{jetIdx}] < 4 && !Electron_bhadron && !Electron_chadron)'.format(jetIdx=jetIdx),
#    'conversion': 'Electron_conversion'
#}

samples['DATA'] = {
    'name': [],
    'weight': '1',
    'isData': ['all'],
    'FilesPerJob': 5,
}

for _, sd in DataRun:
    files = nanoGetSampleFiles(dataDirectory, 'DoubleEG_' + sd)
    samples['DATA']['name'].extend(files)

samples['DATA']['subsamples'] = {}
for leadTag in tnames:
    leadTagCut = re.sub('(Electron_[0-9a-zA-Z_]+)', r'\1[leadE_SS2E]', ' && '.join(tagCuts[leadTag]))
    for trailTag in tnames:
        trailTagCut = re.sub('(Electron_[0-9a-zA-Z_]+)', r'\1[trailE_SS2E]', ' && '.join(tagCuts[trailTag]))
        samples['DATA']['subsamples'][leadTag + trailTag] = ' && '.join([leadTagCut, trailTagCut])
