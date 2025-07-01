#######################################
Cloud Native Postgres (CNPG) Procedures
#######################################

Intended audience: Anyone who is administering databases at the USDF.

Requesting new CNPG instance
============================
The SLAC database team builds new CNPG instances.  To request an instance

  #. Open a SNOW ticket to request the instance.  Provide the name of the instance, what vCluster it should be added to, and any database parameters that should be set.
  #. Open another SNOW ticket to request a S3 bucket for backup.  Provide the name of the database instance so that the S3 bucket can be named and the location to put the S3 vault secret.

CNPG Kubernetes Plugin
======================
CNPG developed a Kubernetes plugin to help with cluster operations.  To download goto the `CNPG site <https://cloudnative-pg.io/>`__, access the latest version and search for kubectl plugin.

PSQL Access
===========
``psql`` can be accessed from S3DF and via kubectl.  For S3DF SSH to S3DF and setup the shared stack which has psql installed.  For  S3DF SSH to S3DF and setup the shared stack which has psql installed.

Database Settings
=================
Postgres settings should be tuned based on the workload of the database.  Butler can be used as a reference, but not should be used as a template.  Here is a `good reference <https://www.enterprisedb.com/postgres-tutorials/how-tune-postgresql-memory>`__.  Below are settings that are typically tuned.

* max_connection: Max connections to allow to the database.  Please note that this value should also be coordinated with the pooler connection values.
* shared_buffers: Reasonable value is 25% up to 40% of RAM
* work_mem: memory used for query operations before writing to disk.  Very dependent on the database on what this value should be set to.  There is a balance of setting this value large enough to not spill to disk too much and not running out of memory for concurrent queries.

Database Logging
================
The below statements need to be added to the database Kubernetes manifest to enable logging of all statements.  Note that ``log_min_duration_statement`` should be set to an appropriate value to capture the appropriate minimum duration of queries.

.. rst-class:: technote-wide-content

.. code-block:: yaml

  spec:
    postgresql:
      parameters:
        log_disconnections: "on"
        log_duration: "on"
        log_min_duration_statement: 250ms
        log_statement: all


Setup Cluster
=============

Setup Pooler
============
PgBouncer is used to serve connections to the database.  A Pooler  resource is defined in Kubernetes to create the underlying Kubernetes Pods and Service.  USDF uses both session and transaction poolers.  Transaction Pooler is used for application access to databases because it more efficiently uses connections.

For services to be accessible from the S3DF they need an annotation for the service to request a S3DF IP Address that is accessible outside of the cluster.  Previously these annotations could not be defined in the pooler.  Now service annotations are supported.  Below is snippet from rucio.  Note the ``metallb.universe.tf/address-pool: sdf-rubin-ingest`` annotation.  After an IP address is created a SLAC DNS should be requested with a Service Now ticket.

.. rst-class:: technote-wide-content

.. code-block:: yaml

    apiVersion: postgresql.cnpg.io/v1
    kind: Pooler
    metadata:
    name: pooler-name
    spec:
    serviceTemplate:
        metadata:
        annotations:
            metallb.universe.tf/address-pool: sdf-rubin-ingest
        spec:
          type: LoadBalancer


Setup Backup
============
Below are instructions for setting up backup.  Backups should be created for production databases.  Backups for development are usually not needed.  For storing backups a unique, unused S3 bucket must be created.  It is very important that the S3 bucket cannot have an existing data and should not be shared.  This will cause issues with restore if the cluster names are the same and they share the same bucket.

To setup backup request a new S3 bucket with a Service Now Ticket with the name of the S3 bucket and request the credentials be stored in vault under the name of the database with a key of S3.  We use the syntax of rubin-name of database as the syntax.

Update the makefile to create a s3 secret from vault.  Example below from Butler.  Note the addition of the S3_SECRET_PATH which is the path in Vault and second line with set that creates the S3 secret.

  .. rst-class:: technote-wide-content

  .. code-block:: bash

    SECRET_PATH ?= secret/rubin/usdf-butler/postgres
    S3_SECRET_PATH ?= secret/rubin/usdf-butler/s3

    get-secrets-from-vault:
        mkdir -p etc/.secrets/
        set -e; for i in username password; do vault kv get --field=$$i $(SECRET_PATH) > etc/.secrets/$$i ; done
        set -e; for i in client-id client-secret; do vault kv get --field=$$i $(S3_SECRET_PATH) > etc/.secrets/$$i ; done

