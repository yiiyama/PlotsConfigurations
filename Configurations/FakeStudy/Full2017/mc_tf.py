# Take efake/mctf plots and plot the transfer factors and weights

import os
import sys
import array
import math
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2(True)

sfSourceName = '/afs/cern.ch/work/y/yiiyama/hww/fakefinal/prompt_conversion_scalefactor.root'
outputName = '/afs/cern.ch/work/y/yiiyama/hww/fakefinal/mctf.root'

PLOTDIR = '/afs/cern.ch/user/y/yiiyama/www/plots/hww/mc_tf'
try:
    os.makedirs(PLOTDIR)
except OSError:
    pass

from common import tnames, snames, ptbinning, etabinning

output = ROOT.TFile.Open(outputName, 'recreate')

nptbins = len(ptbinning) - 1
netabins = len(etabinning) - 1
nbins = nptbins * netabins

sfSource = ROOT.TFile.Open(sfSourceName)

sfs = {}
for source in ['prompt', 'conversion']:
    for tag in tnames:
        sfs[(tag, source)] = sfSource.Get('%s_%s_datamcSF' % (source, tag))

maptemplate = ROOT.TH1D('maptemplate', '', nbins, 0., float(nbins))

countsSource = ROOT.TFile.Open(os.path.dirname(os.path.realpath(__file__)) + '/efake/mctf_scores/rootFile/plots_efake_mctf_scores.root')

rawtfs = {}
tfs = {}
for source in snames:
    if source == 'bhadron':
        samples = ['top']
    else:
        samples = ['dy', 'wj']
        
    for tag in tnames:
        output.cd()
        rawtfs[(tag, source)] = maptemplate.Clone('rawtf_%s_%s' % (tag, source))
        if source in ['prompt', 'conversion']:
            tfs[(tag, source)] = rawtfs[(tag, source)].Clone('tf_%s_%s' % (tag, source))
        else:
            tfs[(tag, source)] = rawtfs[(tag, source)]

        for ipt in range(nptbins):
            for ieta in range(netabins):
                ibin = 1 + ieta + ipt * netabins
                kinbin = 'pt%s_eta%s' % (ipt, ieta)

                numer = 0.
                denom = 0.
                for sample in samples:
                    numer += countsSource.Get('%s_%s/counts/histo_%s_%s' % (tag, kinbin, sample, source)).GetBinContent(1)
                    denom += countsSource.Get('baseline_%s/counts/histo_%s_%s' % (kinbin, sample, source)).GetBinContent(1)

                tf = numer / denom
                err = tf * math.sqrt(1. / numer + 1. / denom) # not accurate but OK
                rawtfs[(tag, source)].SetBinContent(ibin, tf)
                rawtfs[(tag, source)].SetBinError(ibin, err)
                if source in ['prompt', 'conversion']:
                    tfs[(tag, source)].SetBinContent(ibin, tf * sfs[(tag, source)].GetBinContent(ibin))
                    tfs[(tag, source)].SetBinError(ibin, err * sfs[(tag, source)].GetBinContent(ibin))

rawinvweights = {}
invweights = {}
rawweights = {}
rawweightUncs = {}
weights = {}
weightUncs = {}

output.cd()
for target in snames:
    for tag in tnames:
        rawinvweights[(tag, target)] = maptemplate.Clone('%s_%s_rawinvweight' % (tag, target))
        invweights[(tag, target)] = maptemplate.Clone('%s_%s_invweight' % (tag, target))
        rawweights[(target, tag)] = maptemplate.Clone('%s_%s_rawweight' % (target, tag))
        weights[(target, tag)] = maptemplate.Clone('%s_%s_weight' % (target, tag))

        rawweightUncs[(target, tag)] = {}
        weightUncs[(target, tag)] = {}
        for efftag in tnames:
            for effsource in snames:
                rawweightUncs[(target, tag)][(efftag, effsource)] = maptemplate.Clone('%s_%s_%s_%s_rawweightUnc' % (tag, target, efftag, effsource))
                weightUncs[(target, tag)][(efftag, effsource)] = maptemplate.Clone('%s_%s_%s_%s_weightUnc' % (tag, target, efftag, effsource))

