############
Shared Stack
############

There are two shared LSST Science Pipelines "stacks" available at USDF, one in CernVM-FS and one in the Weka filesystem at ``/sdf/group/rubin/sw``.

.. _cernvm-fs-stack:

CernVM-FS
=========

A shared LSST Science Pipelines stack is maintained in the ``/cvmfs/sw.lsst.eu/almalinux-x86_64/lsst_distrib`` directory at USDF.
This stack is accessible to all interactive and batch nodes.
It includes conda environments and ``eups`` packages needed for using the LSST Science Pipelines.
Only weekly and official releases are included.

Usage
-----

To activate the conda environment for the latest weekly version of the stack in a fresh shell:

.. code-block:: bash

   source $(ls -d /cvmfs/sw.lsst.eu/almalinux-x86_64/lsst_distrib/w_* | tail -1)/loadLSST.sh

To activate the conda environment for a previous version of the stack in a fresh shell:

.. code-block:: bash

   source /cvmfs/sw.lsst.eu/almalinux-x86_64/lsst_distrib/{eups_tag}/loadLSST.sh

where ``{eups_tag}`` might be ``w_2026_16``, for example.

Within an activated ``rubin-env-developer`` conda environment, the ``setup`` command from ``eups`` is used to select a version of the LSST Science Pipelines for any given product (such as ``lsst_distrib``).
Exactly one version is available in any given conda environment.


Considerations
--------------

Since CernVM-FS caches files locally on each execution node, using this stack results in very few Weka filesystem metadata operations, resulting in greater computational efficiency.

Since CernVM-FS is immutable, it is the best source for production code.

Daily releases are not available in this stack; :ref:`the shared stack in the Weka filesystem <weka-stack>` should be used to access these.

Older versions of the stack were built under ``/cvmfs/sw.lsst.eu/linux-x86_64``.


Maintenance
-----------

The CernVM-FS stack is built and maintained by the French Data Facility at CC-IN2P3.
An ``#in2p3-cvmfs`` `channel <https://discovery-alliance.slack.com/archives/CLQL42BK9>`__ is available in the Discovery Alliance Slack for discussions about this stack.



.. _weka-stack:

Weka
====

A shared LSST Science Pipelines stack is maintained in the ``/sdf/group/rubin/sw`` directory at USDF.
This stack is accessible to all interactive and batch nodes.
It includes conda environments and ``eups`` packages needed for developing and using the LSST Science Pipelines.
Daily, weekly, and official releases are included.

Usage
-----

To activate the conda environment for the latest weekly version of the stack in a fresh shell:

.. code-block:: bash

   source /sdf/group/rubin/sw/loadLSST.sh

To activate the conda environment for the latest daily version of the stack in a fresh shell:

.. code-block:: bash

   source /sdf/group/rubin/sw/d_latest/loadLSST.sh

To activate the conda environment for a previous version of the stack in a fresh shell:

.. code-block:: bash

   source /sdf/group/rubin/sw/tag/{eups_tag}/loadLSST.sh

where ``{eups_tag}`` might be ``w_2026_16``, for example.

Within an activated ``rubin-env-developer`` conda environment, the ``setup`` command from ``eups`` is used to select a version of the LSST Science Pipelines for any given product (such as ``lsst_distrib``).
The default version (tag ``current``) is the most recent weekly version that was built with that conda environment (also available as tag ``w_latest``).
Other available versions will include the most recent daily version built with the conda environment (tag ``d_latest``) and other versions selected by explicit tag.
All available versions for a given conda environment can be listed using:

.. code-block:: bash

   eups tags

Currently, up to 48 daily releases, 26 weekly releases, and all official releases (including release candidates) are kept in the shared stack, but they will not all be available in a single conda environment.

The highest-level available product is currently configured to be ``lsst_sitcom``, which includes the commonly-used ``lsst_distrib`` product.


Considerations
--------------

The ``eups`` packaging system is very flexible, but its use for the LSST Science Pipelines involves creating very long ``PATH`` and ``PYTHONPATH`` environment variables.
Starting up Python processes and importing Python packages with these environment variables set involves searching through many directories, resulting in large numbers of filesystem metadata operations.
For human-triggered interactive usage, this is not a problem.
But automated processes including batch jobs (especially ones that run for a short amount of time and then start a new process) can result in massive metadata operation loads on the filesystem, slowing down everyone's access, including non-Rubin users of S3DF.
Since ``/sdf/home`` is on the same Weka cluster as ``/sdf/group``, user access to home directory files can also be slowed.

Batch jobs should either combine (cluster) processing so that processes run for at least tens of minutes or should use :ref:`the CernVM-FS stack <cernvm-fs-stack>`, which results in only local metadata operations.


Maintenance
-----------

The shared stack is maintained by the USDF Data Curation team using a cron job (running on ``sdfcron001`` under user ``rubinsw``) that executes a script from ``github.com/lsst-dm/shared-stack``.
This script automatically installs new releases from binaries.
This includes installing new conda environments as needed.
When a new environment is installed, it is augmented with additional packages useful for developers (but not needed in production) using the ``rubin-env-developer`` metapackage.

Conda environments are installed into ``/sdf/group/rubin/sw/conda/envs``, and ``eups`` packages are installed into ``share/eups`` within each environment.


.. toctree::
   :maxdepth: 1

