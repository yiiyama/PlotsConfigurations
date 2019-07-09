import os
import sys
import math
import array
import ROOT
ROOT.gROOT.SetBatch(True)

from common import ptbinning, etabinning, snames, tnames
import plotstyle

try:
    tag, ipt, ieta = sys.argv[1:4]
except (IndexError, ValueError):
    ipts = range(len(ptbinning) - 1)
    ietas = range(len(etabinning) - 1)
else:
    tnames = [tag]
    ipts = [int(ipt)]
    ietas = [int(ieta)]

try:
    showPrefit = sys.argv[4]
except IndexError:
    showPrefit = False

thisdir = os.path.dirname(os.path.realpath(__file__))

mcFile = ROOT.TFile.Open('%s/efake/mconly/rootFile/plots_efake_mconly.root' % thisdir)
ssmeFile = ROOT.TFile.Open('%s/efake/ssme/rootFile/plots_efake_ssme.root' % thisdir)
jeteFile = ROOT.TFile.Open('%s/efake/jete/rootFile/plots_efake_jete.root' % thisdir)

plotstyle.WEBDIR = '%s/plots' % thisdir
plotdirbase = 'hadron_efficiency'

outputFileName = '%s/rootFile/hadron_efficiency.root' % thisdir

sfSource = ROOT.TFile.Open('%s/rootFile/prompt_conversion_efficiency.root' % thisdir)
promptSF = {}
conversionSF = {}
for tag in ['base'] + tnames:
    promptSF[tag] = sfSource.Get('prompte_%s_datamcSF' % tag)
    conversionSF[tag] = sfSource.Get('conversion_%s_datamcSF' % tag)

nptbins = len(ptbinning) - 1
netabins = len(etabinning) - 1

sources = ['bhadron', 'chadron', 'light']
vnames = ['r9', 'btag', 'csvv2']
pspaces = ['inclusive', 'bjets', 'nobjet']
pfiles = {'inclusive': ssmeFile, 'bjets': jeteFile, 'nobjet': jeteFile}

canvas = plotstyle.DataMCCanvas()
canvas.legend.setPosition(0.7, 0.7, 0.9, 0.9)
canvas.legend.ncolumns = 1
canvas.colorList = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
    '#bcbd22', '#17becf']

nbinss = {
    'r9': (6, 20),
    'btag': (1, len([0. + 0.05 * x for x in range(12)] + [0.6 + 0.02 * x for x in range(21)]) - 1),
    'csvv2': (1, len([0.] + [0.1 + 0.02 * x for x in range(46)]) - 1)
}
nbins = sum(end - start + 1 for start, end in nbinss.values())

def drawstack(hists, name, plotdir):
    obs = hists['obs'].Clone('obs')
    obs.Scale(1., 'width')
    canvas.addObs(obs)
    for key in ['prompt', 'bhadron', 'chadron', 'light', 'conversion']:
        h = hists[key].Clone(key)
        h.Scale(1., 'width')
        canvas.addStacked(h, title=key)
        h.Delete()

    canvas.ylimits = (0.5, obs.GetMaximum() * 2.)
    canvas.printWeb(plotdir, name + '_log', logy=True)
    canvas.ylimits = (0., obs.GetMaximum() * 1.2)
    canvas.printWeb(plotdir, name, logy=False)
    canvas.Clear(full=True)

    obs.Delete()

