##########
Procedures
##########

Intended audience: Anyone who is administering Data Transfer Monitoring.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployment is through a Makefile in the code repository.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

Backup
======
.. Procedures for backup including how to verify backups.

No backups needed as the application does not store state.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

No specific cold startup procedures needed.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No specific cold shutdown procedures needed.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

Deploy another instance.

.. _Calculate_File_Counts:

Calculate File Counts
=====================

Do not rely on File Notifications for accurate file counts since resent file generates duplicate file notifications for the same file.  Run a recursive word count for the directory.  Example below.

.. rst-class:: technote-wide-content

.. code-block:: bash

   mc ls -r rubin-summit/rubin-summit/LSSTCam/20250921 | wc

Review End Readout and File Transfer Logs
=========================================

Logs for End Readout messages and Summit to USDF Transfer time are in the logs.  This can be manually reviewed to validate transfer times. The `End to End Dashboard Logs <https://grafana.slac.stanford.edu/d/ff4swfag270g0e/end-to-end-dashboard-logs?orgId=1&from=now-24h&to=now&timezone=browser&var-dateAndExposure=20251120_000122>`__ provides a filter variable.  Enter the Date and Sequence number in in ``YYYYMMDD_000<sequence number >`` format.  An example is format is ``20251120_000122``

The output below is an example.

.. rst-class:: technote-wide-content

.. code-block:: text

    INFO:listeners.end_readout:end readout message: EndReadoutModel(private_sndStamp=1764038140.1819582, private_rcvStamp=0.0, private_efdStamp=1764038103.1819582, private_kafkaStamp=1764038140.1819582, private_seqNum=174564, private_revCode='834c6ef5', private_identity='ocs-bridge', private_origin=309651235, additional_keys='imageType:groupId:testType:stutterRows:stutterNShifts:stutterDelay:reason:program', additional_values='OBJECT:2025-11-25T02\\:34\\:56.976:OBJECT:0:0:0.0:FixedChaosMonkeyTest:BLOCK-T644', images_in_sequence=1, image_name='MC_O_20251124_000100', image_index=1, image_source='MC', image_controller='O', image_date='20251124', image_number=100, timestamp_acquisition_start=1764038100.6716127, requested_exposure_time=30.0, timestamp_end_of_readout=1764038140.1770334)
    INFO:shared.metrics.s3_metrics:MC_O_20251124_000100 Summit to USDF transfer time: 4.31 seconds
    INFO:shared.metrics.s3_metrics:MC_O_20251124_000100 end readout timestamp: 2025-11-25 02:35:03.177033+00:00
    INFO:shared.metrics.s3_metrics:MC_O_20251124_000100 newest S3 file timestamp: 2025-11-25 02:35:07.491000+00:00
    INFO:shared.s3_client:found LSSTCam/20251124/MC_O_20251124_000100/MC_O_20251124_000100_expectedSensors.json expected sensors file


Using Data Transfer Monitoring Metrics in Queries and Dashboards
================================================================

The ``day`` label was added to Prometheus metrics for filtering metrics by observation day.  To filter metrics use the day label with the day in ``YYYY-MM-DD`` format. An example query is ``dtm_file_messages_received_total{day="2025-11-22"}``

Enable Debug Logs
=================
To enable debug log change the ``DEBUG_LOGS`` environment label from ``false`` to ``true``.

Changing Late File Time Parameter
=================================
The ``MAX_FILE_LATE_TIME`` value defines what threshold late files are identified.  Change this value in the Data Transfer Monitoring Kubernetes deployment manifest for a different threshold.
