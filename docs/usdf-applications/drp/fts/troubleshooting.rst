###############
Troubleshooting
###############

Intended audience: Anyone who is administering FTS.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - Many transfers stuck in ``ACTIVE`` state
     - Transfers are stuck in ``ACTIVE`` state for long periods of time, with no new transfers.
     - Cancel all ``ACTIVE`` jobs
   * - No transfer updates
     - Transfers are not getting updates
     - Temporary work around: disable MariaDB operator reconciliation, set primary back to read_only false

Monitoring
==========
.. Describe how to monitor application and include relevant links.

* USDF FTS Monitoring: https://usdf-fts3.slac.stanford.edu:8449/fts3/ftsmon/#/
* RAL FTS Monitoring: https://lcgfts3.gridpp.rl.ac.uk:8449/fts3/ftsmon/#/
* Rucio Transfer Monitoring: https://grafana.slac.stanford.edu/d/YVcucApIk/rucio-transfer-monitoring

.. Template to use for troubleshooting

Transfers stuck in ``ACTIVE`` state
===================================

**Symptoms:**
Many FTS transfers have been stuck in ``ACTIVE`` state. FTS Pod does not have any ``fts_url_copy`` processes running.

**Cause:**
We have set the ``MaxURLCopyProcesses`` configuration in the FTS Pod to prevent FTS from being overloaded by transfer requests. This error seems to occurs when the number of ``ACTIVE`` tranfers FTS sees in the database exceeds the ``MaxURLCopyProcesses``. This results in the pod crashing and restarting.

**Solution:**
The current solution is to cancel all of the ``ACTIVE`` jobs. If Rucio is submitting transfers, Rucio will retry the cancelled transfers.

No updates on transfers
=======================

**Symptoms:**
FTS transfers are stuck in submitting or active.

**Cause:**
The MariaDB operator is attempting to reconcile replicas; however, there are reconciliation issues. This causes the primary database to be read-only, which prevents fts from updating transfer statuses.

**Solution:**
A plan is being tested to move from a replicated MariaDB deployment to a single instance deployment.
