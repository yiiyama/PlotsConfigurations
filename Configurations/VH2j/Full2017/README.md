VH2j plots
==============

Common tools for analysis:

voms-proxy-init -voms cms -rfc --valid 168:0

cmsenv

mkShapesMulti.py --pycfg=configuration.py  --inputDir=/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/ --doBatch=True --batchQueue=workday --treeName=Events --batchSplit=Samples,Files

mkShapesMulti.py --doHadd=1 --batchSplit=Samples,Files --doNotCleanup --nThreads=8


mkPlot.py        --pycfg=configuration.py  --inputFile=rootFile/plots_WW.root --minLogC=0.01 --minLogCratio=0.01 --maxLogC=1000 --maxLogCratio=1000  --showIntegralLegend=1 
