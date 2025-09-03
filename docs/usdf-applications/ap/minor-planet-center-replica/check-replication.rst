:orphan:

#################
Check Replication
#################

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

  select slot_name, active  from pg_replication_slots WHERE slot_name LIKE '%rubin_usdf%';

To check the status of replication this query can be run from the publication instance at MPC.  Running the command multiple times with time in between will show how if the data behind is growing.

.. rst-class:: technote-wide-content

.. code-block:: sql

    SELECT redo_lsn, slot_name,restart_lsn,
    round((redo_lsn-restart_lsn) / 1024 / 1024 / 1024, 2) AS GB_behind
    FROM pg_control_checkpoint(), pg_replication_slots WHERE slot_name LIKE '%rubin%';

To check for replication lag from the publication instance at MPC.

.. rst-class:: technote-wide-content

.. code-block:: sql

    select application_name, client_addr, state, write_lag, flush_lag, replay_lag from pg_stat_replication WHERE application_name LIKE '%rubin%';

The below query shows what the latest observation day that is replicated.

.. rst-class:: technote-wide-content

.. code-block:: sql

   select max(updated_at) from current_identifications;