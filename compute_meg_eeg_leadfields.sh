#!/usr/bin/env bash

GEOMETRY=head_model.geom
CONDUCTIVITIES=head_model.cond
DIPOLES=cortex_dipoles.txt
EEG_ELECTRODES=eeg_channels_locations.txt
SQUIDS=meg_channels_locations.squids

# Leadfields
EEG_LEADFIELD=eeg_leadfield.dgem
MEG_LEADFIELD=meg_leadfield.dgmm

# Name temporary matrices
HM=tmp/tmp.hm           # For EEG and MEG
HMINV=tmp/tmp.hm_inv    # For EEG and MEG
DSM=tmp/tmp.dsm         # For EEG and MEG
H2EM=tmp/tmp.h2em       # For EEG
H2MM=tmp/tmp.h2mm       # For MEG
DS2MEG=tmp/tmp.ds2mm    # For MEG

mkdir -p tmp

# Compute EEG gain matrix
om_assemble -HM ${GEOMETRY} ${CONDUCTIVITIES} ${HM}
om_minverser ${HM} ${HMINV}
om_assemble -DSM ${GEOMETRY} ${CONDUCTIVITIES} ${DIPOLES} ${DSM}
om_assemble -H2EM ${GEOMETRY} ${CONDUCTIVITIES} ${EEG_ELECTRODES} ${H2EM}
om_gain -EEG ${HMINV} ${DSM} ${H2EM} ${EEG_LEADFIELD}

# Compute MEG gain matrix
om_assemble -H2MM ${GEOMETRY} ${CONDUCTIVITIES} ${SQUIDS} ${H2MM}
om_assemble -DS2MM ${DIPOLES} ${SQUIDS} ${DS2MEG}
om_gain -MEG ${HMINV} ${DSM} ${H2MM} ${DS2MEG} ${MEG_LEADFIELD}
