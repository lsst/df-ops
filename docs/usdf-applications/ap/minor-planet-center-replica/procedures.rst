##########
Procedures
##########

Intended audience: Anyone who is administering the Minor Planet Survey Database replica.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployments are done with a `Makefile <https://github.com/slaclab/rubin-usdf-minor-planet-survey/blob/main/kubernetes/overlays/prod/Makefile>`__  ``make run-apply`` will apply the configuration.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

For maintenance coordinate with the #dm-ssp Slack channel for when downtime is needed for maintenance.

Backup
======
.. Procedures for backup including how to verify backups.

The MPCorb replica is not backed up because data is replicated from the MPC.  The restore
process is detailed in :doc:`build-mpcorb-replica`

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

The service should not be reproduced.  Rubin is limited to one subscriber with the MPC annex.

Rebuild Subscriptions
=====================
The following details how to rebuild the Obs Table and Other Tables Subscriptions that are replicated from the MPC Annex.

Rebuild Subscription - Obs Table Subscription
------------------------------------------------
To rebuild run the following.
 #. Connect to the ``mpc_sbn`` database with ``\c mpc_sbn``
 #. If the replication slot is missing or does not exist an error like this will be in the alerts or logs ``replication slot sbn146_rubin_usdf_obs_table_sub does not exist``.  Disable and drop the ``sbn146_rubin_usdf_obs_table_sub``  subscription.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

        ALTER SUBSCRIPTION sbn146_rubin_usdf_obs_table_sub DISABLE;
        ALTER SUBSCRIPTION sbn146_rubin_usdf_obs_table_sub SET (slot_name=NONE);
        DROP SUBSCRIPTION sbn146_rubin_usdf_obs_table_sub;

    If the message is not ``replication slot does not exist`` the replication slot still exists on the MPC and needs to be deleted.  An example of a message is ``This slot has been invalidated because it exceeded the maximum reserved size``.  Run the below omitting the line with ``slot_name=NONE``

    .. rst-class:: technote-wide-content

    .. code-block:: sql

        ALTER SUBSCRIPTION sbn146_rubin_usdf_obs_table_sub DISABLE;
        DROP SUBSCRIPTION sbn146_rubin_usdf_obs_table_sub;

 #. Truncate the Other Tables.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       TRUNCATE TABLE obs_sbn;

 #. Create the subscriptions.  Replace with the password from Vault.  Validate in logs there are not duplicate keys or replication errors.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       CREATE SUBSCRIPTION sbn146_rubin_usdf_obs_table_sub CONNECTION 'host=sbn-am-aurora16-db.cluster-c1t4y1fwdvea.us-east-2.rds.amazonaws.com port=5432 dbname=mpc_sbn user=sbnmastrubin password=<update>' PUBLICATION sbn146_obs_table_pub;

Rebuild Subscription - Other Tables Subscription
------------------------------------------------
To rebuild run the following.
 #. Connect to the ``mpc_sbn`` database with ``\c mpc_sbn``
 #. If the replication slot is missing or does not exist an error like this will be in the alerts or logs ``replication slot sbn146_rubin_usdf_other_tables_sub does not exist``.  Disable and drop the ``sbn146_rubin_usdf_other_tables_sub``  subscription.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

        ALTER SUBSCRIPTION sbn146_rubin_usdf_other_tables_sub DISABLE;
        ALTER SUBSCRIPTION sbn146_rubin_usdf_other_tables_sub SET (slot_name=NONE);
        DROP SUBSCRIPTION sbn146_rubin_usdf_other_tables_sub;

    If the message is not ``replication slot does not exist`` the replication slot still exists on the MPC and needs to be deleted.  An example of a message is ``This slot has been invalidated because it exceeded the maximum reserved size``.  Run the below omitting the line with ``slot_name=NONE``

    .. rst-class:: technote-wide-content

    .. code-block:: sql

        ALTER SUBSCRIPTION sbn146_rubin_usdf_other_tables_sub DISABLE;
        DROP SUBSCRIPTION sbn146_rubin_usdf_other_tables_sub;

 #. Truncate the Other Tables.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       TRUNCATE TABLE current_identifications, minor_planet_names, mpc_orbits, neocp_els, neocp_events, neocp_obs, neocp_obs_archive, neocp_prev_des, neocp_var, numbered_identifications, obs_alterations_corrections, obs_alterations_deletions, obs_alterations_redesignations, obs_alterations_unassociations, obscodes, primary_objects;

 #. Create the subscriptions.  Replace with the password from Vault.  Validate in logs there are not duplicate keys or replication errors.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       CREATE SUBSCRIPTION sbn146_rubin_usdf_other_tables_sub CONNECTION 'host=sbn-am-aurora16-db.cluster-c1t4y1fwdvea.us-east-2.rds.amazonaws.com port=5432 dbname=mpc_sbn user=sbnmastrubin password=<update>' PUBLICATION sbn146_other_tables_pub;

