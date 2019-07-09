# Take efake/mctf plots and plot the transfer factors and weights

import os
import sys
import array
import math
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2(True)

thisdir = os.path.dirname(os.path.realpath(__file__))

egSourceName = '%s/rootFile/prompt_conversion_efficiency.root' % thisdir
hadronSourceName = '%s/rootFile/hadron_efficiency.root' % thisdir
outputName = '%s/rootFile/datatf.root' % thisdir

PLOTDIR = '%s/plots/datatf' % thisdir
try:
    os.makedirs(PLOTDIR)
except OSError:
    pass

from common import tnames, snames, ptbinning, etabinning

output = ROOT.TFile.Open(outputName, 'recreate')

nptbins = len(ptbinning) - 1
netabins = len(etabinning) - 1
nbins = nptbins * netabins

egSource = ROOT.TFile.Open(egSourceName)
hadronSource = ROOT.TFile.Open(hadronSourceName)

template = ROOT.TH1D('template', '', nbins, 0., float(nbins))
maptemplate = ROOT.TH2D('maptemplate', '', nptbins, array.array('d', ptbinning), netabins, array.array('d', etabinning))

effs = {}
tfs = {}
for source in snames:
    for tag in tnames:
        output.cd()

        if source in ['prompt', 'conversion']:
            if source == 'prompt':
                geff = egSource.Get('prompte_%s_dataeff' % tag)
            else:
                geff = egSource.Get('conversion_%s_dataeff' % tag)

            effs[(tag, source)] = template.Clone('eff_%s_%s' % (tag, source))
            for ibin in range(1, nbins + 1):
                effs[(tag, source)].SetBinContent(ibin, geff.GetY()[ibin - 1])
                effs[(tag, source)].SetBinError(ibin, geff.GetErrorY(ibin - 1))
        else:
            effs[(tag, source)] = hadronSource.Get('%s/efficiency_%s' % (source, tag)).Clone('eff_%s_%s' % (tag, source))

invweights = {}
weights = {}

output.cd()
for target in snames:
    for tag in tnames:
        invweights[(tag, target)] = template.Clone('%s_%s_invweight' % (tag, target))
        weights[(target, tag)] = template.Clone('%s_%s_weight' % (target, tag))

for ipt in range(nptbins):
    for ieta in range(netabins):
        ibin = ieta + ipt * netabins + 1

        mat = ROOT.TMatrixD(5, 5)
        for itag, tag in enumerate(tnames):
            for isource, source in enumerate(snames):
                invweights[(tag, source)].SetBinContent(ibin, effs[(tag, source)].GetBinContent(ibin) / effs[('ptag', source)].GetBinContent(ibin))
                mat[itag][isource] = effs[(tag, source)].GetBinContent(ibin)

        mat.Invert()

        for itarget, target in enumerate(snames):
            for itag, tag in enumerate(tnames):
                weights[(target, tag)].SetBinContent(ibin, mat[itarget][itag] * effs[('ptag', target)].GetBinContent(ibin))
                
                uncsq = 0.
                for iefftag, efftag in enumerate(tnames):
                    for ieffsource, effsource in enumerate(snames):
                        coeff = mat[itarget][iefftag] * mat[ieffsource][itag]
                        unc = coeff * effs[(efftag, effsource)].GetBinError(ibin)
                        uncsq += unc * unc

                weights[(target, tag)].SetBinError(ibin, math.sqrt(uncsq) * effs[('ptag', target)].GetBinContent(ibin))

weightmaps = {}
for itarget, target in enumerate(snames):
    for itag, tag in enumerate(tnames):
        weightmap = maptemplate.Clone('%s_%s_weightmap' % (target, tag))
        weightmaps[(target, tag)] = weightmap

        for ipt in range(nptbins):
            for ieta in range(netabins):
                ibin = ieta + ipt * netabins + 1
                weightmap.SetBinContent(ipt + 1, ieta + 1, weights[(target, tag)].GetBinContent(ibin))
                weightmap.SetBinError(ipt + 1, ieta + 1, weights[(target, tag)].GetBinError(ibin))

output.Write()

## print the tfs and weights
bigcanvas = ROOT.TCanvas('c2', 'c2', 900, 900)

zero = ROOT.TLine(0., 0., float(nbins), 0.)
zero.SetLineColor(ROOT.kBlack)
zero.SetLineWidth(1)

bigcanvas.Divide(5, 5)

