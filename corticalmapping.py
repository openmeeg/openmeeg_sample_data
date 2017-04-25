#!/usr/bin/env python
"""
Created on December 2014.

This uses the method develloped in:
M. Clerc, J. Kybic "Cortical mapping by Laplace-Cauchy transmission using a
boundary element method".
calling the OpenMEEG class CorticalMat.
There is also an alternative solver CorticalMat2.

@author: - E. Olivi
This work has been done for the
CNRS, Laboratoire de Neurosciences Cognitives, UMR 7291,
13331, Marseille, France
under the supervision of Boris Burle
"""

import sys
import openmeeg as om
from om_basics import load_headmodel, forward_problem  # openmeeg basics
from openmeeg_viz import display_vtp  # visualiation with VTK
from om_compare import compare_vtp    # rdm and mag errors
from os import path as op

print(__doc__)

# These are good parameters for cortical mapping reconstruction
alphas = {'Head1': 1.e-4, 'Head2': 1.39e-7, 'Head3': 2.69e-6,
          'canonical': 1e-7, 'canonical_real': 1e-7,
          'mni152': 1.3e-11, 'mni152_real': 1.3e-11}
betas = {'Head1': 1.58e-2, 'Head2': 1.e-5, 'Head3': 5.18e-5,
         'canonical': 0.0413, 'canonical_real': 0.0413,
         'mni152': 1.69e-9, 'mni152_real': 1.69e-9}
gammas = {'Head1': 12.4, 'Head2': 7.3, 'Head3': 4.76,
          'canonical': 270., 'canonical_real': 780.,
          'mni152': 10.37, 'mni152_real': 10.37}

# adding a new model ?: put negative values for (alphas, betas), and the code
# will automatically estimated the parameters. (betas are often misestimated)
# for CorticalMat2: only choose a gamma parameter

# recompute or load matrices ?
recompute = True
recompute_CM = False
recompute_Xo = False


def main(argv):
    """Compute the cortical mapping."""
    # create a dir for leadfields and tmp
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
            # CM = om.CorticalMat(model['geometry'], M, 'Brain', 3, \
            #     alphas[argv], betas[argv], op.join('tmp', argv + '_P.mat'))
            CM = om.CorticalMat2(model['geometry'], M, 'Brain', 3,
                                 gammas[argv], op.join('tmp', argv + '_H.mat'))
            CM.save(str(filename_CM))
        else:
            CM = om.Matrix(str(filename_CM))

        if 'dipsources' in model:
            # for testing: lets compute a forward solution with a few dipoles
            # and then display both the reconstruction through the
            # CorticalMapping and the original
            if recompute_Xo or not op.exists(filename_Xo):
                X_original = forward_problem(model)
                X_original.save(str(filename_Xo))
            else:
                X_original = om.Matrix(str(filename_Xo))
            V_s = M * X_original  # get the potentials at sensors
        elif 'potentials' in model:
            V_s = model['potentials']
        else:
            print("Error: either specify input potentials or dipsources to",
                  "simulate them.")

        X_reconstructed = CM * V_s
        print("Error norm = ", (V_s - M * X_reconstructed).frobenius_norm())

        # write the geometry and the solution as a VTK file
        # (viewable in pavaview)
        if 'dipsources' in model:
            model['geometry'].write_vtp(str(filename_O), X_original)
        model['geometry'].write_vtp(str(filename_R), X_reconstructed)

        if 'dipsources' in model:
            display_vtp(filename_O)
            compare_vtp(filename_O, filename_R)

    display_vtp(filename_R)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        main("canonical")
    else:
        if sys.argv[1] in alphas:
            main(sys.argv[1])
        else:
            print("Please specify a correct model",
                  " (and set its default alphas)")
