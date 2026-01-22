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
       Overwrites show up as "Failed to perform mirroring, with error condition" errors in the monitoring dashboard.
       Since these errors are not fatal and still allow other files to be mirrored, they do not need to be addressed right away.
       However, they do need to be addressed before the original object expires from the Summit bucket.
     - The current manual workaround procedure is to move the older version of the object mentioned in the error message (e.g. ``https://s3dfrgw.slac.stanford.edu/rubinobs-lfa-cp/AllSkyCamera/2025/12/16/asc2512160033.jpg``) to another pathname that doesn't conflict with the newer version that will be mirrored from the Summit.
       In this particular case, ``mc mv lfa-w/rubinobs-lfa-cp/AllSkyCamera/2025/12/16/asc2512160033.jpg lfa-w/rubinobs-lfa-cp/AllSkyCamera/2025/12/16/overwrite/asc2512160033.jpg`` can be used, where ``lfa-w`` refers to the appropriate credentials for writing the LFA bucket at ``s3dfrgw``.

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
