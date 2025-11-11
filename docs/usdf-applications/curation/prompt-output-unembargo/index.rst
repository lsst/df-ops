##########################
Unembargo Propmpt Products
##########################

This document describes how to unembargo prompt products from Rubin embargo storage. It is intended for the
members of the data curation team. While the read access of the Rubin embargo storage and embargo Butler can
be done by each member, the actual unembargo operation should be coordinated by the data curation team and
run via a single service account (TBD) that has privileges to write data to the USDF main storage and modify
several Butler DBs in the document.

We will unembago data from the USDF embargo storage and ``embargo`` Butler to the USDF main storage and the
``main`` Butler.

Note that the doc will be obsolete once the tool in `DMTN-330 <https://dmtn-330.lsst.io/v/DM-53016/index.html>`_
is implemented and deployed.

Setup Environment
=================

Credentials files
-----------------

- ``$HOME`` refers the the home directory of the service account that will run the unembargo operation.
- ``$HOME/.lsst/postgres-credentials.txt`` contains the credentials to access viarious Butler Postgres DBs. This file should contain credential to read the ``embargo`` bulter DB and read/write to the ``main`` butler DB.
- If you have a ``$HOME/.lsst/db-auth.yaml`` file. rename it to something else.
- ``$HOME/.lsst/aws-credentials.ini`` contains the credentials to access viarious Ceph Object Storage, e.g Rubin embargo s3.
- You should also have the filesystem write permission to ``/sdf/group/rubin/repo/main``.

Setup environment
-----------------

Login to rubin-devl and run

.. code-block:: bash

   source /sdf/group/rubin/sw/profile.d/05-permissions.conf
   source /sdf/group/rubin/sw/profile.d/10-rubin.conf
   source /sdf/group/rubin/sw/profile.d/20-ceph.conf
   source /sdf/group/rubin/sw/profile.d/30-tmpdir.conf
   source /sdf/group/rubin/sw/profile.d/40-postgres.conf

   source /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/w_2025_10/loadLSST.sh
   setup obs_lsst

The first five ``source`` commands are probably already in your ``$HOME/.profile.d``.
Afte this setup, you should have the following envionment variables defined:

- ``PGUSER=rubin``
- ``PGPASSFILE=$HOME/.lsst/postgres-credentials.txt``
- ``DAF_BUTLER_REPOSITORY_INDEX=/sdf/group/rubin/shared/data-repos.yaml``. This file list all the aliases of
  Rubin Butlers.

Check the prompt products to unembargo
======================================

Choose a day that you want to unembargo all the prompt products for. For example, 2025-11-01. Run the following
command to see prompt products collection in the ``embargo`` Butler for that day:

.. code-block:: bash

   butler query-collections embargo LSSTCam/prompt/output-2025-11-01

The output should look like:

.. code-block::

                                           Name                                              Type
  ------------------------------------------------------------------------------------------ -------
  LSSTCam/prompt/output-2025-11-01                                                           CHAINED
    LSSTCam/prompt/output-2025-11-01/NoPipeline/pipelines-682fa38-config-8f017ea             RUN
    LSSTCam/prompt/output-2025-11-01/Preprocessing-noForced/pipelines-682fa38-config-8f017ea RUN
    LSSTCam/prompt/output-2025-11-01/SingleFrame/pipelines-682fa38-config-8f017ea            RUN
    LSSTCam/prompt/output-2025-11-01/ApPipe-noForced/pipelines-682fa38-config-8f017ea        RUN
    LSSTCam/prompt/output-2025-11-01/Isr-cal/pipelines-682fa38-config-8f017ea                RUN
    LSSTCam/prompt/output-2025-11-01/Isr/pipelines-682fa38-config-8f017ea                    RUN

``LSSTCam/prompt/output-2025-11-01`` is a CHAIN collection. In this example, it contains six RUN collections
(could be more than six). These RUN collections contain the actual prompt products that we will need to
unembargo

Each of the RUN collection contains a number of datasets, ranging from a few to many. To see how many
datasets in a RUN collection, run

.. code-block:: bash

  butler query-datasets --collections <a-RUN-collection> --limit 0 embargo '*' | wc -l

The above command also counts headers and blank lines, but will give you an idea of how many datasets are there.

Unembargo prompt products
=========================

LSST-DM's transfer_embargo repo contains tools that we can use to unembargo these prompt products. The source
butler is ``embargo`` and the destination butler is ``main``. Follow
the following steps to checkout the tool and prepare to run it.

- ``git clone https://github.com/sst-dm/transfer_embargo``
- ``cd transfer_embargo``
- ``git checkout -b tickets/DM-51619``
- ``cd src``

Edit the ``collections`` line in ``config_non_raw.yaml``:

.. code-block::

  - dataset_types: "*"
    collections: "<one-of-the-run-collections-from-the-above>"
    embargo_hours: 80
    instrument: "LSSTCam"
    where: ""
    avoid_dstypes_from_collections:
    - "refcats/*"
    - "skymaps"
    - "pretrained_models/*"
    - "LSSTCam/raw/all"
    - "LSSTCam/calib"

Then run the following command

.. code-block:: bash

  python ./transfer_non_raw.py --config_file ./config_non_raw.yaml embargo main

The RUN collections above can be unembarged in parallel.

Remove prompt products after unembargo
======================================

<doc under development>

Use the following command to remove the RUN collections

.. code-block:: bash

  butler remove-runs embargo <a-RUN-collection> ???

<do we need to delete the empty CHAIN collections in ``embargo``?>

Recreate the CHAIN collection
=============================

<is this step needed, who should do it?>

Recreate the CHAIN collection in ``main`` using the following commando

.. code-block:: bash

  butler collection-chain main LSSTCam/prompt/output-2025-11-01 \
  LSSTCam/prompt/output-2025-11-01/NoPipeline/pipelines-682fa38-config-8f017ea,\
  LSSTCam/prompt/output-2025-11-01/Preprocessing-noForced/pipelines-682fa38-config-8f017ea,\
  LSSTCam/prompt/output-2025-11-01/SingleFrame/pipelines-682fa38-config-8f017ea,\
  LSSTCam/prompt/output-2025-11-01/ApPipe-noForced/pipelines-682fa38-config-8f017ea,\
  LSSTCam/prompt/output-2025-11-01/Isr-cal/pipelines-682fa38-config-8f017ea,\
  LSSTCam/prompt/output-2025-11-01/Isr/pipelines-682fa38-config-8f017ea

Note:

- The last parameter is a comma-separated list of all the RUN collections in the CHAIN collection. It is a
  single parameter, so there should be no space after the commas.
- In a CHAIN collection, the order of the RUN collections matters. The order should be the same
  as the one shown by the ``butler query-collections embargo LSSTCam/prompt/output-2025-11-01`` command above.
