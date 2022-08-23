.. -*- mode: rst -*-

|GitHub Actions|_

.. |GitHub Actions| image:: https://github.com/openmeeg/openmeeg_sample_data/actions/workflows/testing.yml/badge.svg
.. _Github Actions: https://github.com/openmeeg/openmeeg_sample_data/actions/workflows/testing.yml

CAVEAT on using the python wrapper (see bottom)

**These examples contain mainly two different views on how to use OpenMEEG with scripting languages**

I) Computing/viewing EEG/MEG/EIT leadfields from bash, DOS, or Python
---------------------------------------------------------------------

It concerns files compute_leadfields.* view_leadfields.* mesh.py example_inverse_problem.py view_head_model.py.
The viewer works with mayavi.

II) Compute and apply a corticial mapping, TDCS (Transcranial direct-current stimulation)
-----------------------------------------------------------------------------------------

It concerns files::

	corticalmapping*.py tdcs.py data/canonical/* data/canonical_real/*

and uses Python tools for viewing::

	om_display.py, om_compare.py, om_basics.py

The viewer works with VTK.

Here are more details:

I) Computing/viewing EEG/MEG/EIT leadfields
-------------------------------------------

Demo scripts to compute leadfields with OpenMEEG:

- Supports EEG, MEG, EIT and Internal potential leadfields

This folder contains a sample realistic dataset for EEG, MEG, EIT
and internal potential forward modeling.

The head model is a 3 layers model with 3 nested meshes::

	brain.tri, skull.tri and head.tri

To run the computation you can use the scripts:

On windows (bat script):
------------------------

    compute_leadfields.bat

On Linux or Mac OS X (bash script):
-----------------------------------

	./compute_leadfields.sh

Or using Python:
----------------

	python compute_leadfields.py


The leadfields computed are stored in (matlab format):

    eeg_leadfield.mat (for EEG)

    meg_leadfield.mat (for MEG)

    eit_leadfield.mat (for EIT)

    ip_leadfield.mat (for Internal Potential)

The files used during the BEM computation are stored in the "tmp" folder.

See sample_output.txt to see what the scripts output should look like.

On a recent workstation the computation takes about::

           744.66 s  344.12 s   390.41 s om_assemble -HM
         + 431.74 s   188.5 s   246.5 s  om_inverser
         + 2689.71 s  545.1 s   719.13 s om_assemble -DSM
         + 0.13 s      0.02 s   0.04 s   om_assemble -H2EM
         + 80.92 s     3.19 s   16.42 s  om_gain -EEG
         + 3.39 s.     0.88 s   1.23 s   om_assemble -H2MM
         + 2.33 s      0.21 s   0.95 s   om_assemble -DS2MM
         + 84.84 s     4.17 s   17.65 s  om_gain -MEG
                                173.49 s om_assemble -EITSM
                                 1.15 s  om_gain -EEG


II) Compute and apply a corticial mapping, TDCS
-----------------------------------------------

- *canonical* is a model generated remeshing the MNI template from SPM. It uses conductivities, 1., 0.0125, 1. and has a few defined source terms (8) with intensities roughly at the same scale as the model. 128 electrodes.

- *canonical_real* is the same model with real potentials and sensors (64) locations.

commands:
---------
For cortical mapping:

	$ python corticalmapping.py canonical_real

For TDCS:

	$ python tdcs.py canonical


!!! CAVEAT on using OpenMEEG from Python !!!
=============================================

Beware that a temporary object has its memory released. So do not work with data provided from an OpenMEEG temporary object.

For example, having a symmetric matrix defined as:

	>>> M = om.SymMatrix(100)

Taking as a numpy array the sub-matrix of M might lead to corrupted memory:

	>>> mySubMat = om.asarray(M.submat(0,10,0,10))

since submat returns a newly created object that is hold by nothing, thus destroyed afterward.

Instead do keep an object pointing the newly created submatrix, and then
access the numpy array form of it:

	>>> subM = M.submat(0,10,0,10)
	>>> mySubMat = om.asarray(subM)

If you meet some difficulties running this example please contact:

openmeeg-info@lists.gforge.inria.fr

The OpenMEEG developers.

