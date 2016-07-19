# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 2013

@author: - E. Olivi
"""

import openmeeg as om
from os import path as op

def load_headmodel(name,prefix='data'):
    """ Load a headmodel: read the geometry, conductivities and sources
    eventually."""
    cond_file = op.join(prefix, name, name + '.cond')
    geom_file = op.join(prefix, name, name + '.geom')
    patches_file = op.join(prefix, name, name + '.patches')
    dip_file = op.join(prefix, name, name + '.dip')
    tdcs_file = op.join(prefix, name, name + '.hdtdcs')
    pot_file = op.join(prefix, name, name + '.pot')
    geom = om.Geometry()
    geom.read(str(geom_file), str(cond_file))
    sensors = om.Sensors()
    sensors.load(str(patches_file))
    model = {'geometry':geom, 'sensors':sensors}
    if op.exists(dip_file):
        dipoles = om.Matrix(str(dip_file))
        model['dipsources'] = dipoles
    if op.exists(tdcs_file):
        tdcs = om.Sensors(str(tdcs_file), geom)
        model['tdcssources'] = tdcs
    if op.exists(pot_file):
        pot = om.Matrix(str(pot_file))
        model['potentials'] = pot
    return model

def forward_problem(m):
    """ Compute a Forward problem given a model with geometry and sources """
    hm = om.HeadMat(m['geometry'])
    hm.invert() # invert in place (no copy)
    dsm   = om.DipSourceMat(m['geometry'], m['dipsources'])
    return hm*dsm

