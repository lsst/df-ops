:orphan:

################################
Troubleshoot Logical Replication
################################

View Subscriptions
------------------

To view the logical replication subscriptions at the USDF run the below queries.

.. rst-class:: technote-wide-content

.. code-block:: sql

   select * from pg_subscription;

To see all output or to reduce the output.

.. rst-class:: technote-wide-content

.. code-block:: sql

   select subname, subowner, subenabled, subslotname, subpublications, suborigin from pg_subscription;


View Status from Publication
----------------------------

To view the status of replication slots.

.. rst-class:: technote-wide-content

.. code-block:: sql

  select slot_name, active  from pg_replication_slots;

To check the status of replication this query can be run from the publication instance at the Summit.  Running the command multiple times with time in between will show how if the data behind is growing.

.. rst-class:: technote-wide-content

.. code-block:: sql

    SELECT redo_lsn, slot_name,restart_lsn,
    round((redo_lsn-restart_lsn) / 1024 / 1024 / 1024, 2) AS GB_behind
    FROM pg_control_checkpoint(), pg_replication_slots;

To check for replication lag from the publication instance at the Summit.

.. rst-class:: technote-wide-content

.. code-block:: sql

    select application_name, client_addr, state, write_lag, flush_lag, replay_lag from pg_stat_replication;

The below query looks for log delay in replication.

.. rst-class:: technote-wide-content

.. code-block:: sql

   SELECT CASE WHEN pg_last_wal_receive_lsn() = pg_last_wal_replay_lsn() THEN '0 seconds'::interval
   ELSE age(now(),pg_last_xact_replay_timestamp()) END AS log_delay;

Viewing Last Observation Day
----------------------------

To query for the last observation run ``select max(day_obs) from cdb_lsstcam.exposure;``  The result should show the previous day.  Example output is below.

.. rst-class:: technote-wide-content

.. code-block:: sql

   exposurelog=# select max(day_obs) from cdb_lsstcam.exposure;
      max
   ----------
   20241125
   (1 row)