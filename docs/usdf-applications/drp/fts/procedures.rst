##########
Procedures
##########

Intended audience: Anyone who is administering FTS.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures
USDF FTS3 deployment manifests are located in the https://github.com/slaclab/rubin-rucio-deploy repository. This project requires a Kubernetes cluster with permissions to run operators as needed. Once you have access to your Kubernetes cluster and access to Vault secrets, FTS3 can be deployed for a given overlay depending on the cluster (found in `overlays/{dev,prod}`) using the Makefile found there with:

.. code-block:: bash

    make apply

The deployment uses a custom built FTS3 (https://github.com/fnal-fife/fnal-fts3-rubin).

Deployment is through the Makefile and overlays in https://github.com/slaclab/rubin-fts3-deploy

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.
When there is a new FTS3 version release that the cluster should be upgraded to, there are a few steps that must be done.

Database
--------
FTS3's database schema is changed only for major versions (i.e. 37.0.0 --> 38.0.0). In this case, the database schema must be upgraded in order for the deployment to function properly. FTS3 has built-in checks to ensure the correct database schema version.

`FTS3 Transfer Monitoring Dashboard <https://grafana.slac.stanford.edu/d/YVcucApIk/rucio-transfer-monitoring?var-bin=6h&orgId=1&from=now-7d&to=now&timezone=browser&var-fts=$__all&var-dst_rse=$__all&var-src_rse=$__all&var-group_by=payload.dst-rse&var-protocol=$__all&var-filters=&var-del_rse=$__all&refresh=1m>`__


Backup
======
.. Procedures for backup including how to verify backups.
FTS3 uses MariaDB as the database backend. Backups can be setup through the MariaDB Operator. FTS developers do not recommend backing up the entire database. Restoring from a backup can cause issues with tranfers that have already completed or have not yet completed. The developers do recommend backing up tables containing configuration. See https://fts3-docs.web.cern.ch/fts3-docs/docs/install/backup_policy.html for more details.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.
1. Ensure you have access to the Kubernetes cluster and Vault secrets.

2. Enter the desired overlay.

3. Apply manifests

.. code-block:: bash

   make apply


Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.
To cleanly shutdown the FTS3 application, simply run:

.. code-block:: bash

   make destroy

This will delete all secrets, deployments, pods, services, etc from the cluster.

Reproduce Service
=================
.. How to reproduce service for testing purposes.
