##########
Procedures
##########

Intended audience: Anyone who is administering the Summit Database Replica.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployments are done with the Makefile in the GitHub repo.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

Below are the maintenance tasks that should be performed.
 * Validate backups
 * Review storage growth and PVC size
 * Check resource usage and connections
 * Periodically update the Postgres version to stay current.  Note that with logical replication that the Postgres versions do not have to match between the publication and the subscription.

Communicate on the ``df-announce`` Slack channel when there will be maintenance.

Backup
======
.. Procedures for backup including how to verify backups.

Backups are configured with the CNPG operator.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

Validate replication is active after an outage.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No specific shutdown procedures needed.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

The service cannot be easily reproduced for testing as it would impact connections on the Summit database.

Downloading Summit Postgres schemas
===================================
The below commands can used to download the schemas from the summit.  This can be used for troubleshooting to compare if tables are missing or with schema mismatches.  Tables can also be viewed live with ``replicauser`` account.

.. rst-class:: technote-wide-content

.. code-block:: bash

   pg_dump -s exposurelog -h db-lhn.cp.lsst.org -U replicauser > exposurelog.sql
   pg_dump -s narrativelog -h db-lhn.cp.lsst.org -U replicauser > narrativelog.sql
   pg_dump -s nightreport -h db-lhn.cp.lsst.org -U replicauser > nightreport.sql

Rebuild Subscriptions
=====================
If logical replication loses replication slots on the publisher or there is some other unrecoverable error the tables need to be truncated.  ``TRUNCATE`` keeps the schema while deleting the data.  This will work as long as the schema matches Summit.  The rebuild process differs depending of the type issue.  Below details the process for each subscription.

Rebuild Subscription - Exposurelog and ConsDB
---------------------------------------------
If logical replication loses replication slots on the publisher or there is some other unrecoverable error the tables need to be truncated.  ``TRUNCATE`` keeps the schema while deleting the data.  This will work as long as the schema matches Summit.  The rebuild process differs depending of the type issue.

To rebuild run the following.
 #. Connect to the ``exposurelog`` database with ``\c exposurelog``
 #. If the replication slot is missing or does not exist an error like this will be in the alerts or logs ``replication slot usdf_exposurelog does not exist``.  Disable and drop the exposurelog subscription.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       ALTER SUBSCRIPTION usdf_exposurelog DISABLE;
       ALTER SUBSCRIPTION usdf_exposurelog SET (slot_name=NONE);
       DROP SUBSCRIPTION usdf_exposurelog;

    If the message is not ``replication slot does not exist`` the replication slot still exists on the summit and needs to be deleted.  An example of a message is ``This slot has been invalidated because it exceeded the maximum reserved size`` Run the below omitting the line with ``slot_name=NONE``

    .. rst-class:: technote-wide-content

    .. code-block:: sql

        ALTER SUBSCRIPTION usdf_exposurelog DISABLE;
        DROP SUBSCRIPTION usdf_exposurelog;

 #. Truncate the exposurelog and cdb schemas.

     .. rst-class:: technote-wide-content

     .. code-block:: sql

        TRUNCATE TABLE public.message;
        TRUNCATE TABLE cdb_latiss.ccdexposure, cdb_latiss.ccdexposure_camera, cdb_latiss.ccdexposure_flexdata, cdb_latiss.ccdexposure_flexdata_schema, cdb_latiss.ccdvisit1_quicklook, cdb_latiss.exposure, cdb_latiss.exposure_flexdata, cdb_latiss.exposure_flexdata_schema, cdb_latiss.exposure_quicklook, cdb_latiss.visit1_quicklook;
        TRUNCATE TABLE cdb_lsstcam.ccdexposure, cdb_lsstcam.ccdexposure_camera, cdb_lsstcam.ccdexposure_flexdata, cdb_lsstcam.ccdexposure_flexdata_schema, cdb_lsstcam.ccdexposure_quicklook, cdb_lsstcam.ccdvisit1_quicklook, cdb_lsstcam.exposure, cdb_lsstcam.exposure_flexdata, cdb_lsstcam.exposure_flexdata_schema, cdb_lsstcam.exposure_quicklook, cdb_lsstcam.visit1_quicklook;
        TRUNCATE TABLE cdb_lsstcomcam.ccdexposure, cdb_lsstcomcam.ccdexposure_camera, cdb_lsstcomcam.ccdexposure_flexdata, cdb_lsstcomcam.ccdexposure_flexdata_schema, cdb_lsstcomcam.ccdexposure_quicklook, cdb_lsstcomcam.ccdvisit1_quicklook, cdb_lsstcomcam.exposure, cdb_lsstcomcam.exposure_flexdata, cdb_lsstcomcam.exposure_flexdata_schema, cdb_lsstcomcam.exposure_quicklook, cdb_lsstcomcam.visit1_quicklook;
        TRUNCATE TABLE cdb_lsstcomcamsim.ccdexposure, cdb_lsstcomcamsim.ccdexposure_camera, cdb_lsstcomcamsim.ccdexposure_flexdata, cdb_lsstcomcamsim.ccdexposure_flexdata_schema, cdb_lsstcomcamsim.ccdvisit1_quicklook, cdb_lsstcomcamsim.exposure, cdb_lsstcomcamsim.exposure_flexdata, cdb_lsstcomcamsim.exposure_flexdata_schema, cdb_lsstcomcamsim.visit1_quicklook;
        TRUNCATE TABLE cdb_startrackerfast.exposure, cdb_startrackerfast.exposure_flexdata, cdb_startrackerfast.exposure_flexdata_schema, cdb_startrackerfast.exposure_quicklook;
        TRUNCATE TABLE cdb_startrackernarrow.exposure, cdb_startrackernarrow.exposure_flexdata, cdb_startrackernarrow.exposure_flexdata_schema, cdb_startrackernarrow.exposure_quicklook;
        TRUNCATE TABLE cdb_startrackerwide.exposure, cdb_startrackerwide.exposure_flexdata, cdb_startrackerwide.exposure_flexdata_schema, cdb_startrackerwide.exposure_quicklook;

 #. Create the exposurelog subscription.  Replace with the password from Vault.  Validate in logs there are not duplicate keys or replication errors.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       CREATE SUBSCRIPTION usdf_exposurelog CONNECTION 'host=db-lhn.cp.lsst.org port=5432 dbname=exposurelog user=replicauser password=<REPLACE>' PUBLICATION usdfpub WITH (connect=true);