In the Cluster manifest for the database setup backup.  Example below.  Update the S3 name.

  .. rst-class:: technote-wide-content

  .. code-block:: yaml

        backup:
            retentionPolicy: "15d"
            barmanObjectStore:
            destinationPath: s3://<bucket name>
            endpointURL: https://s3dfrgw.slac.stanford.edu
            s3Credentials:
                accessKeyId:
                name: s3-creds
                key: ACCESS_KEY_ID
                secretAccessKey:
                name: s3-creds
                key: ACCESS_SECRET_KEY

Review Backups
==============
To review the status of backups run ``kubectl get backup -n <namespace>``.  Below is abbreviated output from usdf-butler.  Note that failed backups show an exist status. The most common reason has been S3 being down or slow.  Barman runs from the database pods so examine the logs to obtain more information.

  .. rst-class:: technote-wide-content

  .. code-block:: text

    NAME                                 AGE     CLUSTER        METHOD              PHASE       ERROR
    usdf-butler3-backup-20240405000000   101d    usdf-butler3   barmanObjectStore   failed      exit status 4
    usdf-butler3-backup-20240417000000   89d     usdf-butler3   barmanObjectStore   failed      exit status 1
    usdf-butler3-backup-20240418000000   88d     usdf-butler3   barmanObjectStore   failed      exit status 1
    usdf-butler3-backup-20240715000000   14h     usdf-butler3   barmanObjectStore   completed

To view  how long a backup takes run ``kubectl get backup <backup-name> -n <namespace> -o yaml``.  An abbreviated example below shows the started and stopped times in the status field.

  .. rst-class:: technote-wide-content

  .. code-block:: text

    apiVersion: postgresql.cnpg.io/v1
    kind: Backup
    spec:
      cluster:
        name: usdf-butler3
      method: barmanObjectStore
    status:
      backupId: 20240715T000000
      beginLSN: 1616/33127750
      beginWal: "000000440000161600000033"
      destinationPath: s3://rubin-usdf-butler3
      endLSN: 1616/511273D8
      endWal: "000000440000161600000051"
      endpointURL: https://s3dfrgw.slac.stanford.edu
      instanceID:
        ContainerID: containerd://454e7c0654449fc58182d8705cab4f0c9bec3d4481c381ec7d397a7155beb05c
        podName: usdf-butler3-1
      method: barmanObjectStore
      phase: completed
      s3Credentials:
        accessKeyId:
          key: ACCESS_KEY_ID
          name: s3-creds
        secretAccessKey:
          key: ACCESS_SECRET_KEY
          name: s3-creds
      serverName: usdf-butler3
      startedAt: "2024-07-15T00:00:00Z"
      stoppedAt: "2024-07-15T04:21:38Z

Ad Hoc Backup
=============
Before major database maintenance or schema migrations an ad hoc backup should be performed to prevent data loss from when the last active backup is taken to when the maintenance is performed.  Below is an example manifest to configure the backup.  Replace the values below for the cluster to be backed up.

  .. rst-class:: technote-wide-content

  .. code-block:: yaml

     apiVersion: postgresql.cnpg.io/v1
     kind: Backup
     metadata:
        name: <name of backup>
        namespace: <namespace for cluster>
      spec:
        cluster:
          name: <name of cluster>


Restore from Backup
===================
Restores have to be performed on a separate cluster. and reference the backups in Ceph/S3.  Below is an example configuration to restore butler.  The ``serverName`` is optional, but should be specified if the new cluster name created differs from the original cluster name.  Restores can be performed in the same kubernetes namespace, different namespace, or different vCluster depending on the purpose of the restore.  Documentation on restore is on the CNPG website.  Adjust the WAL ``maxParallel`` setting is their are a lot of WALS to restore.  This can occur when the last successful backup was completed successfully in a while and a large amount of WALs need to be replayed as part of the restore.

  .. rst-class:: technote-wide-content

  .. code-block:: yaml

    bootstrap:
    recovery:
      source: usdf-butler3
    externalClusters:
    - name: usdf-butler3
      barmanObjectStore:
        destinationPath: s3://rubin-usdf-butler3
        endpointURL: https://s3dfrgw.slac.stanford.edu
        serverName: usdf-butler3
        s3Credentials:
          accessKeyId:
            name: s3-creds
            key: ACCESS_KEY_ID
          secretAccessKey:
            name: s3-creds
            key: ACCESS_SECRET_KEY
        wal:
          maxParallel: 8