def fit(htarget, hhadrons, nbins, fitSources):
    total = htarget.GetSumOfWeights()
    
    x = ROOT.RooRealVar('x', 'x', 0., 0., float(nbins))
    x.setBins(nbins)
    xlist = ROOT.RooArgList(x)
    xset = ROOT.RooArgSet(x)
    
    target = ROOT.RooDataHist('target', 'target', xlist, htarget)
    hadrons = dict((source, ROOT.RooDataHist(source, source, xlist, hhadrons[source])) for source in fitSources)
    
    _pdfs = []
    _coeffs = {}
    pdfs = ROOT.RooArgList()
    coeffs = ROOT.RooArgList()
    for isource, source in enumerate(fitSources):
        pdf = ROOT.RooHistPdf('p' + source, source, xset, hadrons[source])
        _pdfs.append(pdf)
        pdfs.add(pdf)
        coeff = ROOT.RooRealVar('c' + source, source, 0.1 * total, 0., 2. * total)
        if source == 'conversion':
            c = coeff
            c.setVal(hhadrons[source].GetSumOfWeights())
            c.setConstant(True)
            sfunc = ROOT.RooRealVar('sfunc', 'sfunc', 0., -10., 10.)
            coeffScale = ROOT.RooExponential('coeffScale', 'coeffScale', sfunc, ROOT.RooFit.RooConst(1.))
            coeff = ROOT.RooProduct('scconversion', 'scconversion', ROOT.RooArgList(c, coeffScale))
            sfrelunc = conversionSF[tag].GetBinError(ikinbin) / conversionSF[tag].GetBinContent(ikinbin)
            constraint = ROOT.RooGaussian('constraint', 'constraint', sfunc, ROOT.RooFit.RooConst(0.), ROOT.RooFit.RooConst(sfrelunc))

        _coeffs[source] = coeff
        coeffs.add(coeff)
    
    model = ROOT.RooAddPdf('model', 'model', pdfs, coeffs)

    fitOptions = (ROOT.RooFit.SumW2Error(True),)
    if applyConversionSF:
        fitOptions += (ROOT.RooFit.ExternalConstraints(ROOT.RooArgSet(constraint)),)
    
    model.fitTo(target, *fitOptions)

    result = {}
    for source, c in _coeffs.iteritems():
        if source == 'conversion':
            result[source] = (c.getVal(), 0.) # no error for RooProduct
        else:
            result[source] = (c.getVal(), c.getError())

    return result


template = ROOT.TH1D('template', '', nbins, 0., float(nbins))
longtemplate = ROOT.TH1D('longtemplate', '', nbins * len(pspaces), 0., float(nbins * len(pspaces)))

counttemplate = ROOT.TH1D('counttemplate', '', nptbins * netabins, 0., float(nptbins * netabins))

outputFile = ROOT.TFile.Open(outputFileName, 'recreate')

counters = {}
efficiencies = {}
for source in sources:
    sdir = outputFile.mkdir(source)
    sdir.cd()
    for tag in ['base'] + tnames:
        for pspace in pspaces:
            counters[(source, tag, pspace)] = counttemplate.Clone('counts_%s_%s' % (tag, pspace))

    for tag in tnames:
        efficiencies[(source, tag)] = counttemplate.Clone('efficiency_%s' % tag)

