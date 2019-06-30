import os
import math
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

from common import tnames, ptbinning, etabinning

outputFileName = '/afs/cern.ch/work/y/yiiyama/hww/fakefinal/prompt_conversion_scalefactor.root'
PLOTDIR = '/afs/cern.ch/user/y/yiiyama/www/plots/hww/prompt_conversion_scalefactor'

try:
    os.makedirs(PLOTDIR)
except OSError:
    pass

outputFile = ROOT.TFile.Open(outputFileName, 'recreate')

zmassdir = os.path.dirname(os.path.realpath(__file__)) + '/zmass'

nptbins = len(ptbinning) - 1
netabins = len(etabinning) - 1

canvas = ROOT.TCanvas('c1', 'c1', 600, 600)
canvas.SetLeftMargin(0.15)
canvas.SetRightMargin(0.05)
canvas.SetBottomMargin(0.15)
canvas.SetTopMargin(0.05)
canvas.SetGridy(True)

legend = ROOT.TLegend(0.2, 0.7, 0.4, 0.9)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

one = ROOT.TLine(0., 1., 30., 1.)

graw = ROOT.TGraph(1)
graw.SetLineColor(ROOT.kBlack)
graw.SetLineWidth(2)
graw.SetMarkerColor(ROOT.kBlack)
graw.SetMarkerStyle(8)
legend.AddEntry(graw, 'raw', 'LP')

gmerged = ROOT.TGraph(1)
gmerged.SetLineColor(ROOT.kBlue + 2)
gmerged.SetLineWidth(2)
gmerged.SetMarkerColor(ROOT.kBlue)
gmerged.SetMarkerStyle(4)
legend.AddEntry(gmerged, 'pt-merged', 'LP')

gdata = ROOT.TGraph(1)
gdata.SetLineColor(ROOT.kRed + 2)
gdata.SetLineWidth(2)
gdata.SetMarkerColor(ROOT.kRed)
gdata.SetMarkerStyle(4)

gmc = ROOT.TGraph(1)
gmc.SetLineColor(ROOT.kGreen + 2)
gmc.SetLineWidth(2)
gmc.SetMarkerColor(ROOT.kGreen)
gmc.SetMarkerStyle(3)

def style(hist, temp):
    hist.SetTitle('')
    hist.GetXaxis().SetLabelSize(0.06)
    hist.GetYaxis().SetLabelSize(0.06)
    hist.SetLineColor(temp.GetLineColor())
    hist.SetLineWidth(temp.GetLineWidth())
    hist.SetMarkerColor(temp.GetMarkerColor())
    hist.SetMarkerStyle(temp.GetMarkerStyle())

## prompt

histFile = ROOT.TFile.Open(zmassdir + '/prompt/rootFile/plots_zmass_prompt.root')

hnormdata = histFile.Get('onZ/nZ/histo_DATA')
hnormmc = histFile.Get('onZ/nZ/histo_mc')

for tag in ['base'] + tnames:
    if tag == 'base':
        tagsuffix = '_trig'
    else:
        tagsuffix = '_' + tag
    
    htagdata = histFile.Get('onZ%s/nZ/histo_DATA' % tagsuffix)
    htagmc = histFile.Get('onZ%s/nZ/histo_mc' % tagsuffix)

    outputFile.cd()

    dataeff = htagdata.Clone('prompt_%s_dataeff' % tag)
    mceff = htagmc.Clone('prompt_%s_mceff' % tag)
    if tag == 'base':
        dataeff.Divide(hnormdata)
        mceff.Divide(hnormmc)
        database = htagdata
        mcbase = htagmc
    else:
        dataeff.Divide(database)
        mceff.Divide(mcbase)

    style(dataeff, gdata)
    style(mceff, gmc)
    dataeff.Draw('EP')
    mceff.Draw('EP SAME')
    dataeff.SetMinimum(0.)
    if tag in ['base', 'ptag']:
        dataeff.SetMaximum(1.)
    else:
        dataeff.SetMaximum(0.1)
    canvas.Print(os.path.join(PLOTDIR, 'eff_prompt_%s.pdf' % tag))
    canvas.Print(os.path.join(PLOTDIR, 'eff_prompt_%s.png' % tag))
    canvas.Clear()

    sf = dataeff.Clone('prompt_%s_datamcSF' % tag)
    sf.Divide(mceff)

    style(sf, graw)
    sf.Draw('EP')
    sf.SetMinimum(0.)
    sf.SetMaximum(1.2)
    one.Draw()
    canvas.Print(os.path.join(PLOTDIR, 'prompt_%s.pdf' % tag))
    canvas.Print(os.path.join(PLOTDIR, 'prompt_%s.png' % tag))
    canvas.Clear()

    sf.Write()
    dataeff.Write()
    mceff.Write()

histFile.Close()

## conversion

eHistFile = ROOT.TFile.Open(zmassdir + '/conversion/rootFile/plots_zmass_conversion.root')
gHistFile = ROOT.TFile.Open(zmassdir + '/photon/rootFile/plots_zmass_photon.root')

hnormdata = gHistFile.Get('onZ/nZ/histo_DATA')
hnormmc = gHistFile.Get('onZ/nZ/histo_mc')

