##########
Procedures
##########

Intended audience: Anyone who is administering Rucio.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

USDF Rucio deployment is done through the https://github.com/slaclab/rubin-rucio-deploy repository. This project requires a Kubernetes cluster with permissions to run operators as needed. Once you have access to your Kubernetes cluster and access to Vault secrets, Rucio can be deployed for a given overlay depending on the cluster (found in ``overlays/{dev,prod}``) using the Makefile found there with:

.. code-block:: bash

    make apply

The deployment uses the official Rucio images (https://github.com/rucio/containers), besides the ``hermes`` daemon. Rucio manifests are mainly created from the official Rucio Helm charts (https://github.com/rucio/helm-charts).

Deployment is through the Makefile and overlays in https://github.com/slaclab/rubin-rucio-deploy

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

When there is a new Rucio version release that the cluster should be upgraded to, there are a few steps that must be done.

Database
--------
Rucio's database schema is changed only for major versions (i.e. 37.0.0 --> 38.0.0). In this case, the database schema must be upgraded in order for the deployment to function properly. Rucio has built-in checks to ensure the correct database schema version.

`Rucio Transfer Monitoring Dashboard <https://grafana.slac.stanford.edu/d/YVcucApIk/rucio-transfer-monitoring?var-bin=6h&orgId=1&from=now-7d&to=now&timezone=browser&var-fts=$__all&var-dst_rse=$__all&var-src_rse=$__all&var-group_by=payload.dst-rse&var-protocol=$__all&var-filters=&var-del_rse=$__all&refresh=1m>`__


Backup
======
.. Procedures for backup including how to verify backups.

Postgres database backups are done through the CNPG operator. Backups are done periodcially and are uploaded to the SLAC S3 storage. This is configured by the database administrator.

Backups of the Rucio Database are configured.

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

To cleanly shutdown the Rucio application, simply run:

.. code-block:: bash

   make destroy

This will delete all secrets, deployments, pods, services, etc from the cluster.

Reproduce Service
=================
.. How to reproduce service for testing purposes.
