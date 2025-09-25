###############
Troubleshooting
###############

Intended audience: Anyone who is administering S3 File Notifications Kafka.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - S3 Notification Config not changing
     - When changing file notifications in Ceph a blank configuration needs to be applied to overwrite what is there.
     - See :ref:`Creating_File_Notifications` procedure to apply a blank configuration
   * - File Notifications configured but not sending notifications
     - There was corruption with Kafka notifications in the production Embargo Ceph Cluster.  Unclear why this happens.
     - Do not use ``persistent:true``.  Naming the topic a new name that has not been used before.

Monitoring
==========
.. Describe how to monitor application and include relevant links.

.. Template to use for troubleshooting

Identify if Kafka events are being created
==========================================

**Symptoms:** New file notification events are not being created.  Prompt Processing may time out because the file notification did not arrive.

**Cause:** The file notifications in Ceph are not working.

**Solution:**  :ref:`View_Prompt_Kafdrop_Messages` and re-create File Notifications using the :ref:`Creating_File_Notifications` procedure.
