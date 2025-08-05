##########
Procedures
##########

Intended audience: Anyone who is administering the MPC Sandbox.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployments are done with a `Makefile <https://github.com/slaclab/rubin-usdf-minor-planet-survey/blob/main/kubernetes/overlays/mpc-sandbox-prod/Makefile>`__  ``make run-apply`` will apply the configuration.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

Backup
======
.. Procedures for backup including how to verify backups.

The MPC Sandbox is not backed up because data is replicated from the Minor Planet Center.  The restore
process is detailed in :doc:`build-mpc-sandbox-replica`

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

No specific cold startup procedures needed.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No specific cold shutdown procedures needed.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

Refresh the Subscriptions
=========================

To refresh subscriptions after tables updates run.

.. rst-class:: technote-wide-content

.. code-block:: bash

   ALTER SUBSCRIPTION usdf_mpc_obs_ingest_sub REFRESH PUBLICATION;
   ALTER SUBSCRIPTION usdf_mpc_obs_sbn_sub REFRESH PUBLICATION;
   ALTER SUBSCRIPTION usdf_mpc_orbits_sub REFRESH PUBLICATION;

Drop all Subscriptions
======================

To drop all subscriptions run the below commands.

.. rst-class:: technote-wide-content

.. code-block:: bash

   DROP SUBSCRIPTION usdf_mpc_obs_ingest_sub;
   DROP SUBSCRIPTION usdf_mpc_obs_sbn_sub;
   DROP SUBSCRIPTION usdf_mpc_orbits_sub;