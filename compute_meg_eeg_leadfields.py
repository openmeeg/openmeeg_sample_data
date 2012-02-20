#!/usr/bin/env python

import openmeeg as om
from os import path
import sys

# =============
# = Load data =
# =============

geomFile        = 'head_model.geom'
condFile        = 'head_model.cond'
dipolesFile     = 'dipoles.txt'
squidsFile      = 'meg_channels_locations.txt'
electrodesFile  = 'eeg_channels_locations.txt'

geom = om.Geometry()
geom.read(geomFile,condFile)

mesh = om.Mesh()
mesh.load(sourceMeshFile)

dipoles = om.Matrix()
dipoles.load(dipoleFile)

sensors = om.Sensors()
sensors.load(squidsFile)

patches = om.Matrix()
patches.load(patchesFile)

# ======================
# = Compute Leadfields =
# ======================

gaussOrder = 3
use_adaptive_integration = True

hm            = om.HeadMat(geom,gaussOrder)
hminv         = hm.inverse()
# ssm           = om.SurfSourceMat(geom,mesh,gaussOrder)
# ss2mm         = om.SurfSource2MEGMat(mesh,sensors)
dsm           = om.DipSourceMat(geom,dipoles,gaussOrder,use_adaptive_integration)

# For EEG
# h2em          = om.Head2EEGMat(geom,patches)

# For MEG
ds2mm         = om.DipSource2MEGMat(dipoles,sensors)
# h2mm          = om.Head2MEGMat(geom,sensors)

meg_leadfield = om.GainMEG(hminv,dsm,h2mm,ds2mm)
# eeg_leadfield = om.GainEEG(hminv,dsm,h2em)

print "hm              : %d x %d"%(hm.nlin(),hm.ncol())
print "hminv           : %d x %d"%(hminv.nlin(),hminv.ncol())
print "ssm             : %d x %d"%(ssm.nlin(),ssm.ncol())
print "ss2mm           : %d x %d"%(ss2mm.nlin(),ss2mm.ncol())
print "dsm             : %d x %d"%(ssm.nlin(),ssm.ncol())
print "ds2mm           : %d x %d"%(ss2mm.nlin(),ss2mm.ncol())
print "h2mm            : %d x %d"%(h2mm.nlin(),h2mm.ncol())
print "h2em            : %d x %d"%(h2mm.nlin(),h2mm.ncol())
print "eeg_leadfield   : %d x %d"%(eeg_leadfield.nlin(),eeg_leadfield.ncol())
print "meg_leadfield   : %d x %d"%(meg_leadfield.nlin(),meg_leadfield.ncol())
