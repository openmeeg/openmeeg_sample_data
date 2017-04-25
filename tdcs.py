#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tues. January 14 2014

@author: - E. Olivi
This work has been done for the
CNRS, Laboratoire de Neurosciences Cognitives, UMR 7291,
13331, Marseille, France
under the supervision of Boris Burle
"""

import sys
import numpy as np
import openmeeg as om
from om_basics import load_headmodel  # openmeeg basics
from openmeeg_viz import display_vtp  # visualiation with VTK
from os import path as op

print(__doc__)

# recompute or load matrices ?
recompute = True
recompute_HMi = False

#############################################################################
# Load data


def main(argv):

    # create a dir for leadfields and tmp
    if not op.exists("tmp"):
        import os
        os.mkdir('tmp')
    if not op.exists("leadfields"):
        import os
        os.mkdir('leadfields')

    filename = 'leadfields/HDTDCS_' + argv + '.vtp'
    filename_HMi = op.join('tmp', argv + '_HMi.mat')

    if recompute:
        model = load_headmodel(argv)
        if recompute_HMi or not op.exists(filename_HMi):
            hm = om.HeadMat(model['geometry'])
            hm.invert()
            hm.save(filename_HMi)
        else:
            print("Loading %s" % filename_HMi)
            hm = om.SymMatrix(filename_HMi)

        sm = om.EITSourceMat(model['geometry'], model['tdcssources'])
        # set here the input currents (actually a current density [I/L])
        activation = om.fromarray(
            np.array([[-4., 1.], [1., -4.], [1., 1.], [1., 1.], [1., 1.]]))
        # each column must have a zero mean
        # now apply the currents and get the result
        X = hm * (sm * activation)
        # concatenate X with input currents (to see the what was injected)
        Xt = np.append(om.asarray(X),
                       np.zeros((model['geometry'].size() - X.nlin(),
                                 X.ncol())),
                       0)
        currents = om.asarray(activation)
        for s in range(model['tdcssources'].getNumberOfSensors()):
            # get the triangles supporting this sensor
            tris = model['tdcssources'].getInjectionTriangles(s)
            for it in tris:
                Xt[it.getindex(), :] = (currents[s, :] *
                                        model['tdcssources'].getWeights()(s))

        X = om.fromarray(Xt)
        model['geometry'].write_vtp(filename, X)

    display_vtp(filename)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        main("canonical")
    else:
        main(sys.argv[1])
