###############
Troubleshooting
###############

Intended audience: Anyone who is administering the MPC Sandbox.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * -
     -
     -

Monitoring
==========
.. Describe how to monitor application and include relevant links.

The CNPG dashboard in Grafana.

Replication is broken
=====================

**Symptoms:** There are alerts in ops-usdf-alert channel for replication slot is missing or replication is failing.  A user could notice that is not new data
for observations.

**Cause:**  An extended SLAC outage or network interruption can cause the replica to lose its place in the replication slot.  If the schema changes at the publication and is not updated
on the subscription.

**Solution:** To review issues :doc:`check-replication` and :doc:`validate-data`

Follow :doc:`build-mpc-sandbox-replica` to rebuild the replica.
