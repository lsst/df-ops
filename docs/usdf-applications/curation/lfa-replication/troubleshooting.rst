###############
Troubleshooting
###############

Intended audience: Anyone who is administering Large File Annex replication.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - Summit overwrites
     - Occasionally, an LFA object at the Summit will be overwritten.
       This violates requirements and interface specifications, but it does happen, particularly with the All Sky Camera and the sequence summaries published as part of control system scripts.
       The USDF bucket has S3 versioning enabled and the mirror runs with ``--overwrite`` (set through ``MINIO_OPTIONS`` in the deployment), so the newer Summit object replaces the USDF copy automatically and the older copy is kept as a noncurrent version.
       Overwrites therefore no longer show up as "Failed to perform mirroring, with error condition" errors in the monitoring dashboard; if that error does appear, it has some other cause and needs investigation.
       Noncurrent versions are not expired automatically.
     - No action is needed for an overwrite.
       To retrieve an older version of an object, use the AWS CLI container described under "Command line" in :doc:`../../../users/object-store`, with credentials for the USDF LFA bucket (Vault ``secret/rubin/usdf-lfa``).
       List the versions with ``s3api list-object-versions --bucket rubinobs-lfa-cp --prefix <key>``, then fetch the one wanted with ``s3api get-object --bucket rubinobs-lfa-cp --key <key> --version-id <id> <outfile>``.
       (``mc ls --versions`` currently fails against ``s3dfrgw`` with "unrecognized option:Tenant".)
       Objects written before versioning was enabled have the version ID ``null``.
       Older copies moved to an ``overwrite/`` pathname by the former manual procedure remain at that location.

Monitoring
==========
.. Describe how to monitor application and include relevant links.

Monitoring dashboard: https://grafana.slac.stanford.edu/d/c0382eb5-99c0-46fd-8d63-c5743836d4cb/usdf-large-file-annex-lfa-transfer-overview?orgId=1

.. Template to use for troubleshooting

Sample Troubleshooting
======================

**Symptoms:**

**Cause:**

**Solution:**
