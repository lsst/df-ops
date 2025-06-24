###########################
Troubleshooting MPC Sandbox
###########################

Intended audience: Anyone who is administering the MPC replica.

Monitoring
==========

Known Issues
============
Replication commands do not work through PgBouncer.   Please note this in the future if new connections are made for replication.

Replication is broken
=====================

**Symptoms:** There are alerts in ops-usdf-alert channel for replication slot is missing or replication is failing.  A user could notice that is not new data
for observations.

**Cause:**  An extended SLAC outage or network interruption can cause the replica to lose its place in the replication slot.  If the schema changes at the publication and is not updated
on the subscription.

**Solution:** :doc:`fix-replication`


