:orphan:

####################
Build MPCorb Replica
####################

To build the replica run the following.
 #. Connect to the ``mpc_sbn`` database with ``\c mpc_sbn;``
 #. Prepare the schemas

    .. rst-class:: technote-wide-content

    .. code-block:: bash

       cat create_mpc_sbn146_all_tables_schemas.sql | kubectl exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
       cat create_mpc_sbn_obs_alterations_tables_schemas.sql | kubectl exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
       cat create_table_mpc_orbits.sql | kubectl exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
       cat mpc_orbits_add_new_columns_and_comments.sql | kubectl exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
       cat mpc_sbn_add_new_columns_to_obs_sbn_table.sql | kubectl exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
       cat obscodes.sql | kubectl exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
       cat minor_planet_names.sql | kubectl exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn
       cat grants.sql | kubectl exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn

 #. If there is an error ``NOTICE:  table "obs_alterations_unassociations" does not exist, skipping`` reported re-apply with below.

    .. rst-class:: technote-wide-content

    .. code-block:: bash

       cat create_mpc_sbn_obs_alterations_tables_schemas.sql | kubectl exec -it mpcorb-1 -n mpcorb-replica -- psql -d mpc_sbn

 #. Create the subscriptions.  Replace with the password from Vault.  Validate in logs there are not duplicate keys or replication errors.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       CREATE SUBSCRIPTION sbn146_rubin_usdf_other_tables_sub CONNECTION 'host=sbn-am-aurora16-db.cluster-c1t4y1fwdvea.us-east-2.rds.amazonaws.com port=5432 dbname=mpc_sbn user=sbnmastrubin password=<update>' PUBLICATION sbn146_other_tables_pub;

       CREATE SUBSCRIPTION sbn146_rubin_usdf_obs_table_sub CONNECTION 'host=sbn-am-aurora16-db.cluster-c1t4y1fwdvea.us-east-2.rds.amazonaws.com port=5432 dbname=mpc_sbn user=sbnmastrubin password=<update>' PUBLICATION sbn146_obs_table_pub;




