###############
Troubleshooting
###############

Intended audience: Anyone who is administering OpenSearch.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - Upgrades blocked and version locked at OpenSearch 2.16.
     - Upgrades were tried, but failed because OpenSearch checks all the certificates running on the system for any that are expired.  There were some expired host certificates so running OpenSearch failed and the upgrade had to be reverted.
     - The only known workaround is to ensure all host certificates are not expired (including the certificates not used by OpenSearch), but is a risky to maintain.  There is an open issue and discussion with OpenSearch to hopefully resolve the requirement.

Monitoring
==========
.. Describe how to monitor application and include relevant links.

.. Template to use for troubleshooting

Sample Troubleshooting
======================

**Symptoms:**

**Cause:**

**Solution:**