bigcanvas.cd(0)
text = ROOT.TLatex(0., 0., '')
text.SetTextSize(0.02)
for isource, source in enumerate(snames):
    text.DrawLatexNDC(0.2 * (isource + 0.5), 0.95, source)
for itag, tag in enumerate(tnames):
    text.DrawLatexNDC(0., 1. - 0.2 * (itag + 0.5), tag)

ic = 1

for source in snames:
    for tag in tnames:
        eff = effs[(tag, source)]
        
        pad = bigcanvas.cd(ic)
        pad.SetGridy(True)
        eff.SetLineColor(ROOT.kBlack)
        eff.SetFillColor(ROOT.kBlack)
        eff.SetFillStyle(3003)
        eff.GetXaxis().SetLabelSize(0.05)
        eff.GetYaxis().SetLabelSize(0.05)
        eff.SetMinimum(0.)
        eff.SetMaximum(1.)
        eff.Draw('HIST')
        zero.Draw()

        ic += 5
        if ic > 25:
            ic = (ic % 5) + 1

bigcanvas.Print(PLOTDIR + '/effmap.pdf')
bigcanvas.Print(PLOTDIR + '/effmap.png')

ic = 1

for source in snames:
    for tag in tnames:
        invweight = invweights[(tag, source)]
        
        pad = bigcanvas.cd(ic)
        pad.SetGridy(True)
        invweight.SetLineColor(ROOT.kBlack)
        invweight.SetFillColor(ROOT.kBlack)
        invweight.SetFillStyle(3003)
        invweight.GetXaxis().SetLabelSize(0.05)
        invweight.GetYaxis().SetLabelSize(0.05)
        invweight.SetMinimum(0.)
        invweight.SetMaximum(1.)
        invweight.Draw('HIST')
        zero.Draw()

        ic += 5
        if ic > 25:
            ic = (ic % 5) + 1

bigcanvas.Print(PLOTDIR + '/invweightmap.pdf')
bigcanvas.Print(PLOTDIR + '/invweightmap.png')

bigcanvas.Clear()

ROOT.gStyle.SetPalette(ROOT.kLightTemperature)

bigcanvas.Divide(5, 5)

bigcanvas.cd(0)
text = ROOT.TLatex(0., 0., '')
text.SetTextSize(0.02)
for isource, source in enumerate(snames):
    text.DrawLatexNDC(0., 1. - 0.2 * (isource + 0.5), source)
for itag, tag in enumerate(tnames):
    text.DrawLatexNDC(0.2 * (itag + 0.5), 0.95, tag)

ic = 1

for source in snames:
    for tag in tnames:
        weight = weights[(source, tag)]

        pad = bigcanvas.cd(ic)
        pad.SetGridy(True)
        weight.SetLineColor(ROOT.kBlack)
        weight.SetFillColor(ROOT.kBlack)
        weight.SetFillStyle(3003)
        weight.GetXaxis().SetLabelSize(0.05)
        weight.GetYaxis().SetLabelSize(0.05)
        weight.SetMinimum(-3.)
        weight.SetMaximum(3.)
        weight.Draw('HIST')
        zero.Draw()

        ic += 1

bigcanvas.Print(PLOTDIR + '/weightmap.pdf')
bigcanvas.Print(PLOTDIR + '/weightmap.png')

bigcanvas.Clear()

bigcanvas.Divide(5, 5)

bigcanvas.cd(0)
text = ROOT.TLatex(0., 0., '')
text.SetTextSize(0.02)
for itag, tag in enumerate(tnames):
    text.DrawLatexNDC(0.2 * (itag + 0.5), 0.95, tag)

ic = 1

for tag in tnames:
    weight = None

    for source in snames:
        if source == 'prompt':
            continue
        if weight is None:
            weight = weights[(source, tag)]
        else:
            weight.Add(weights[(source, tag)])

    pad = bigcanvas.cd(ic)
    pad.SetGridy(True)
    weight.SetLineColor(ROOT.kBlack)
    weight.SetFillColor(ROOT.kBlack)
    weight.SetFillStyle(3003)
    weight.GetXaxis().SetLabelSize(0.05)
    weight.GetYaxis().SetLabelSize(0.05)
    weight.SetMinimum(-5.)
    weight.SetMaximum(5.)
    weight.Draw('HIST')
    zero.Draw()

    ic += 1

bigcanvas.Print(PLOTDIR + '/weightsum.pdf')
bigcanvas.Print(PLOTDIR + '/weightsum.png')
