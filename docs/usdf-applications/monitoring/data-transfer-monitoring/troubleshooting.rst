###############
Troubleshooting
###############

Intended audience: Anyone who is administering Data Transfer Monitoring.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - File Counts are not accurate
     - The Summit will resend files if USDF Ceph S3 is not responsive causing duplicate file notifications for the same file.
     - See :ref:`Calculate_File_Counts`
   * - Negative Time File transfers
     - End Readout Messages Timestamps for ``DARK LSSTCamcheckout`` images are after the file transfers
     - No known work around.  It could be investigated to exclude these from file transfer calculations.

Monitoring
==========
.. Describe how to monitor application and include relevant links.

See :ref:`DTM_Overview` for links to the dashboard.

.. Template to use for troubleshooting

Metrics not Displaying
======================

**Symptoms:**  Metrics are not getting displayed in Grafana.

**Cause:** The scrape settings or port settings could have been modified or removed.

**Solution:** Validate the following is set on the pod.  If not update the deployment manifest.


.. rst-class:: technote-wide-content

.. code-block:: yaml

    metadata:
      annotations:
        prometheus.io/port: "8000"
        prometheus.io/scrape: "true"
