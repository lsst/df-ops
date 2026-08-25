############
Stack Access
############

This document describes access to nightly, weekly, and release versions of the
LSST Science Pipelines "stack" available at the USDF.

Release and Weekly
==================

Access to self-contained release and weekly versions is available via cvmfs (e.g. ``v24.0.0`` or ``w_2023_01``).
Each version is available in three variants: a Conda environment with minimal dependencies for processing data, an extended Conda environment with packages appropriate for code developers, and an Apptainer container with the minimal environment.

Minimal processing Conda environment:

.. code-block:: bash

   source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2023_01/loadLSST.bash

Developer-friendly Conda environment:

.. code-block:: bash

   source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2023_01/loadLSST-ext.bash

Minimal processing Apptainer:

.. code-block:: bash

   apptainer run-help /cvmfs/sw.lsst.eu/containers/apptainer/lsst_distrib/w_2023_01.sif

provides more information.

You can see which versions are available by:
``ls /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/``
and
``ls /cvmfs/sw.lsst.eu/containers/apptainer/lsst_distrib/``
