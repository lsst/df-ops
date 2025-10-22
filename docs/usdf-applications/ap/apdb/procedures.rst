##########
Procedures
##########

Intended audience: Anyone who is administering APDB.

The `dax_apdb_deploy <https://github.com/lsst-dm/dax_apdb_deploy/>`_ package implements deployment and management procedues based on ``Ansible``.
Details of operations are documented in its `README <https://github.com/lsst-dm/dax_apdb_deploy/blob/main/README.md>`_ file.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployment of a new Cassandra cluster consists of defining a set of parameters for the new instance.
This is done by adding a new group to ``group_vars`` folder and a new inventory YAML file.
Additionally new secrets need to be setup in the Vault for both a standard user account and superuser account.
Once the group and inventory are defined one needs to run a series of ansible roleplays to configure remote systems and brign up all services.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

To be completed...

Backup
======
.. Procedures for backup including how to verify backups.

Backup operations are based on ``cassandra-medusa`` service that runs on every node on the cluster.
Location of the backups on S3 is configured in the ``group_vars``.
The ``medusa-backup`` CLI is implemented to make and manage backups.

Taking backups is not automated yet.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

The services run in docker containers and will restart automatically after downtime.
Recovery from a disaster involves additional steps to restore data files from S3 to local filesystem.

To be documented...

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

Shutdown consusts of running ``down.yml`` playbook using a corresponding inventory.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

``dax_apdb_deploy`` already has inventory and configuration for production and test clusters.
Creating another Cassandra cluster would require finding a separate set of nodes with sufficient local storage.