Rebuild Replicas
================
See :doc:`build-mpcorb-replica`

.. _minor_planet_survey_schema_updates:

Schema Updates
==============
Schema updates will come in email from Andrei at the MPC Annex.  Perform the following to update schemas.
 #. Add the SQL to the `SQL directory of the GitHub repo <https://github.com/slaclab/rubin-usdf-minor-planet-survey/tree/main/kubernetes/overlays/prod/sql>`__
 #. Add the command to apply the schema to :doc:`build-mpcorb-replica` and commit the changes to the repo.  These changes will also be used by EPO.
 #. Inform Eric Rosas and Jared Trouth on the *ops-df-databases* database Slack Channel.
 #. Once confirmed the changes are applied at EPO refresh the USDF publications with below.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       ALTER SUBSCRIPTION sbn146_rubin_usdf_obs_table_sub REFRESH PUBLICATION;
       ALTER SUBSCRIPTION sbn146_rubin_usdf_other_tables_sub REFRESH PUBLICATION;
 #.  Instruct EPO to refresh their subscriptions in Google Cloud.  Validate there are no schema mismatches in the log.


Configure Publication for EPO
=============================
Below is the configuration of the publication for EPO.  Additional tables can be added with the ``ALTER PUBLICATION ADD TABLE`` command.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

         CREATE PUBLICATION epo FOR TABLE current_identifications;

         ALTER PUBLICATION epo ADD TABLE mpc_orbits;
         ALTER PUBLICATION epo ADD TABLE neocp_els;
         ALTER PUBLICATION epo ADD TABLE neocp_events;
         ALTER PUBLICATION epo ADD TABLE neocp_obs;
         ALTER PUBLICATION epo ADD TABLE neocp_obs_archive;
         ALTER PUBLICATION epo ADD TABLE neocp_prev_des;
         ALTER PUBLICATION epo ADD TABLE neocp_var;
         ALTER PUBLICATION epo ADD TABLE numbered_identifications;
         ALTER PUBLICATION epo ADD TABLE obs_alterations_corrections;
         ALTER PUBLICATION epo ADD TABLE obs_alterations_deletions;
         ALTER PUBLICATION epo ADD TABLE obs_alterations_redesignations;
         ALTER PUBLICATION epo ADD TABLE obs_alterations_unassociations;
         ALTER PUBLICATION epo ADD TABLE obs_sbn;
         ALTER PUBLICATION epo ADD TABLE primary_objects;
         ALTER PUBLICATION epo ADD TABLE minor_planet_names;

Also update the grants for EPO for the corresponding table.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

         CREATE USER epo with PASSWORD '<replace with password from vault>';

         ALTER ROLE epo REPLICATION;

         GRANT SELECT ON public.current_identifications TO epo;
         GRANT SELECT ON public.mpc_orbits  TO epo;
         GRANT SELECT ON public.neocp_els TO epo;
         GRANT SELECT ON public.neocp_events TO epo;
         GRANT SELECT ON public.neocp_obs TO epo;
         GRANT SELECT ON public.neocp_obs_archive TO epo;
         GRANT SELECT ON public.neocp_prev_des TO epo;
         GRANT SELECT ON public.neocp_var TO epo;
         GRANT SELECT ON public.numbered_identifications TO epo;
         GRANT SELECT ON public.obs_alterations_corrections TO epo;
         GRANT SELECT ON public.obs_alterations_deletions TO epo;
         GRANT SELECT ON public.obs_alterations_redesignations TO epo;
         GRANT SELECT ON public.obs_alterations_unassociations TO epo;
         GRANT SELECT ON public.obs_sbn TO epo;
         GRANT SELECT ON public.primary_objects TO epo;
         GRANT SELECT ON public.minor_planet_names TO epo;


Obs Table Validation
====================

Run the below query to validate the obs_table.

To validate data is in subscriptions run the below to validate data in the ``obs_sbn`` table.

.. rst-class:: technote-wide-content

.. code-block:: sql

   SELECT pg_size_pretty(pg_relation_size('obs_sbn'));


Update IP Addresses for EPO Access
==================================
Access to the USDF Minor Planet Survey Data replica is limited by IP Address.  Perform the following to update IP Addresses.

#. Modify the `db-svc-gcp.yaml <https://github.com/slaclab/rubin-usdf-minor-planet-survey/blob/main/kubernetes/overlays/prod/db-svc-gcp.yaml>`__ Kubernetes Load Balancer Service.  Note that is not setup as Pooler because replication commands are not supported through a Pooler.
#. EPO has static IP addresses defined in Cloud NAT.  If there was a change or new project add the IP Address under ``loadBalancerSourceRanges``.
#.  Apply the changes and commit to GitHub.
