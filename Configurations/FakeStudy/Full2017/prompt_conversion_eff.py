import os
import math
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

from common import tnames, ptbinning, etabinning

thisdir = os.path.dirname(os.path.realpath(__file__))

outputFileName = '%s/rootFile/prompt_conversion_efficiency.root' % thisdir
PLOTDIR = '%s/plots/prompt_conversion_efficiency' % thisdir

try:
    os.makedirs(thisdir + '/rootFile')
except OSError:
    pass

try:
    os.makedirs(PLOTDIR)
except OSError:
    pass

outputFile = ROOT.TFile.Open(outputFileName, 'recreate')

zmassdir = '%s/zmass' % thisdir

nptbins = len(ptbinning) - 1
netabins = len(etabinning) - 1
nbins = nptbins * netabins

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

def makesf(name, dataeff, mceff, template):
    sf = template.Clone(name)
    sf.Reset()
    for iX in range(1, sf.GetNbinsX() + 1):
        data = dataeff.GetY()[iX - 1]
        mc = mceff.GetY()[iX - 1]
        if data != 0.:
            datarelerr2 = math.pow(dataeff.GetErrorY(iX - 1) / data, 2.)
        else:
            datarelerr2 = 0.
        if mc != 0.:
            mcrelerr2 = math.pow(mceff.GetErrorY(iX - 1) / mc, 2.)
            sf.SetBinContent(iX, data / mc)
            sf.SetBinError(iX, data / mc * math.sqrt(datarelerr2 + mcrelerr2))
        else:
            sf.SetBinContent(iX, 0.)
            sf.SetBinError(iX, 0.)

    return sf

def compute(name, histFile, basecut, hnormdata, hnormmc, ganging={}):
    for tag in ['base'] + tnames:
        if tag == 'base':
            cut = basecut
        else:
            cut = 'onZ_' + tag
    
        htagdata = histFile.Get('%s/nZ/histo_DATA' % cut)
        htagmc = histFile.Get('%s/nZ/histo_mc' % cut)

        outputFile.cd()
        if tag == 'base':
            heffbasedata = htagdata.Clone('%s_total_data' % name)
            heffbasemc = htagmc.Clone('%s_total_mc' % name)
            heffbasedata.Write()
            heffbasemc.Write()
   
        datapass = htagdata.Clone('%s_%s_data' % (name, tag))
        mcpass = htagmc.Clone('%s_%s_mc' % (name, tag))
    
        if tag == 'base':
            datanorm = hnormdata
            mcnorm = hnormmc
        else:
            datanorm = heffbasedata
            mcnorm = heffbasemc
            
        dataeff = ROOT.TGraphAsymmErrors(datapass, datanorm)
        mceff = ROOT.TGraphAsymmErrors(mcpass, mcnorm)

        ymax = max([dataeff.GetY()[ip] for ip in range(dataeff.GetN())] + [mceff.GetY()[ip] for ip in range(mceff.GetN())])
        ymax = math.ceil(ymax * 10.) * 0.1
    
        style(dataeff, gdata)
        style(mceff, gmc)
        dataeff.Draw('APE')
        mceff.Draw('PE')
        dataeff.SetMinimum(0.)
        dataeff.SetMaximum(ymax)
        dataeff.GetXaxis().SetLimits(0., nbins)
        canvas.Print(os.path.join(PLOTDIR, 'eff_%s_%s.pdf' % (name, tag)))
        canvas.Print(os.path.join(PLOTDIR, 'eff_%s_%s.png' % (name, tag)))
        canvas.Clear()
    
        sf = makesf('%s_%s_datamcSF' % (name, tag), dataeff, mceff, datapass)
    
        style(sf, graw)
        sf.Draw('EP')
        sf.SetMinimum(0.)
        sf.SetMaximum(2.)
        one.Draw()
        canvas.Print(os.path.join(PLOTDIR, 'sf_%s_%s.pdf' % (name, tag)))
        canvas.Print(os.path.join(PLOTDIR, 'sf_%s_%s.png' % (name, tag)))
        canvas.Clear()

        if tag in ganging:
            sf.SetName('%s_%s_datamcSFraw' % (name, tag))
            sf.Write()
            sfraw = sf

            datapass.SetName('%s_%s_dataraw' % (name, tag))
            datapass.Write()
            datapassraw = datapass
            mcpass.SetName('%s_%s_mcraw' % (name, tag))
            mcpass.Write()
            mcpassraw = mcpass

            dataeff.Write('%s_%s_dataeffraw' % (name, tag))
            dataeffraw = dataeff
            mceff.Write('%s_%s_mceffraw' % (name, tag))
            mceffraw = mceff
    
            outputFile.cd()
    
            datapass = htagdata.Clone('%s_%s_data' % (name, tag))
            mcpass = htagmc.Clone('%s_%s_mc' % (name, tag))

            datanorm = datanorm.Clone('datanorm')
            mcnorm = mcnorm.Clone('mcnorm')

            for hist in [datapass, mcpass, datanorm, mcnorm]:
                for bingroup in ganging[tag]:
                    c = 0.
                    e2 = 0.
                    for ibin in bingroup:
                        c += hist.GetBinContent(ibin)
                        e2 += math.pow(hist.GetBinError(ibin), 2.)
    
                    for ibin in bingroup:
                        hist.SetBinContent(ibin, c)
                        hist.SetBinError(ibin, math.sqrt(e2))

            dataeff = ROOT.TGraphAsymmErrors(datapass, datanorm)
            mceff = ROOT.TGraphAsymmErrors(mcpass, mcnorm)

            datanorm.Delete()
            mcnorm.Delete()

            sf = makesf('%s_%s_datamcSF' % (name, tag), dataeff, mceff, datapass)
    
            style(sf, gmerged)
            sfraw.Draw('EP')
            sf.Draw('EP SAME')
            sfraw.SetMinimum(0.)
            sfraw.SetMaximum(2.)
            one.Draw()
            canvas.Print(os.path.join(PLOTDIR, 'sfmerged_%s_%s.pdf' % (name, tag)))
            canvas.Print(os.path.join(PLOTDIR, 'sfmerged_%s_%s.png' % (name, tag)))
            canvas.Clear()
    
        sf.Write()
        datapass.Write()
        mcpass.Write()
        dataeff.Write('%s_%s_dataeff' % (name, tag))
        mceff.Write('%s_%s_mceff' % (name, tag))


## prompt electron

histFile = ROOT.TFile.Open(zmassdir + '/prompt_e/rootFile/plots_zmass_prompt_e.root')

hnormdata = histFile.Get('onZ/nZ/histo_DATA')
hnormmc = histFile.Get('onZ/nZ/histo_mc')

compute('prompte', histFile, 'onZ_trig', hnormdata, hnormmc)

histFile.Close()

## conversion

eHistFile = ROOT.TFile.Open(zmassdir + '/conversion/rootFile/plots_zmass_conversion.root')
gHistFile = ROOT.TFile.Open(zmassdir + '/photon/rootFile/plots_zmass_photon.root')

hnormdata = gHistFile.Get('onZ/nZ/histo_DATA')
hnormmc = gHistFile.Get('onZ/nZ/histo_mc')

ganging = {
    'base': [[x, x + 1, x + 2] for x in range(1, 31, 5)],
    'ptag': [range(1, 37)]
}

compute('conversion', eHistFile, 'onZ', hnormdata, hnormmc, ganging=ganging)
