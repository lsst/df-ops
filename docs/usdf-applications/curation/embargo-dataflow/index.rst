####################################
DataFlow in the USDF Embargo Storage
####################################

**This is an unfinished draft document. More content will be added later.**

From Rubin Summit, raw image data are ingested to the USDF embargo storage (Ceph S3). Several groups
of events will happen after the data ingestion:

- Trigger Prompt Processing(PP) and Rapid Analysis(RA)/Nightly Validation(NV) in the USDf Kubernetes.
- Unembargo raw image data and prompt products to the USDF main storage after the 80h embargo period.
- Write raw data to USDF HPSS and transfer raw data to FrDF for long-term archival.
- Publish prompt products.

This document intends to give an overview of each group of events, with links to the technical details
with available. This document will be updated as we gain more understanding of the current dataflow.

Data Ingestion and Notifications
================================

Under normal night operation, Rubin Summit is expected to ingest 205 detector images (189 science
images + 8 wavefront images (also considered science images) and 8 guiders images) every minute to
the USDF embargo CEPH S3 storage. All images from an exposure (and the associated .json files)
are saved to a foler like

.. code-block:: text

  embargo/rubin-summit/LSSTCam/YYYYMMDD/<EXPOSURE_ID>/

where ``embargo`` refers to the embargo S3 storage and ``EXPOSURE_ID`` is like ``MC_O_20251231_000010``.

Each time an new object/file is ingested to the ``rubin-summit`` bucket,  two notification event are
triggered:

- via a Webhook to the ``embargo-butler-enqueue`` service (path "/notify") running
  in vCluster ``usdf-embargo-dmz``, name space ``summit-new`` (After that, the other services in the
  ``summit-new`` namespace will then ingest the new raw images to the ``embargo`` Butler). Rapid
  Analysis is generally triggered by polling the Butler for completion of ingest. Nightly Validation is
  no longer running against the Embargo.
- vai a Kafka message to trigger Prompt processing. See the `Link text <../s3-file-notifications>`__.

The Embargo s3's ``rubin-summit`` bucket is configured to send these notificatios. CEPH has an
internal queue with topic name ``rubin-ingest-embargo-new2``. The creation of a new object in the
``rubin-summit`` bucket and the notification sending is currently configured as a synchronous
but non-blocking operation: If not notification failed to be added to the internal CEPH queue,
the object will not be saved. If the notification failed to be sent to the downsteam services,
the object will still be saved.

Unembargo Raw Image Data
========================

After the raw imaged data reach the 80h embargo period, they need to be unembargoed. This is a
automated process running. The following describes the tools and steps for unembargoing the raw
image data and how and where the automated process runs.

The ``transfer_raw_zip`` Tool
-----------------------------

The ``transfer_raw_zip.py`` in https://github.comr/lsst-dm/transfer_embargo (branch tickets/DM-51619) is
used to unembargo raw image data. This tool will unembargo the data:

- Transfer from ``embargo`` S3 storage's ``rubin-summit`` bucket to the destination directory
  ``/sdf/data/rubin/lsstdata/offline/instrument/LSSTCam`` in the USDF main storage. All files of an exposure
  are zipped into a single zip file (e.g. ``<dest_dir>/20251231/MC_O_20251231_000010.zip``), along with
  a _dimensions.yaml file named in the same way (e.g. ``<dest_dir>/20251231/MC_O_20251231_000010_dimensions.yaml``).
  The _dimensions.yaml file contains dimension metadata needed for importing the .zip at a remote
  site's Butler (e.g. FrDF and UKDFs)
- Transfer dimension records from source butler ``embargo`` to destination butler ``main``.

The tool will first select all the exposures that meet the selection windows (see below). For each exposure
it will do the following orderred steps:

- If the destination .zip file already exists, skip to the next exposure.
- Query the source butler to find out which Tracts the exposure belongs to.
- Make the zip file in a temporary location, check again if the destination .zip file already exists, if not,
  move the zip file to the destination directory.
- Gether the dimension records and write to the _dimensions.yaml file in the destination directory.
- Transfer the dimension records from source butler to destination butler.
- Ingest the zip file to the destination butler.
- Register the zip file to Rucio

  * Inplace register the zip file to Rucio with DID ``raw:LSSTCam/20251231/MC_O_20251231_000010.zip``
  * Add the DID to the corresponding Tract (Rucio) datasets (e.g. ``raw:Dataset/LSSTCam/raw/Tract4206/20251231``,
    and other tracts e.g. ``Tract4207``, or NoTract datasets)
  * Add the DID to the ``Obs`` dataset (e.g. ``raw:Dataset/LSSTCam/raw/Obs/20251231/MC_O_20251231_000010``)

- Do the same for the _dimensions.yaml file:
- Add Rucio metadata (key: arcBackup, value: SLAC_RAW_DISK_BKUP:need) to the ``Obs`` (Rucio) dataset so that it
  will be backed up to HPSS later.

Note:

- Both Butler and Rucio use the word "dataset". They mean differently.
- A Tract dataset contains multiple exposures as Tracts overlap each other at the edge. Obs dataset contains only one exposure.

Automated Unembargo Process
---------------------------

The automated unembargo process runs in vCluster ``usdf-embargo-dmz``, namespace ``transfer``.
The process is managed by a Kubernetes cron job. See `transfer-raw-deploy.yaml
<https://github.com/slaclab/usdf-embargo-deploy/blob/tickets/DM-51916/kubernetes/overlays/transfer/transfer-raw-deploy.yaml>`_
(branch ``tickets/DM-51916``). Every
15 minutes, the cron job deploys a pod that runs the ``transfer_raw_zip.py`` tool. The pod will
unembargo all the raw images that have reached the 80h embargo period but not older than 80h + 35m.
Use the following commands to check what those pods do:

.. code-block:: bash

  <setup Kubernetes access to usdf-embargo-dmz vCluster>
  kubectl -n transfer get cronjob
  kubectl -n transfer get pods
  kubectl -n transfer describe pod transfer-embargo-raw-29459674-wm5jm

Failure and Recovery
--------------------

The ``transfer_raw_zip.py`` tool runs many steps for each exposure. For various reasons, the tool may fail
(Out-of-Memory, storage issue, etc.) and leave an exposure not fully unembargoed. In most cases, the
subsequent runs of the tool will NOT
be able to pick up the unfinished exposures because the zip file likely already exists in the
destination directory. To recover from such failures, a manual intervention is needed. **But unless we
carefully check the logs of each run of the tool, we may not know which exposures are not fully
unembargoed.**.

Detect Exposures Not Unembargoed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We can use the following command to check which exposures have been unembargoed and registered in Rucio
(those that completed all Rucio related ``transfer_raw_zip`` steps must have also
completed previous steps).

.. code-block:: bash

  rucio did list --filter="type=dataset" --short raw:Dataset/LSSTCam/raw/Obs/<YYYYMMDD>/*

This will list all the exposures known to Rucio (as the ``Obs`` datasets) for a given day. We can compare
this list with all exposures stored in the ``embargo`` storage (command below) for the same day to find
out which exposures are NOT unembargoed.

.. code-block:: bash

  mc ls embargo/rubin-summit/LSSTCam/<YYYYMMDD>

