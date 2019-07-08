import os
import sys

PLOTDIR = '/afs/cern.ch/user/y/yiiyama/www/plots/hww/zmass'

source = sys.argv[1]
del sys.argv[1:]

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

try:
    from common import tnames
except ImportError:
    confdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(confdir)
    from common import tnames, ptbinning, etabinning

try:
    os.makedirs(os.path.join(PLOTDIR, source))
except OSError:
    pass

nptbins = len(ptbinning) - 1
netabins = len(etabinning) - 1

canvas = ROOT.TCanvas('c1', 'c1', 600, 600)
canvas.SetLeftMargin(0.15)
canvas.SetRightMargin(0.05)
canvas.SetBottomMargin(0.15)
canvas.SetTopMargin(0.05)

matcanvas = ROOT.TCanvas('mat', 'mat', 800, 800)

legend = ROOT.TLegend(0.2, 0.7, 0.4, 0.9)
legend.SetBorderSize(0)
legend.SetFillStyle(0)

gdata = ROOT.TGraph(1)
gdata.SetLineColor(ROOT.kRed)
gdata.SetLineWidth(2)
gdata.SetFillColor(ROOT.kRed)
gdata.SetFillStyle(3004)
legend.AddEntry(gdata, 'Data', 'LF')

gmc = ROOT.TGraph(1)
gmc.SetLineColor(ROOT.kGray + 2)
gmc.SetLineWidth(2)
gmc.SetFillColor(ROOT.kGray)
gmc.SetFillStyle(1001)
legend.AddEntry(gmc, 'MC', 'LF')

def style(hist, temp):
    hist.SetTitle('')
    hist.GetXaxis().SetLabelSize(0.06)
    hist.GetYaxis().SetLabelSize(0.06)
    hist.SetLineColor(temp.GetLineColor())
    hist.SetLineWidth(temp.GetLineWidth())
    hist.SetFillColor(temp.GetFillColor())
    hist.SetFillStyle(temp.GetFillStyle())

histFile = ROOT.TFile.Open(os.path.join(os.path.dirname(__file__), source, 'rootFile', 'plots_zmass_%s.root' % source))

if source == 'photon':
    tags = ['notag']
else:
    tags = ['notag'] + tnames

for tag in tags:
    if tag == 'notag':
        stag = ''
    else:
        stag = '_' + tag

    canvas.cd()
    
    hdata = histFile.Get('base%s/mass/histo_DATA' % stag)
    hmc = histFile.Get('base%s/mass/histo_mc' % stag)
    style(hdata, gdata)
    style(hmc, gmc)
    hmc.Draw('HIST')
    hdata.Draw('HIST SAME')
    legend.Draw()
    hmc.SetMaximum(max(hmc.GetMaximum(), hdata.GetMaximum()) * 1.2)
    
    canvas.Print(os.path.join(PLOTDIR, source, '%s.pdf' % tag))
    canvas.Print(os.path.join(PLOTDIR, source, '%s.png' % tag))
    canvas.Clear()

    template = hdata.Clone('template')
    template.Reset()

    hdataetamerged = [template.Clone('hdataetamerged%d' % ipt) for ipt in range(nptbins)]
    hmcetamerged = [template.Clone('hmcetamerged%d' % ipt) for ipt in range(nptbins)]

    matcanvas.Divide(nptbins, netabins)

    for ieta in range(netabins):
        hdataptmerged = template.Clone('hdataptmerged')
        hmcptmerged = template.Clone('hdataptmerged')
        for ipt in range(nptbins):
            matcanvas.cd(nptbins * (netabins - 1 - ieta) + 1 + ipt)
            
            hdata = histFile.Get('basebinned%s_pt%d_eta%d/mass/histo_DATA' % (stag, ipt, ieta))
            hmc = histFile.Get('basebinned%s_pt%d_eta%d/mass/histo_mc' % (stag, ipt, ieta))
            style(hdata, gdata)
            style(hmc, gmc)
            hmc.Draw('HIST')
            hdata.Draw('HIST SAME')
            hmc.SetMaximum(max(hmc.GetMaximum(), hdata.GetMaximum()) * 1.2)

            hdataptmerged.Add(hdata)
            hmcptmerged.Add(hmc)

            hdataetamerged[ipt].Add(hdata)
            hmcetamerged[ipt].Add(hmc)

        canvas.cd()
        style(hdataptmerged, gdata)
        style(hmcptmerged, gmc)
        hmcptmerged.Draw('HIST')
        hdataptmerged.Draw('HIST SAME')
        legend.Draw()
        hmcptmerged.SetMaximum(max(hmcptmerged.GetMaximum(), hdataptmerged.GetMaximum()) * 1.2)
    
        canvas.Print(os.path.join(PLOTDIR, source, '%s_eta%d.pdf' % (tag, ieta)))
        canvas.Print(os.path.join(PLOTDIR, source, '%s_eta%d.png' % (tag, ieta)))
        canvas.Clear()

        hdataptmerged.Delete()
        hmcptmerged.Delete()

    template.Delete()

    canvas.cd()
    for ipt in range(nptbins):
        hdata = hdataetamerged[ipt]
        hmc = hmcetamerged[ipt]
        style(hdata, gdata)
        style(hmc, gmc)
        hmc.Draw('HIST')
        hdata.Draw('HIST SAME')
        legend.Draw()
        hmc.SetMaximum(max(hmc.GetMaximum(), hdata.GetMaximum()) * 1.2)
    
        canvas.Print(os.path.join(PLOTDIR, source, '%s_pt%d.pdf' % (tag, ipt)))
        canvas.Print(os.path.join(PLOTDIR, source, '%s_pt%d.png' % (tag, ipt)))
        canvas.Clear()

    matcanvas.Print(os.path.join(PLOTDIR, source, '%s_binned.pdf' % tag))
    matcanvas.Print(os.path.join(PLOTDIR, source, '%s_binned.png' % tag))
    matcanvas.Clear()
