#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on December 2014

This uses the method develloped in:
M. Clerc, J. Kybic "Cortical mapping by Laplace–Cauchy transmission using a boundary element method".
calling the OpenMEEG class CorticalMat.
There is also an alternative solver CorticalMat2.

@author: - E. Olivi
This work has been done for the
CNRS, Laboratoire de Neurosciences Cognitives, UMR 7291, 13331, Marseille, France
under the supervision of Boris Burle
"""

import sys
import numpy as np
import openmeeg as om
from om_basics  import load_headmodel, forward_problem # openmeeg basics
from openmeeg_viz import display_vtp # visualiation with VTK
from om_compare import compare_vtp # rdm and mag errors
from os import path as op

# These are good parameters for cortical mapping reconstruction
alphas =dict(); betas = dict(); gammas = dict()
alphas['Head1'] = 1.e-4; betas['Head1'] = 1.58e-2; gammas['Head1'] = 12.4
alphas['Head2'] = 1.39e-7; betas['Head2'] = 1.e-5; gammas['Head2'] = 7.3
alphas['Head3'] = 2.69e-6; betas['Head3'] = 5.18e-5; gammas['Head3'] = 4.76
alphas['canonical'] = 1e-7; betas['canonical'] = 0.0413; gammas['canonical'] = 270.
alphas['canonical_real'] = 1e-7; betas['canonical_real'] = 0.0413; gammas['canonical_real'] = 780.
alphas['mni152'] = 1.3e-11; betas['mni152'] = 1.69e-9; gammas['mni152'] = 10.37
alphas['mni152_real'] = 1.3e-11; betas['mni152_real'] = 1.69e-9; gammas['mni152_real'] = 10.37

# adding a new model ?: put negative values for (alphas,betas), and the code
# will automatically estimated the parameters. (betas are often misestimated)
# for CorticalMat2: only choose a gamma parameter

# recompute or load matrices ?
recompute = True
recompute_CM = False
recompute_Xo = False

def main(argv):

    #create a dir for leadfields and tmp
    if not op.exists("tmp"):
        import os
        os.mkdir('tmp')
    if not op.exists("leadfields"):
        import os
        os.mkdir('leadfields')
    
    filename_O = 'leadfields/Original_' + argv + '.vtp'
    filename_R = 'leadfields/Reconstructed_' + argv + '.vtp'

    if recompute:
        # set matrices filenames
        filename_Xo = op.join('tmp', argv + '_Xo.mat')
        filename_CM = op.join('tmp', argv + '_CM.mat')

        model = load_headmodel(argv)
        # Compute the projector onto the sensors
        M = om.Head2EEGMat(model['geometry'], model['sensors'])

        # 'Brain' is the name of the domain containing the sources (a-priori)
        if recompute_CM or not op.exists(filename_CM): 
            # CM, a matrix N_unknown X N_sensors
            #CM = om.CorticalMat(model['geometry'], M, 'Brain',3, alphas[argv], betas[argv], op.join('tmp',argv + '_P.mat'))
            CM = om.CorticalMat2(model['geometry'], M, 'Brain',3, gammas[argv], op.join('tmp',argv + '_H.mat'))
            CM.save(str(filename_CM))
        else:
            CM = om.Matrix(str(filename_CM))

        if model.has_key('dipsources'):
            # for testing: lets compute a forward solution with a few dipoles
            # and then display both the reconstruction through the CorticalMapping
            # and the original
            if recompute_Xo or not op.exists(filename_Xo):
                X_original = forward_problem(model)
                X_original.save(str(filename_Xo))
            else:
                X_original = om.Matrix(str(filename_Xo))
            V_s = M * X_original # get the potentials at sensors
        elif model.has_key('potentials'):
            V_s = model['potentials']
        else:
            print("Error: either specify input potentials or dipsources to\
                  simulate them.")

        X_reconstructed = CM * V_s
        print "Error norm = ", (V_s-M * X_reconstructed).frobenius_norm()

        # write the geometry and the solution as a VTK file (viewable in pavaview)
        if model.has_key('dipsources'):
            model['geometry'].write_vtp(str(filename_O), X_original)
        model['geometry'].write_vtp(str(filename_R), X_reconstructed)

        if model.has_key('dipsources'):
            display_vtp(filename_O)
            compare_vtp(filename_O,filename_R)

    display_vtp(filename_R)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        main("canonical")
    else:
        if alphas.has_key(sys.argv[1]):
            main(sys.argv[1])
        else:
            print("Please specify a correct model (and set its default\
                  alphas).")
