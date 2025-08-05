:orphan:

#########################
Validate MPC Sandbox Data
#########################


View Subscriptions
------------------

To validate data is in subscriptions run the below to see if data is in the subscriptions.

.. rst-class:: technote-wide-content

.. code-block:: sql

   select count(*) from obs_ingest;
   select count(*) from obs_sbn;
   select count(*) from mpc_orbits;