for ipt in ipts:
    for ieta in ietas:
        kinbin = 'pt%d_eta%d' % (ipt, ieta)
        ikinbin = 1 + ieta + ipt * netabins

        kindir = outputFile.mkdir(kinbin)

        for tag in ['base'] + tnames:
            sourcehists = {}

            applyConversionSF = (tag in ['base', 'ptag', 'gtag'])

            for pspace in pspaces:
                dataFile = pfiles[pspace]
                if tag == 'base':
                    cut = '%s_%s' % (pspace, kinbin)
                    mccut = 'baseline_%s' % kinbin
                else:
                    cut = '%s_%s_%s' % (pspace, tag, kinbin)
                    mccut = '%s_%s' % (tag, kinbin)

                ROOT.gROOT.cd()

                for vname in vnames + ['counts']:
                    hists = sourcehists[(pspace, vname)] = {}
                    hists['obs'] = dataFile.Get('%s/%s/histo_DATA' % (cut, vname)).Clone('%s_%s_obs' % (pspace, vname))
                    hists['prompt'] = dataFile.Get('%s/%s/histo_prompt' % (cut, vname)).Clone('%s_%s_prompt' % (pspace, vname))
                    #if dataFile is ssmeFile:
                    if False:
                        bhadron_norm = dataFile.Get('%s/%s/histo_fake_bhadron' % (cut, vname)).GetSumOfWeights()
                        chadron_norm = dataFile.Get('%s/%s/histo_fake_chadron' % (cut, vname)).GetSumOfWeights()
                        light_norm = dataFile.Get('%s/%s/histo_fake_light' % (cut, vname)).GetSumOfWeights()
                    else:
                        bhadron_norm = hists['obs'].GetSumOfWeights() * 0.3
                        chadron_norm = hists['obs'].GetSumOfWeights() * 0.3
                        light_norm = hists['obs'].GetSumOfWeights() * 0.3
    
                    conversion_norm = dataFile.Get('%s/%s/histo_conversion' % (cut, vname)).GetSumOfWeights()
    
                    hists['bhadron'] = mcFile.Get('%s/%s/histo_top_bhadron' % (mccut, vname)).Clone('%s_%s_bhadron' % (pspace, vname))
                    hists['chadron'] = mcFile.Get('%s/%s/histo_wj_chadron' % (mccut, vname)).Clone('%s_%s_chadron' % (pspace, vname))
                    hists['chadron'].Add(mcFile.Get('%s/%s/histo_dy_chadron' % (mccut, vname)))
                    hists['light'] = mcFile.Get('%s/%s/histo_wj_light' % (mccut, vname)).Clone('%s_%s_light' % (pspace, vname))
                    hists['light'].Add(mcFile.Get('%s/%s/histo_dy_light' % (mccut, vname)))
                    hists['conversion'] = mcFile.Get('%s/%s/histo_wj_conversion' % (mccut, vname)).Clone('%s_%s_conversion' % (pspace, vname))
                    hists['conversion'].Add(mcFile.Get('%s/%s/histo_dy_conversion' % (mccut, vname)))

                    hists['bhadron'].Scale(bhadron_norm / hists['bhadron'].GetSumOfWeights())
                    hists['chadron'].Scale(chadron_norm / hists['chadron'].GetSumOfWeights())
                    hists['light'].Scale(light_norm / hists['light'].GetSumOfWeights())
                    hists['conversion'].Scale(conversion_norm / hists['conversion'].GetSumOfWeights())

                    hists['prompt'].Scale(promptSF[tag].GetBinContent(ikinbin))
                    if applyConversionSF:
                        hists['conversion'].Scale(conversionSF[tag].GetBinContent(ikinbin))
    
                    for source in sources:
                        hist = hists[source]
                        for iX in range(1, hist.GetNbinsX() + 1):
                            if hist.GetBinContent(iX) <= 0.:
                                hist.SetBinContent(iX, 1.e-5)

                    if showPrefit:
                        drawstack(hists, '%s_%s' % (vname, kinbin), '%s/prefit/%s/%s' % (plotdirbase, tag, pspace))

            kindir.cd()

            if applyConversionSF:
                fitSources = sources + ['conversion']
            else:
                fitSources = sources
                                
            if tag == 'base':
                # three separate fits

                for pspace in pspaces:
                    htarget = template.Clone('target')
                    hhadrons = dict((source, template.Clone(source)) for source in fitSources)

                    ibin = 1

                    for vname in vnames:
                        hists = sourcehists[(pspace, vname)]
                                                                           
                        start, end = nbinss[vname]
                        for iX in range(start, end + 1):
                            cont = hists['obs'].GetBinContent(iX)
                            cont -= hists['prompt'].GetBinContent(iX)
                            
                            err2 = math.pow(hists['obs'].GetBinError(iX), 2.) * 4. # to account for using 4 templates from the same set of events
                            err2 += math.pow(hists['prompt'].GetBinError(iX), 2.)
        
                            if not applyConversionSF:
                                cont -= hists['conversion'].GetBinContent(iX)
                                err2 += math.pow(hists['conversion'].GetBinError(iX), 2.)
            
                            htarget.SetBinContent(ibin, cont)
                            htarget.SetBinError(ibin, math.sqrt(err2))
        
                            for source in fitSources:
                                hhadrons[source].SetBinContent(ibin, hists[source].GetBinContent(iX))
                                hhadrons[source].SetBinError(ibin, hists[source].GetBinError(iX))

                            ibin += 1

                    coeffs = fit(htarget, hhadrons, nbins, fitSources)

                    scales = {}
                    for source in fitSources:
                        scales[source] = coeffs[source][0] / hhadrons[source].GetSumOfWeights()

                    for vname in vnames + ['counts']:
                        hists = sourcehists[(pspace, vname)]
                        for source in fitSources:
                            hists[source].Scale(scales[source])
        
                        drawstack(hists, '%s_%s' % (vname, kinbin), '%s/%s/%s' % (plotdirbase, tag, pspace))
                        
                        if vname == 'counts':
                            for source in sources:
                                counter = counters[(source, tag, pspace)]
                                counter.SetBinContent(ikinbin, hists[source].GetBinContent(1))
                                counter.SetBinError(ikinbin, hists[source].GetBinError(1))

            else:
                # simultaneous fit
                htarget = longtemplate.Clone('target')
                hhadrons = dict((source, longtemplate.Clone(source)) for source in fitSources)

                scales = {}

                ibin = 1
                for pspace in pspaces:
                    for source in sources:
                        scales[(pspace, source)] = counters[(source, 'base', pspace)].GetBinContent(ikinbin) / sourcehists[(pspace, 'counts')][source].GetBinContent(1)
                    if applyConversionSF:
                        scales[(pspace, 'conversion')] = 1.

                    for vname in vnames:
                        hists = sourcehists[(pspace, vname)]
                                                                           
                        start, end = nbinss[vname]
                        for iX in range(start, end + 1):
                            cont = hists['obs'].GetBinContent(iX)
                            cont -= hists['prompt'].GetBinContent(iX)
                            
                            err2 = math.pow(hists['obs'].GetBinError(iX), 2.) * 4. # to account for using 4 templates from the same set of events
                            err2 += math.pow(hists['prompt'].GetBinError(iX), 2.)
        
                            if not applyConversionSF:
                                cont -= hists['conversion'].GetBinContent(iX)
                                err2 += math.pow(hists['conversion'].GetBinError(iX), 2.)
            
                            htarget.SetBinContent(ibin, cont)
                            htarget.SetBinError(ibin, math.sqrt(err2))

                            for source in fitSources:
                                hhadrons[source].SetBinContent(ibin, hists[source].GetBinContent(iX) * scales[(pspace, source)])
                                hhadrons[source].SetBinError(ibin, hists[source].GetBinError(iX) * scales[(pspace, source)])
                                
                            ibin += 1

                coeffs = fit(htarget, hhadrons, nbins * len(pspaces), fitSources)
                            
                kindir.cd()
                eff = {}
                for source in fitSources:
                    eff[source] = (coeffs[source][0] / hhadrons[source].GetSumOfWeights(), coeffs[source][1] / hhadrons[source].GetSumOfWeights())
                    print 'ipt', ipt, 'ieta', ieta, source, tag, eff[source]

                    if source != 'conversion':
                        efficiencies[(source, tag)].SetBinContent(ikinbin, eff[source][0])
                        efficiencies[(source, tag)].SetBinError(ikinbin, eff[source][1])

                for pspace in pspaces:
                    for vname in vnames + ['counts']:
                        hists = sourcehists[(pspace, vname)]
                        for source in fitSources:
                            hists[source].Scale(scales[(pspace, source)] * eff[source][0])
        
                        drawstack(hists, '%s_%s' % (vname, kinbin), '%s/%s/%s' % (plotdirbase, tag, pspace))
                        
                        if vname == 'counts':
                            for source in sources:
                                counter = counters[(source, tag, pspace)]
                                counter.SetBinContent(ikinbin, hists[source].GetBinContent(1))
                                counter.SetBinError(ikinbin, hists[source].GetBinError(1))

            for hists in sourcehists.itervalues():
                for hist in hists.itervalues():
                    hist.Delete()
    