Rebuild Subscription - Narrativelog
-----------------------------------
To rebuild run the following.
 #. Connect to the ``narrativelog`` database with ``\c narrativelog``
 #. If the replication slot is missing or does not exist an error like this will be in the alerts or logs ``replication slot usdf_narrativelog does not exist``.  Disable and drop the narrativelog subscription.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

        ALTER SUBSCRIPTION usdf_narrativelog DISABLE;
        ALTER SUBSCRIPTION usdf_narrativelog SET (slot_name=NONE);
        DROP SUBSCRIPTION usdf_narrativelog;

    If the message is not ``replication slot does not exist`` the replication slot still exists on the summit and needs to be deleted.  An example of a message is ``This slot has been invalidated because it exceeded the maximum reserved size``.  Run the below omitting the line with ``slot_name=NONE``

    .. rst-class:: technote-wide-content

    .. code-block:: sql

        ALTER SUBSCRIPTION usdf_narrativelog DISABLE;
        DROP SUBSCRIPTION usdf_narrativelog;

 #. Truncate the narrativelog schema.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       TRUNCATE TABLE public.message, jira_fields;

 #. Create the narrativelog subscription.  Replace with the password from Vault.  Validate in logs there are not duplicate keys or replication errors.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       CREATE SUBSCRIPTION usdf_narrativelog CONNECTION 'host=db-lhn.cp.lsst.org port=5432 dbname=narrativelog user=replicauser password=<REPLACE>' PUBLICATION usdfpubnarrativelog WITH (connect=true);

Rebuild Subscription - Nightreport
----------------------------------
To rebuild run the following.
 #. Connect to the ``nightreport`` database with ``\c nightreport``
 #. If the replication slot is missing or does not exist an error like this will be in the alerts or logs ``replication slot usdf_nightreport does not exist``.  Disable and drop the nightreport subscription.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       ALTER SUBSCRIPTION usdf_nightreport DISABLE;
       ALTER SUBSCRIPTION usdf_nightreport SET (slot_name=NONE);
       DROP SUBSCRIPTION usdf_nightreport;

    If the message is not ``replication slot does not exist`` the replication slot still exists on the summit and needs to be deleted.  An example of a message is ``This slot has been invalidated because it exceeded the maximum reserved size``.  Run the below omitting the line with ``slot_name=NONE``

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       ALTER SUBSCRIPTION usdf_nightreport DISABLE;
       DROP SUBSCRIPTION usdf_nightreport;

 #. Truncate the nightreport schemas.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       TRUNCATE TABLE public.nightreport;

 #. Create the usdf_nightreport subscription.  Replace with the password from Vault.  Validate in logs there are not duplicate keys or replication errors.

    .. rst-class:: technote-wide-content

    .. code-block:: sql

       CREATE SUBSCRIPTION usdf_nightreport CONNECTION 'host=db-lhn.cp.lsst.org  port=5432 dbname=nightreport user=replicauser password=<REPLACE>' PUBLICATION usdfpubnightreport WITH (connect=true);

