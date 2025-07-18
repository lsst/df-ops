######################
MPC Replica Procedures
######################

Intended audience: Anyone who is administering the MPC replica.

Scheduled Maintenance
=====================

Upgrades and Rollback
=====================

Update Schema
=============

Rebuild MPC Replica
===================

To update schemas obtain the changes from SBN run the script file manally. CNPG runs script as a one time bootstrap so that is why it must be manual. Example below.

.. rst-class:: technote-wide-content

.. code-block:: bash

  cat create_mpc_sbn146_all_tables_schemas.sql | k exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
  cat create_mpc_sbn_obs_alterations_tables_schemas.sql |k exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
  cat create_table_mpc_orbits.sql | | k exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
  cat mpc_orbits_add_new_columns_and_comments.sql | k exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
  cat mpc_sbn_add_new_columns_to_obs_sbn_table.sql | k exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
  cat obscodes.sql | k exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
  cat minor_planet_names.sql | k exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
  cat grants.sql | | k exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn


Backup
======

The MPCorb replica is not backed up because data is replicated from the MPC.  The restore
process is detailed in :doc:`rebuild-mpcorb-replica`

Reproduce Service
=================

Disaster Recovery
=================

Security Incident Response
==========================

The main risk is that the replication password is compromised.  If the password is compromised contact the Minor Planet Center and to reset the password.

