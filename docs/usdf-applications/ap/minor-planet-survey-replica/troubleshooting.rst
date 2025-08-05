###############
Troubleshooting
###############

Intended audience: Anyone who is administering the Minor Planet Survey Replica.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - Logical Replication with Pooler
     - Logical Replication do not work though the pooler.  The pooler cannot process the replication commands.
     - Configure Kubernetes Service to connect directly to the database.  Poolers can still be configured for application and user connections to the database.  Replication commands do not work through PgBouncer.   Please note this in the future if new connections are made for replication.


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

**Solution:** See :doc:`check-replication` to review for lag.  Follow :doc:`build-mpcorb-replica` to rebuild.

Replication Slot Already in Use
===============================
**Symptoms:** Replication slot already in use error when trying to rebuild subscription

**Cause:**  It can happen if the database crashes or if the slot name is still active on the publication after the subscription.

**Solution:**  For the MPC Annex login to the MPC annex.  The connection info can be found from the subscription.  Enter the below commands to drop the replication slot.

.. rst-class:: technote-wide-content

.. code-block:: sql

   SELECT pg_drop_replication_slot('sbn146_rubin_usdf_obs_table_sub');
   SELECT pg_drop_replication_slot('sbn146_rubin_usdf_other_tables_sub');

For the USDF access the Minor Planet Survey replica at the USDF.  Enter the below command to drop the replication slot.

.. rst-class:: technote-wide-content

.. code-block:: sql

   SELECT pg_drop_replication_slot('epo_dev_slot1');

Schema Mismatch
===============
**Symptoms:** There are logs for schema mismatches.

**Cause:**  A change at the schema at the MPC Annex such as adding a column or changing the name of column will cause replication to stop.  There are emails from Andrei at the MPC Annex when this happens.

**Solution:** Follow :ref:`minor_planet_survey_schema_updates`