To restore a specific backup browse S3 first review the available backups in S3.  Below is an example command to run from S3DF to browse the backups for butler dc2-16-prod database s3-dc2-16 S3 profile.
Update your ``aws-credentials.ini`` under ``.lsst`` in your home directory ``/sdf/home/j/jdoe`` to have a profile for the S3 bucket. Backups are under the base directory as ``data.tar`` files.

 .. rst-class:: technote-wide-content

 .. code-block:: bash

    singularity exec /sdf/sw/s3/aws-cli_latest.sif aws --endpoint-url https://s3dfrgw.slac.stanford.edu s3 --profile s3-dc2-16 ls s3://rubin-usdf-butler-dc2-16/usdf-butler-dc2-16/base/

The above command will display an output similar to below.

 .. rst-class:: technote-wide-content

 .. code-block:: text

    PRE 20241007T000902/
    PRE 20241008T000902/
    PRE 20241008T193421/
    PRE 20241009T000902/
    PRE 20241009T200458/
    PRE 20241009T222802/
    PRE 20241010T000902/
    PRE 20241011T000902/
    PRE 20241012T000903/
    PRE 20241013T000903/
    PRE 20241014T000903/
    PRE 20241015T000903/
    PRE 20241018T055313/
    PRE 20241019T000002/
    PRE 20241020T000002/
    PRE 20241021T000003/
    PRE 20241022T000003/
    PRE 20241023T000002/

Below is an example which restores the Panda IDDS database from a backup on September 1, 2024.  Note the ``backupID`` references the date.

 .. rst-class:: technote-wide-content

 .. code-block:: yaml

    bootstrap:
        recovery:
          source: panda-idds
          recoveryTarget:
            backupID: 20240901T000003
      externalClusters:
      - name: panda-idds
        barmanObjectStore:
          destinationPath: s3://rubin-usdf-panda-idds
          endpointURL: https://s3dfrgw.slac.stanford.edu
          serverName: usdf-panda-idds
          s3Credentials:
            accessKeyId:
              name: s3-creds
              key: ACCESS_KEY_ID
            secretAccessKey:
              name: s3-creds
              key: ACCESS_SECRET_KEY
          wal:
            maxParallel: 8

Building Containers
===================
Custom container image are built `at this link <https://github.com/lsst-sqre/cnpg-postgres-images>`__.  pgSphere, cron, other extensions are added in this build process.

Enable PgSphere
===============
PgSphere is installed on the LSST CNPG image as detailed in the Building Container Image section.  To enable the extension connect to the database and execute the ``CREATE EXTENSION pg_sphere;``   Below is how you can validate that pg_sphere is enabled and version.


.. rst-class:: technote-wide-content

.. code-block:: sql

   SELECT pg_sphere_version();
    pg_sphere_version
    -------------------
    1.3.2
    (1 row)

Review Cluster Health
=====================
Run ``kubectl cnpg status <cluster-name> -n <namespace>``  to get the status of the cluster replacing the cluster name and namespace.  Below is an abbreviated cluster from the usdf-butler3  cluster.  Note there are 2 ready instances, the streaming replicating status is active, WAL archiving is working, and backup is working.

.. rst-class:: technote-wide-content

