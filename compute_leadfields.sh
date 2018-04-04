#!/usr/bin/env bash

GEOMETRY=data/model/head_model.geom
CONDUCTIVITIES=data/model/head_model.cond
DIPOLES=data/model/cortex_dipoles.txt
EEG_ELECTRODES=data/model/eeg_channels_locations.txt
EIT_ELECTRODES=data/model/eit_locations.txt
ECOG_ELECTRODES=data/model/ecog_electrodes_locations.txt
SQUIDS=data/model/meg_channels_locations.squids
INTERNAL_ELECTRODES=data/model/internal_electrodes_locations.txt

# Leadfields
EEG_LEADFIELD=leadfields/eeg_leadfield.mat
EEG_LEADFIELD_ADJOINT=leadfields/eeg_leadfield_adjoint.mat
ECOG_LEADFIELD=leadfields/ecog_leadfield.mat
MEG_LEADFIELD=leadfields/meg_leadfield.mat
MEG_LEADFIELD_ADJOINT=leadfields/meg_leadfield_adjoint.mat
EIT_LEADFIELD=leadfields/eit_leadfield.mat
IP_LEADFIELD=leadfields/ip_leadfield.mat
EITIP_LEADFIELD=leadfields/eitip_leadfield.mat

# Name temporary matrices
HM=tmp/tmp.hm           # For EEG and MEG
HMINV=tmp/tmp.hm_inv    # For EEG and MEG
DSM=tmp/tmp.dsm         # For EEG and MEG
H2EM=tmp/tmp.h2em       # For EEG
H2ECOGM=tmp/tmp.h2ecogm # For ECoG
H2MM=tmp/tmp.h2mm       # For MEG
DS2MEG=tmp/tmp.ds2mm    # For MEG
EITSM=tmp/tmp.eitsm     # For EIT
IPHM=tmp/tmp.iphm       # For IP
IPSM=tmp/tmp.ipsm       # For IP

mkdir -p tmp
mkdir -p leadfields

# Compute EEG gain matrix
time om_assemble -HM ${GEOMETRY} ${CONDUCTIVITIES} ${HM}
time om_minverser ${HM} ${HMINV}
time om_assemble -DSM ${GEOMETRY} ${CONDUCTIVITIES} ${DIPOLES} ${DSM}
time om_assemble -H2EM ${GEOMETRY} ${CONDUCTIVITIES} ${EEG_ELECTRODES} ${H2EM}
time om_gain -EEG ${HMINV} ${DSM} ${H2EM} ${EEG_LEADFIELD}
# or with the adjoint
#time om_gain -EEGadjoint ${GEOMETRY} ${CONDUCTIVITIES} ${DIPOLES} ${HM} ${H2EM} ${EEG_LEADFIELD_ADJOINT}

# Compute ECoG gain matrix
time om_assemble -H2ECOGM ${GEOMETRY} ${CONDUCTIVITIES} ${ECOG_ELECTRODES} "Cortex" ${H2ECOGM}
time om_gain -EEG ${HMINV} ${DSM} ${H2ECOGM} ${ECOG_LEADFIELD}

# Compute MEG gain matrix
time om_assemble -H2MM ${GEOMETRY} ${CONDUCTIVITIES} ${SQUIDS} ${H2MM}
time om_assemble -DS2MM ${DIPOLES} ${SQUIDS} ${DS2MEG}
time om_gain -MEG ${HMINV} ${DSM} ${H2MM} ${DS2MEG} ${MEG_LEADFIELD}
# or with the adjoint
time om_gain -MEGadjoint ${GEOMETRY} ${CONDUCTIVITIES} ${DIPOLES} ${HM} ${H2MM} ${DS2MEG} ${MEG_LEADFIELD_ADJOINT}

# Compute EIT gain matrix
time om_assemble -EITSM ${GEOMETRY} ${CONDUCTIVITIES} ${EIT_ELECTRODES} ${EITSM}
time om_gain -EEG ${HMINV} ${EITSM} ${H2EM} ${EIT_LEADFIELD}

# Compute Internal Potential ....
time om_assemble -H2IPM ${GEOMETRY} ${CONDUCTIVITIES} ${INTERNAL_ELECTRODES} ${IPHM}
# ...for internal dipoles
time om_assemble -DS2IPM ${GEOMETRY} ${CONDUCTIVITIES} ${DIPOLES} ${INTERNAL_ELECTRODES} ${IPSM}
time om_gain -IP ${HMINV} ${DSM} ${IPHM} ${IPSM} ${IP_LEADFIELD}
# ...for boundary-injected current
time om_gain -EITIP ${HMINV} ${EITSM} ${IPHM} ${EITIP_LEADFIELD}

