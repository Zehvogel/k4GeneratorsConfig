#!/usr/bin/env bash
if [ -z "${KEY4HEP_STACK}" ]; then
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
fi

mg5_aMC MuonNeutrino91.2_ISR.dat
gunzip Output/Events/run_01/unweighted_events.lhe.gz
ln -sf Output/Events/run_01/unweighted_events.lhe unweighted_events.lhe
sed -i '/<header>/,/<\/header>/{//!d}' unweighted_events.lhe
$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i lhe -o hepmc3 unweighted_events.lhe MuonNeutrino91.2_ISR.hepmc
$CONVERTHEPMC2EDM4HEP/convertHepMC2EDM4HEP -i hepmc3 -o edm4hep MuonNeutrino91.2_ISR.hepmc MuonNeutrino91.2_ISR.edm4hep
