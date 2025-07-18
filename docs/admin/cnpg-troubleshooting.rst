############################################
Cloud Native Postgres (CNPG) Troubleshooting
############################################

Intended audience: Anyone who is administering application infrastructure at the USDF.

Known Issues
============

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - Logical Replication with Pooler
     - Logical Replication do not work though the pooler.  The pooler cannot process the replication commands.
     - Configure Kubernetes Service to connect directly to the database.  Poolers can still be configured for application and user connections to the database.

Identifying Blocked Transactions
================================

**Symptoms:**  Blocked transactions will show in the CNPG dashboard or there will be performance issues reported.

**Cause:** There can be a wide range of causes.

**Solution:**  Run the below query to identify the transactions.   Note the results ``blocked_by`` will show the ``pid`` that is blocking

.. rst-class:: technote-wide-content

.. code-block:: sql

    SELECT
        pid,
        usename,
        pg_blocking_pids(pid) AS blocked_by,
        query AS blocked_query
    FROM
        pg_stat_activity
    WHERE
        cardinality(pg_blocking_pids(pid)) > 0;

To find the ``pid`` use below replacing the pid value.

.. rst-class:: technote-wide-content

.. code-block:: sql

   select * from pg_stat_activity WHERE pid = replace;

For locks reference the `postgres Wiki <https://wiki.postgresql.org/wiki/Lock_Monitoring>`__ on locks.

Identifying Long Transactions
=============================

**Symptoms:**  Long running transactions will show in the CNPG dashboard or there will be performance issues reported with transactions not finishing.

**Cause:** There can be a wide range of causes from a suboptimal query to database congestion.

**Solution:**  Run the below query to identify the transaction.  Adjust the ``interval`` lower or higher depending on the issue.

.. rst-class:: technote-wide-content

.. code-block:: sql

    SELECT datname, usename, now() - xact_start AS xact_duration, query
    FROM pg_stat_activity
    WHERE xact_start IS NOT NULL  -- Filter for transactions
    AND (now() - xact_start) > interval '5 minutes'  -- Adjust duration as needed
    ORDER BY xact_start;

Vacuum Not Running
==================

**Symptoms:**  Performance issues or database not being cleaned up.

**Cause:** Other operations could impact vacuum running or the settings for autovacuum may not be configured appropriately.

**Solution:**  To see when autovacuum was last run connect to the relevant database then run below.

.. rst-class:: technote-wide-content

.. code-block:: sql

   SELECT relname, last_vacuum, last_autovacuum FROM pg_stat_user_tables;

This `article <https://www.datadoghq.com/blog/postgresql-vacuum-monitoring/>`__ discusses how to troubleshoot autovacuum.

Replica Not Syncing
===================

**Symptoms:**  The pod logs on the standby will show that WALS are missing.

**Cause:** This can be caused by network issues.

**Solution:** Resize the cluster.  Set the number of instances to 1 by editing the running database cluster configuration.  Once the replica is gone set the instances back to 2 and observe the rebuild.  If there are more than 2 running instances the same logic applies.

Replica Pod Not Healthy
=======================

**Symptoms:**  The Cluster will show as unhealthy and/or a pod will not be running.

**Cause:** Database replicas can fail due to losing connectivity with the primary instance or not being able to replay a WAL file.

**Solution:**  To rebuild an instance you can first try deleting the affected pod.  If that does not work the instance can be deleted with the destroy option with CNPG kubectl plugin.  Perform this with caution as you can destroy the cluster if you do not enter an instance name or all running instances.  To perform this find the selected failed instance then run

.. rst-class:: technote-wide-content

.. code-block:: bash

   kubectl cnpg destroy <name of cluster> <instance id> -n <namespace>

The instance id is the -number  at the end of the pod name.  For example in the output below the primary instance is 2 and standby instance is 1.

.. rst-class:: technote-wide-content

.. code-block:: text

    Instances status
    Name            Database Size  Current LSN    Replication role  Status  QoS        Manager Version  Node
    ----            -------------  -----------    ----------------  ------  ---        ---------------  ----
    usdf-butler3-2  1339 GB        1616/81000000  Primary           OK      Burstable  1.21.1           sdfk8sn003
    usdf-butler3-1  1339 GB        1616/81000000  Standby (async)   OK      Burstable  1.21.1           sdfk8sn006
