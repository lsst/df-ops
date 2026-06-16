##########
Procedures
##########

Intended audience: Anyone who is administering APDB.

The `dax_apdb_deploy <https://github.com/lsst-dm/dax_apdb_deploy/>`_ package implements deployment and management procedures based on ``Ansible``.
Details of operations are documented in its `README <https://github.com/lsst-dm/dax_apdb_deploy/blob/main/README.md>`_ file.

``dax_apdb_deploy`` needs to be cloned to a user's directory on any ``rubin-devl`` machine and setup:

.. code-block:: bash

   cd somewhere
   git clone git@github.com:lsst-dm/dax_apdb_deploy.git
   cd dax_apdb_deploy
   make setup
   . ./setup.sh

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployment of a new Cassandra cluster consists of defining a set of parameters for the new instance.
This is done by adding a new group to ``group_vars`` folder and a new inventory YAML file.
Additionally new secrets need to be setup in the Vault for both a standard user account and superuser account.
Once the group and inventory are defined one needs to run a `series of Ansible playbooks <https://github.com/lsst-dm/dax_apdb_deploy/blob/main/README.md#bootstrapping-a-new-cluster>`_ to configure remote systems and bring up all services.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

Maintenance operations that could impact APDB availability need to be announced on ``dm-prompt-processing-dev`` Slack channel in advance.

Operations that involve CQL queries (e.g. altering keyspace or table properties) need to be executed on one of the cluster nodes.
There is a ``cqlsh`` wrapper script installed in a Docker deployment directory on each cluster node.

.. code-block:: bash

   ssh rubincas@sdfk8sk001
   cd apdb_deploy/docker
   # Some operations may need superuser access. Cqlsh will prompt for a password.
   ./cqlsh -u superuser
   Password:
   cqlsh> DESCRIBE KEYSPACES
   cqlsh> ...

Tasks that use ``nodetool`` command can be run from ``dax_apdb_deploy`` using its ``ansible-pssh`` command, e.g.:

.. code-block:: bash

   # -d means to change to docker deployment directory before running the command.
   # -1 means execute command on a single cluster node, default is to run on all nodes.
   ansible-pssh -i inventory/apdb_prod.yaml -d -1 "./nodetool status"

Periodic maintenance tasks are executed by cron jobs from user's account (currently ``salnikov``).
Scripts used by the cron jobs are located in `dax_apdb_deploy/tree/main/etc/cron <https://github.com/lsst-dm/dax_apdb_deploy/tree/main/etc/cron>`_ directory.
Cron jobs use pre-installed ``dax_apdb_deploy`` location in user's home directory.

Presently there are a few periodic cron jobs:

- backups of the ``prod`` Cassandra cluster (daily/weekly/monthly/yearly) (etc/cron/backup-job.sh)
- backups of the ``dev`` Cassandra cluster (daily/weekly) (etc/cron/backup-job.sh)
- cleanup of the old backups (etc/cron/backup-cleanup-job.sh)
- cluster repair (twice a week) (etc/cron/repair-job.sh)
- check of cluster connection status by checking Cassandra port on each node (every 10 minutes)

Backup
======
.. Procedures for backup including how to verify backups.

Backup operations are based on ``cassandra-medusa`` service that runs on every node on the cluster.
Location of the backups on S3 is configured in the ``group_vars``.
The ``medusa-backup`` CLI is implemented to make and manage backups.

Backups of the production cluster happen daily at 7:00 USDF time.
In addition to daily backups there are weekly, monthly, and yearly backups.
We keep 10 latest daily backups, 8 weekly backups, and 12 monthly backups.
Yearly backups will be kept forever in case we will need to access data that was removed.

Each backup created by ``cassandra-medusa`` is a full backup, but backups use deduplication.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

The services run in docker containers and will restart automatically after downtime.
Recovery from a disaster involves additional steps to restore data files from S3 to local filesystem.
Restore procedure is documented in ``dax_apdb_deploy``.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

Shutdown consists of running ``down.yml`` playbook using a corresponding inventory.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

``dax_apdb_deploy`` already has inventory and configuration for production, development (used for Prompt Production development), and integration clusters.
Creating another Cassandra cluster would require finding a separate set of nodes with sufficient local storage.
