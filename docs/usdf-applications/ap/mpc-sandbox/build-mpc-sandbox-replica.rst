:orphan:

#################
Build MPC Sandbox
#################

To build the replica run the following.

#. Connect to the ``mpc_obs_sandbox`` database with ``\c mpc_obs_sandbox;``
#. Prepare the schemas

   .. rst-class:: technote-wide-content

   .. code-block:: bash

      cat obs_ingest.sql | kubectl exec -it mpc-sandbox-prod-2 -n mpc-sandbox-prod -- psql -d mpc_obs_sandbox
      cat orbit_table_scripts.sql | kubectl exec -it mpc-sandbox-prod-2 -n mpc-sandbox-prod -- psql -d mpc_obs_sandbox
      cat obs_obit_data.sql | kubectl exec -it mpc-sandbox-prod-2 -n mpc-sandbox-prod -- psql -d mpc_obs_sandbox
      cat obs_sbn.sql | kubectl exec -it mpc-sandbox-prod-2 -n mpc-sandbox-prod -- psql -d mpc_obs_sandbox
      cat mpc_orbits.sql | kubectl exec -it mpc-sandbox-prod-2 -n mpc-sandbox-prod -- psql -d mpc_obs_sandbox


 #. Create the subscriptions.  Replace with the password from Vault.  Validate in logs there are not duplicate keys or replication errors.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       CREATE SUBSCRIPTION usdf_mpc_obs_ingest_sub CONNECTION 'host=mpc-pipeline-dev-sandbox-cluster.cuee8irghiva.us-east-2.rds.amazonaws.com port=5432 dbname=mpc_obs_sandbox user=mpc_lsst_user password=<update>' PUBLICATION mpc_lsst_sandbox_obs_ingest_pub;

       CREATE SUBSCRIPTION usdf_mpc_obs_sbn_sub CONNECTION 'host=mpc-pipeline-dev-sandbox-cluster.cuee8irghiva.us-east-2.rds.amazonaws.com port=5432 dbname=mpc_obs_sandbox user=mpc_lsst_user password=<update>' PUBLICATION mpc_lsst_sandbox_obs_sbn_pub;

       CREATE SUBSCRIPTION usdf_mpc_orbits_sub CONNECTION 'host=mpc-pipeline-dev-sandbox-cluster.cuee8irghiva.us-east-2.rds.amazonaws.com port=5432 dbname=mpc_obs_sandbox user=mpc_lsst_user password=<update>' PUBLICATION mpc_lsst_sandbox_mpc_orbits_pub;;