Schema Updates - ConsDB
=======================
The following is the process for changes to the Summit ConsDB tables are replicated to the USDF.

#. Disable the subscription at the USDF with ``ALTER SUBSCRIPTION usdf_exposurelog DISABLE;``
#. Work with Consdb developer to apply the Alembic Migration at the Summit
#. If there is a table added as part of the schema changes add the table to the publication.  Also add that table to list of tables to truncate in the rebuild process.
#. Work with the Consdb developer to apply the Alembic Migration at the USDF.  Below is example just as reference.  The developer should run the upgrade because they will know the version of the schema to apply.

   .. rst-class:: technote-wide-content

   .. code-block:: sql

       source /sdf/group/rubin/sw/w_latest/loadLSST.sh
       setup sdm_schemas
       setup felis
       export CONSDB_URL=postgresql://oods@usdf-summitdb-replica.slac.stanford.edu/exposurelog
       alembic -n latiss upgrade head
       alembic -n lsstcam upgrade head
       alembic -n lsstcomcam upgrade head
       alembic -n lsstcomcamsim upgrade head
       alembic -n startrackerfast upgrade head
       alembic -n startrackerwide upgrade head
       alembic -n startrackernarrow upgrade head

#. Enable and refresh the subscription at the USDF.

   .. rst-class:: technote-wide-content
   .. code-block:: sql

      ALTER SUBSCRIPTION usdf_exposurelog ENABLE;
      ALTER SUBSCRIPTION usdf_exposurelog REFRESH PUBLICATION;

#. Validate there are no replication errors on the USDF pods.

Schema Updates - Exposurelog, Narrativelog, Nightreport
=======================================================
The following is the process for changes to the ExposureLog, NarrativeLog and Night Report. Public Schema tables replicated to the USDF.

Below are the names of the subscription.  Replace ``<subscription_name>`` in each command below for the respective database.

.. rst-class:: technote-wide-content
.. code-block:: text

   usdf_exposurelog
   usdf_narrativelog
   usdf_nightreport

#. Disable the subscription at the USDF.  ``ALTER SUBSCRIPTION <subscription_name> DISABLE;``

#. Work with exposurelog developer to apply the Alembic Migration at the Summit.  The developer should run the upgrade because they will know the version of the schema to apply.

#. If there is a table added as part of the schema changes add the table to the publication.  Also add that table to list of tables to truncate in the rebuild process.

#. Apply the Alembic Migration at the USDF

#. Enable and refresh the subscription at the USDF

   .. rst-class:: technote-wide-content
   .. code-block:: sql

     ALTER SUBSCRIPTION <subscription_name> ENABLE;
     ALTER SUBSCRIPTION <subscription_name> REFRESH PUBLICATION;

#. Validate there are no replication errors on the USDF pods.

Add Tables to Publication
=========================

To add tables to the publication:

#. Create an IT Project ticket in Jira.  Include the commands needed to be added for the table including additional ``GRANTS`` if needed.  For example ``ALTER PUBLICATION usdfpub ADD TABLE cdb_latiss.visit1_quicklook;``

#. Update the SQL files `here <https://github.com/slaclab/rubin-usdf-summit-db-replica-deploy/tree/main/overlays/prod-logical-replication/summit-sql>`__. That has all the publication configuration for the Summit.

#. Update the truncate tables documentation in the Rebuild Subscriptions sections to include the additional table.

To view which tables are replicated on the publication use the query ``select * from pg_publication_tables;``

Drop Replication Slot on the Publication
========================================

To view the status of replication slots on the publication use the query ``select slot_name, active from pg_replication_slots;``

Example output below.

.. rst-class:: technote-wide-content
.. code-block:: text

   exposurelog=> select slot_name, active  from pg_replication_slots;
         slot_name       | active
   -----------------------+--------
   _cnpg_cnpg_cluster_9  | t
   _cnpg_cnpg_cluster_10 | t
   usdf_exposurelog   | t
   usdf_narrativelog  | t
   usdf_nightreport   | t
   (5 rows)

To drop a replication slot on the publisher use the below command.  Change ``<REPLACE>`` to the appropriate replication slot to drop.

.. rst-class:: technote-wide-content
.. code-block:: sql

   SELECT pg_drop_replication_slot('<REPLACE>');