.. code-block:: text

    Cluster Summary
    Name:                usdf-butler3
    Namespace:           prod2
    System ID:           7129014289015427109
    PostgreSQL Image:    ghcr.io/lsst-sqre/cnpg-postgres-images:14.5
    Primary instance:    usdf-butler3-2
    Primary start time:  2024-06-27 19:06:01 +0000 UTC (uptime 426h59m57s)
    Status:              Cluster in healthy state
    Instances:           2
    Ready instances:     2
    Current Write LSN:   1616/7D000110 (Timeline: 68 - WAL File: 00000044000016160000007D)
    Continuous Backup status
    First Point of Recoverability:  2024-06-30T04:18:31Z
    Working WAL archiving:          OK
    WALs waiting to be archived:    0
    Last Archived WAL:              00000044000016160000007C   @   2024-07-15T13:58:13.046625Z
    Last Failed WAL:                -
    Physical backups
    No running physical backups found
    Streaming Replication status
    Replication Slots Enabled
    Name            Sent LSN       Write LSN      Flush LSN      Replay LSN     Write Lag  Flush Lag  Replay Lag  State      Sync State  Sync Priority  Replication Slot
    ----            --------       ---------      ---------      ----------     ---------  ---------  ----------  -----      ----------  -------------  ----------------
    usdf-butler3-1  1616/7D000110  1616/7D000110  1616/7D000110  1616/7D000110  00:00:00   00:00:00   00:00:00    streaming  async       0              active
    Managed roles status
    No roles managed
    Instances status
    Name            Database Size  Current LSN    Replication role  Status  QoS        Manager Version  Node
    ----            -------------  -----------    ----------------  ------  ---        ---------------  ----
    usdf-butler3-2  1339 GB        1616/7D000110  Primary           OK      Burstable  1.21.1           sdfk8sn003


Resize Cluster
==============
To increase or decrease the number of database instances edit the ``instances`` section of the database manifest as detailed below and apply the change.

.. rst-class:: technote-wide-content

.. code-block:: yaml

   spec:
     instances: 2

Upgrade Operator
================
To update the CNPG operator first check the release notes to make sure there are prerequisites or order to the upgrades.  If not then download the operator mainfest.  There is usually a makefile for the database with a make update-cnpg-operator step.  Update the makefile to have the CNPG version then run make apply-cnpg-operator to perform the upgrade.  Some recent upgrades have had this error returned

``The CustomResourceDefinition "poolers.postgresql.cnpg.io" is invalid: metadata.annotations: Too long: must have at most 262144 bytes``

If so change the makefile to have this syntax for ``make apply-cnpg-operator``

.. rst-class:: technote-wide-content

.. code-block:: bash

   kubectl apply -f cnpg-operator.yaml --server-side --force-conflicts

Database Upgrades
=================
Minor version upgrades are performed in place by changing the container image to the appropriate minor version.   Major version upgrades did not used to be supported with CNPG, but are now supported with CNPG v1.26 and at least Postgres version 16.  To read about the in place upgrade process access the `CNPG documentation <https://cloudnative-pg.io/>`__ for operator version in place and search for ``PostgreSQL Upgrades``

Below is the legacy process using ``pg_dump`` and ``pg_restore``
  #. Create new CNGP instance with the Postgres version.  If the CNPG Rubin image is not built see Building Container Image section.
  #. Note what the current transaction level is set for the database.  Set the database to read only for the databases to be migrated with ``ALTER DATABASE <database> SET default_transaction_read_only TO on;``.  Replace database with the database(s) to be upgraded.
  #. Run pg_dump from the S3DF.  Example command is ``pg_dump -U <username> -h <hostname> -d <database name> -F t -f <filename>.pgdump``
  #. Run pg_restore from the S3DF to the new CNPG instance.
  #. Validate the new database, enable backups, update any client connections settings.  Set the transaction level back to the original setting to allow writes.
  #. Once functionality is validated and a successful backup has been taken the old instance can be deleted.

Hibernate Cluster
==================
Declarative hibernation can be used to hibernate databases.   Reference documentation is on the `CNPG site <https://cloudnative-pg.io/>`__ if you search for Hibernate.

Below is the command to hibernate a cluster.  Replace the name of the cluster and namespace.  Pods will be deleted.  The Cluster and PVCs are retained.

.. rst-class:: technote-wide-content

.. code-block:: bash

   kubectl annotate cluster <name of cluster> --overwrite cnpg.io/hibernation=on -n <namespace>

The below command will annotate the cluster to wake up the cluster.  Pods will be created.

.. rst-class:: technote-wide-content

.. code-block:: bash

   kubectl annotate cluster <name of cluster> --overwrite cnpg.io/hibernation=off -n <namespace>

To view the status of hiberation review the annotations.  Example below with hibernation on.

.. rst-class:: technote-wide-content

.. code-block:: text

   kubectl describe cluster -n test-cnpg
   Name:         test-cnpg
   Namespace:    test-cnpg
   Labels:       <none>
   Annotations:  cnpg.io/hibernation: on
   API Version:  postgresql.cnpg.io/v1