for ipt in range(nptbins):
    for ieta in range(netabins):
        ibin = ieta + ipt * netabins + 1

        mat = ROOT.TMatrixD(5, 5)
        for itag, tag in enumerate(tnames):
            for isource, source in enumerate(snames):
                rawinvweights[(tag, source)].SetBinContent(ibin, rawtfs[(tag, source)].GetBinContent(ibin) / rawtfs[('ptag', source)].GetBinContent(ibin))
                mat[itag][isource] = rawtfs[(tag, source)].GetBinContent(ibin)

        mat.Invert()

        for itarget, target in enumerate(snames):
            for itag, tag in enumerate(tnames):
                rawweights[(target, tag)].SetBinContent(ibin, mat[itarget][itag] * rawtfs[('ptag', target)].GetBinContent(ibin))
                
                uncsq = 0.
                for iefftag, efftag in enumerate(tnames):
                    for ieffsource, effsource in enumerate(snames):
                        coeff = mat[itarget][iefftag] * mat[ieffsource][itag]
                        unc = coeff * rawtfs[(efftag, effsource)].GetBinError(ibin)
                        rawweightUncs[(target, tag)][(efftag, effsource)].SetBinContent(ibin, unc)
                        uncsq += unc * unc

                rawweights[(target, tag)].SetBinError(ibin, math.sqrt(uncsq) * rawtfs[('ptag', target)].GetBinContent(ibin))
        
        mat = ROOT.TMatrixD(5, 5)
        for itag, tag in enumerate(tnames):
            for isource, source in enumerate(snames):
                invweights[(tag, source)].SetBinContent(ibin, tfs[(tag, source)].GetBinContent(ibin) / tfs[('ptag', source)].GetBinContent(ibin))
                mat[itag][isource] = tfs[(tag, source)].GetBinContent(ibin)

        mat.Invert()

        for itarget, target in enumerate(snames):
            for itag, tag in enumerate(tnames):
                weights[(target, tag)].SetBinContent(ibin, mat[itarget][itag] * tfs[('ptag', target)].GetBinContent(ibin))
                
                uncsq = 0.
                for iefftag, efftag in enumerate(tnames):
                    for ieffsource, effsource in enumerate(snames):
                        coeff = mat[itarget][iefftag] * mat[ieffsource][itag]
                        unc = coeff * tfs[(efftag, effsource)].GetBinError(ibin)
                        weightUncs[(target, tag)][(efftag, effsource)].SetBinContent(ibin, unc)
                        uncsq += unc * unc

                weights[(target, tag)].SetBinError(ibin, math.sqrt(uncsq) * tfs[('ptag', target)].GetBinContent(ibin))

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
        rawtf = rawtfs[(tag, source)]
        
        pad = bigcanvas.cd(ic)
        pad.SetGridy(True)
        rawtf.SetLineColor(ROOT.kBlack)
        rawtf.SetFillColor(ROOT.kBlack)
        rawtf.SetFillStyle(3003)
        rawtf.GetXaxis().SetLabelSize(0.05)
        rawtf.GetYaxis().SetLabelSize(0.05)
        rawtf.SetMinimum(0.)
        rawtf.SetMaximum(1.)
        rawtf.Draw('HIST E')
        zero.Draw()

        ic += 5
        if ic > 25:
            ic = (ic % 5) + 1

bigcanvas.Print(PLOTDIR + '/rawtfmap.pdf')
bigcanvas.Print(PLOTDIR + '/rawtfmap.png')

ic = 1

for source in snames:
    for tag in tnames:
        tf = tfs[(tag, source)]
        
        pad = bigcanvas.cd(ic)
        pad.SetGridy(True)
        tf.SetLineColor(ROOT.kBlack)
        tf.SetFillColor(ROOT.kBlack)
        tf.SetFillStyle(3003)
        tf.GetXaxis().SetLabelSize(0.05)
        tf.GetYaxis().SetLabelSize(0.05)
        tf.SetMinimum(0.)
        tf.SetMaximum(1.)
        tf.Draw('HIST E')
        zero.Draw()

        ic += 5
        if ic > 25:
            ic = (ic % 5) + 1

bigcanvas.Print(PLOTDIR + '/tfmap.pdf')
bigcanvas.Print(PLOTDIR + '/tfmap.png')

ic = 1

for source in snames:
    for tag in tnames:
        rawinvweight = rawinvweights[(tag, source)]
        
        pad = bigcanvas.cd(ic)
        pad.SetGridy(True)
        rawinvweight.SetLineColor(ROOT.kBlack)
        rawinvweight.SetFillColor(ROOT.kBlack)
        rawinvweight.SetFillStyle(3003)
        rawinvweight.GetXaxis().SetLabelSize(0.05)
        rawinvweight.GetYaxis().SetLabelSize(0.05)
        rawinvweight.SetMinimum(0.)
        rawinvweight.SetMaximum(1.)
        rawinvweight.Draw('HIST E')
        zero.Draw()

        ic += 5
        if ic > 25:
            ic = (ic % 5) + 1

bigcanvas.Print(PLOTDIR + '/rawinvweightmap.pdf')
bigcanvas.Print(PLOTDIR + '/rawinvweightmap.png')

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
        invweight.Draw('HIST E')
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
        rawweight = rawweights[(source, tag)]

        pad = bigcanvas.cd(ic)
        pad.SetGridy(True)
        rawweight.SetLineColor(ROOT.kBlack)
        rawweight.SetFillColor(ROOT.kBlack)
        rawweight.SetFillStyle(3003)
        rawweight.GetXaxis().SetLabelSize(0.05)
        rawweight.GetYaxis().SetLabelSize(0.05)
        rawweight.SetMinimum(-3.)
        rawweight.SetMaximum(3.)
        rawweight.Draw('HIST E')
        zero.Draw()

        ic += 1

bigcanvas.Print(PLOTDIR + '/rawweightmap.pdf')
bigcanvas.Print(PLOTDIR + '/rawweightmap.png')

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
        weight.Draw('HIST E')
        zero.Draw()

        ic += 1

bigcanvas.Print(PLOTDIR + '/weightmap.pdf')
bigcanvas.Print(PLOTDIR + '/weightmap.png')