for source in sources:
    outputFile.cd(source)
    for tag in ['base'] + tnames:
        for pspace in pspaces:
            counters[(source, tag, pspace)].Write()
        
    for tag in tnames:
        efficiencies[(source, tag)].Write()

scanvas = plotstyle.SimpleCanvas()

for source in sources:
    for tag in ['base'] + tnames:
        for pspace in pspaces:
            counter = counters[(source, tag, pspace)]
            counter.SetLineWidth(2)
            counter.SetLineColor(ROOT.kBlack)
            scanvas.addHistogram(counter, drawOpt='HIST E')
            scanvas.ylimits = (0., -1.)
            scanvas.printWeb('%s/counts' % plotdirbase, '%s_%s_%s' % (source, tag, pspace), logy=False)
            scanvas.Clear()

    for tag in tnames:
        efficiency = efficiencies[(source, tag)]
        efficiency.SetLineWidth(2)
        efficiency.SetLineColor(ROOT.kBlack)
        scanvas.addHistogram(efficiency, drawOpt='EP')
        scanvas.ylimits = (0., 1.3)
        scanvas.addLine(0., 1., efficiency.GetXaxis().GetXmax(), 1.)
        scanvas.printWeb('%s/efficiencies' % plotdirbase, '%s_%s' % (source, tag), logy=False)
        scanvas.Clear()
