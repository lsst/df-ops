###############
Troubleshooting
###############

Intended audience: Anyone who is administering the Summit Database Replica.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - Replication Slots are not replicated at the Summit
     - This is due to a limitation of Postgres 14. Slots are replicated in Postgres 17.  Pending work to validate Postgres 17 at the USDF.
     - Follow the rebuild subscription procedures.

Monitoring
==========
.. Describe how to monitor application and include relevant links.

The CNPG Postgres Dashboard in Grafana is used for monitoring.

.. Template to use for troubleshooting

Replication Slot Issues
=======================
**Symptoms:** There are alerts in ops-usdf-alert channel for replication slot is missing or replication is failing.  A user could notice that is not new data
for observations.

**Cause:**  An extended SLAC outage or network interruption can cause the replica to lose its place in the replication slot.  If the schema changes at the publication and is not updated
on the subscription.

**Solution:** Follow rebuild subscription steps in procedures page.  Check status using queries in :doc:`replication-issues`. If a replication slot needs to be dropped follow the Drop Replication Slot procedure.

Schema Mismatch
===============
**Symptoms:** There are logs for schema mismatches.

**Cause:**  A change at the schema at the Summit such as adding a column or changing the name of column will cause replication to stop.

**Solution:** Follow the schema update procedures.
