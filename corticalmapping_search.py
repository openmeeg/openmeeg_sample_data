#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This code is made to search parameters for the cortical mapping.
Either alphas, betas for the CorticalMat
    or gammas for the CorticalMat2

"""

from __future__ import print_function
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import openmeeg as om
from om_basics import load_headmodel, forward_problem  # openmeeg basics
from om_compare import compare_vtp  # rdm and mag errors
from os import path as op

# recompute or load matrices
recompute = True
recompute_CM = True
recompute_Xo = False
Axes3D


def main(argv):
    filename_O = 'leadfields/Original_' + argv + '.vtp'
    filename_R = 'leadfields/Reconstructed_' + argv + '.vtp'
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # ax.xaxis.set_scale('log')
    # ax.yaxis.set_scale('log')
    # ax.zaxis.set_scale('log')
    N1 = 5  # choose sampling here
    N2 = 1  # choose sampling here
    xs = np.random.rand(N1, N2)
    ys = np.random.rand(N1, N2)
    zs = np.random.rand(N1, N2)

    alphas = np.logspace(0.3, 1.5, N1)
    betas = np.logspace(0.3, -0.3, N2)
    for alph in range(0, N1):
        for bet in range(0, N2):

            if recompute:
                # set matrices filenames
                filename_Xo = op.join('tmp', argv + '_Xo.mat')
                filename_CM = op.join('tmp', argv + '_CM.mat')

                model = load_headmodel(argv)
                # Compute the projector onto the sensors
                M = om.Head2EEGMat(model['geometry'], model['sensors'])

                # 'Brain' is the name of the domain containing the sources
                # (a-priori)
                if recompute_CM or not op.exists(filename_CM):
                    alpha = alphas[alph]
                    beta = betas[bet]
                    # CM, a matrix N_unknown X N_sensors
                    # CM = om.CorticalMat(model['geometry'], M, 'Brain', 3,
                    #      alpha, beta, op.join('tmp', argv + '_P.mat'))
                    CM = om.CorticalMat2(model['geometry'], M, 'Brain', 3,
                                         alpha,
                                         op.join('tmp', argv + '_H.mat'))
                    CM.save(str(filename_CM))
                else:
                    CM = om.Matrix(str(filename_CM))

                # for testing: lets compute a forward solution with a few
                # dipoles and then display both the reconstruction through the
                # CorticalMapping and the original
                if recompute_Xo or not op.exists(filename_Xo):
                    X_original = forward_problem(model)
                    X_original.save(str(filename_Xo))
                else:
                    X_original = om.Matrix(str(filename_Xo))

                V_s = M * X_original  # get the potentials at sensors
                X_reconstructed = CM * (V_s)

                # write the geometry and the solution as a VTK file
                # (viewable in pavaview)
                model['geometry'].write_vtp(str(filename_R), X_reconstructed)

            norm = (V_s-M*X_reconstructed).getcol(0).norm()
            rdm, mag = compare_vtp(filename_O, filename_R)
            print("||=%f" % norm, "\talpha=%f" % alpha, "\tbeta=%f" % beta,
                  "\t\tRDM=%f" % rdm, "\trMAG=%f" % mag, "\t", str(mag + rdm),
                  "\n", file=sys.stderr)
            print("||=%f" % norm, "\talpha=%f" % alpha, "\tbeta=%f" % beta,
                  "\t\tRDM=%f" % rdm, "\trMAG=%f" % mag, "\t", str(mag + rdm),
                  "\n")
            xs[alph, bet] = alpha
            ys[alph, bet] = beta
            zs[alph, bet] = rdm + mag

    ax.plot_wireframe(np.log(xs), np.log(ys), np.log(zs))
    ax.set_xlabel('alpha')
    ax.set_ylabel('beta')
    ax.set_zlabel('RDM + MAG')
    i = np.nonzero(zs == np.min(zs))
    print('xs = %f' % xs[i], ' ys = %f' % ys[i], ' rdm+mag=%f' % np.min(zs),
          "\n", file=sys.stderr)
    print('xs = %f' % xs[i], ' ys = %f' % ys[i], ' rdm+mag=%f' % np.min(zs),
          "\n")
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        main("canonical")
    else:
        main(sys.argv[1])
