Fake lepton estimates by source decomposition
=============================================

- Reference: https://indico.cern.ch/event/788744/contributions/3432812/attachments/1847971/3032818/fakes.pdf
  Note that the method has evolved somewhat since this presentation. The basic idea remains the same.

- Steps summary:
  - Produce skim ntuples for fake studies (NanoGardener module FakeSkimMaker).

  - Identify cuts that separate the fake sources well.
    For electrons, the sources are B hadron, C hadron, UDSG hadron, and conversion.
    For muons, the sources are mostly B and C hadrons.
    Verify the purity and efficiency of the tag cuts using mc_eff.py

  - Determine tagging (identification) efficiencies over prompt e/mu and conversion e by running the configurations under zmass/. Compute the efficiencies and scalefactors using prompt_conversion_eff.py.

  - Determine tagging efficiencies over hadronic sources through fits to distributions sensitive to hadron flavor. Distributions are made with configurations under efake/. Fits are performed in hadron_eff.py. 

  - Compute the weights with tf.py.

  - Validate the weights with configurations under validation/.
