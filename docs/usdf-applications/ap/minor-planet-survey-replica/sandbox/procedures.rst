######################
MPC Sandbox Procedures
######################

Intended audience: Anyone who is administering the MPC replica.

Update Schema
=============

Rebuild MPC Sandbox
===================

To update schemas obtain the changes from SBN run the script file manally. CNPG runs script as a one time bootstrap so that is why it must be manual. Example below.

.. rst-class:: technote-wide-content

.. code-block:: bash

cat obs_ingest.sql | kubectl exec -it mpc-sandbox-prod-2 -n mpc-sandbox-prod -- psql -d mpc_obs_sandbox
cat orbit_table_scripts.sql | kubectl exec -it mpc-sandbox-prod-2 -n mpc-sandbox-prod -- psql -d mpc_obs_sandbox
cat obs_obit_data.sql | kubectl exec -it mpc-sandbox-prod-2 -n mpc-sandbox-prod -- psql -d mpc_obs_sandbox
cat obs_sbn.sql | kubectl exec -it mpc-sandbox-prod-2 -n mpc-sandbox-prod -- psql -d mpc_obs_sandbox
cat mpc_orbits.sql | kubectl exec -it mpc-sandbox-prod-2 -n mpc-sandbox-prod -- psql -d mpc_obs_sandbox


Backup
======

Reproduce Service
=================

Disaster Recovery
=================

