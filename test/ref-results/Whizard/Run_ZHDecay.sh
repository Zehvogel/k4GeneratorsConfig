#!/usr/bin/env bash
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
whizard Run_ZHDecay.sin
$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep proc.hepmc ZHDecay.edm4hep