for tag in ['base'] + tnames:
    if tag == 'base':
        tagsuffix = ''
    else:
        tagsuffix = '_' + tag

    htagdata = eHistFile.Get('onZ%s/nZ/histo_DATA' % tagsuffix)
    htagmc = eHistFile.Get('onZ%s/nZ/histo_mc' % tagsuffix)

    outputFile.cd()

    dataeff = htagdata.Clone('conversion_%s_dataeff' % tag)
    mceff = htagmc.Clone('conversion_%s_mceff' % tag)
    if tag == 'base':
        dataeff.Divide(hnormdata)
        mceff.Divide(hnormmc)
        database = htagdata
        mcbase = htagmc
    else:
        dataeff.Divide(database)
        mceff.Divide(mcbase)

    style(dataeff, gdata)
    style(mceff, gmc)
    dataeff.Draw('EP')
    mceff.Draw('EP SAME')
    dataeff.SetMinimum(0.)
    if tag in ['base', 'ptag', 'gtag']:
        dataeff.SetMaximum(1.)
    else:
        dataeff.SetMaximum(0.2)
    canvas.Print(os.path.join(PLOTDIR, 'eff_conversion_%s.pdf' % tag))
    canvas.Print(os.path.join(PLOTDIR, 'eff_conversion_%s.png' % tag))
    canvas.Clear()

    sf = htagdata.Clone('conversion_%s_datamcSF' % tag)
    sf.Divide(hnormdata)
    sf.Multiply(hnormmc)
    sf.Divide(htagmc)

    style(sf, graw)
    sf.Draw('EP')
    sf.SetMinimum(0.)
    sf.SetMaximum(2.)
    one.Draw()
    canvas.Print(os.path.join(PLOTDIR, 'conversion_%s.pdf' % tag))
    canvas.Print(os.path.join(PLOTDIR, 'conversion_%s.png' % tag))
    canvas.Clear()

#    if tag in ['ptag', 'btag', 'ctag', 'ltag']:
#        # stat too small for these tags - merge pt bins
#        sf.SetName('conversion_%s_datamcSFraw' % tag)
#        sf.Write()
#        sfraw = sf
#
#        dataeff.SetName('conversion_%s_dataeffraw' % tag)
#        dataeff.Write()
#        mceff.SetName('conversion_%s_mceffraw' % tag)
#        mceff.Write()
#
#        outputFile.cd()
#
#        dataeff = htagdata.Clone('conversion_%s_dataeff' % tag)
#        dataeff.Reset()
#        mceff = htagmc.Clone('conversion_%s_mceff' % tag)
#        mceff.Reset()
#
#        if False:
#            for ieta in range(netabins):
#                tagdataTotal = 0.
#                tagmcTotal = 0.
#                normdataTotal = 0.
#                normmcTotal = 0.
#        
#                for ipt in range(nptbins):
#                    ibin = 1 + ieta + ipt * netabins
#                    tagdataTotal += htagdata.GetBinContent(ibin)
#                    tagmcTotal += htagmc.GetBinContent(ibin)
#                    normdataTotal += hnormdata.GetBinContent(ibin)
#                    normmcTotal += hnormmc.GetBinContent(ibin)
#    
#                cont = (tagdataTotal / normdataTotal) / (tagmcTotal / normmcTotal)
#                err = cont * math.sqrt(1. / tagdataTotal + 1. / normdataTotal + 1. / tagmcTotal + 1. / normmcTotal)
#        
#                for ipt in range(nptbins):
#                    ibin = 1 + ieta + ipt * netabins
#                    sf.SetBinContent(ibin, cont)
#                    sf.SetBinError(ibin, err)
#
#            plotname = 'conversion_%s_ptmerged' % tag
#
#        else:
#            tagdataTotal = htagdata.GetSumOfWeights()
#            tagmcTotal = htagmc.GetSumOfWeights()
#            normdataTotal = database.GetSumOfWeights()
#            normmcTotal = mcbase.GetSumOfWeights()
#        
#            datacont = tagdataTotal / normdataTotal
#            dataerr = datacont * math.sqrt(1. / tagdataTotal + 1. / normdataTotal)
#            mccont = tagmcTotal / normmcTotal
#            mcerr = mccont * math.sqrt(1. / tagmcTotal + 1. / normmcTotal)
#    
#            for ieta in range(netabins):
#                for ipt in range(nptbins):
#                    ibin = 1 + ieta + ipt * netabins
#                    dataeff.SetBinContent(ibin, datacont)
#                    dataeff.SetBinError(ibin, dataerr)
#                    mceff.SetBinContent(ibin, mccont)
#                    mceff.SetBinError(ibin, mcerr)
#
#            plotname = 'conversion_%s_allmerged' % tag
#
#        sf = dataeff.Clone('conversion_%s_datamcSF' % tag)
#        sf.Divide(mceff)
#
#        style(sf, gmerged)
#        sfraw.Draw('EP')
#        sf.Draw('EP SAME')
#        sfraw.SetMinimum(0.)
#        sfraw.SetMaximum(2.)
#        one.Draw()
#        canvas.Print(os.path.join(PLOTDIR, '%s.pdf' % plotname))
#        canvas.Print(os.path.join(PLOTDIR, '%s.png' % plotname))
#        canvas.Clear()

    sf.Write()
    dataeff.Write()
    mceff.Write()
