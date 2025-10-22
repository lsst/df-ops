#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

The central component of APDB is `Apache Cassandra database <https://cassandra.apache.org/>`_.
The database serves approximately 200 clients of Prompt Processing system concurrently reading and writing to the database.
Cassandra stores its data on fast local storage (NVMe disks in raidz2 array).
Presently there are 12 nodes at USDF (sdfk8sk001-012) split between two Cassandra clusters.

Backups of the Cassandra files are managed by `cassandra-meduza <https://github.com/thelastpickle/cassandra-medusa>`_ service running on each cluster node.
Backups are stored in S3 bucket, off-site storage of backups is not implemented yet.

A separate application reads data from APDB and replicates it to PPDB, which will likely be implemented on top of Google BigQuery.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

.. mermaid::
  :config: {"theme": "neutral"}

  flowchart LR
          pp@{ shape: procs, label: "Prompt<br/>Processing" }
          pp <--> c8@{ shape: procs, label: "Cassandra"}
          c8 <--> disk@{ shape: lin-cyl, label: "Local<br/>storage" }
          disk <--> medusa@{ shape: procs, label: "Medusa<br/>backup" }
          medusa <--> S3disk@{ shape: lin-cyl, label: "S3 Bucket" }
          c8 --> replication["Replication"]
          replication --> ppdb[("PPDB")]

Replication process is an application separate from APDB.

Associated Systems
==================
.. Describe other applications are associated with this applications.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/lsst-dm/dax_apdb_deploy
   * - Vault Secrets Dev
     - | rubin/usdf-apdb-test/cassandra-super
       | rubin/usdf-apdb-test/cassandra
   * - Vault Secrets Prod
     - | rubin/usdf-apdb-dev/cassandra-super
       | rubin/usdf-apdb-dev/apdb-prod

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

- Prompt Processing jobs query APDB for the pre-existing data in the region covered by visit-detector.
- Based on the images and pre-existing data Prompt Processing generates a set of records that it saves to Cassandra.
- This repeats for every visit during the night, approx 1k vistits are expected during the nitght.
- Newly generated data are copied from Cassandra periodically by a replication process.
- Backups are taken perdiodically (once a day or more frequently) and uploaded to an S3 bucket.
- Off-site backup is not implemented yet.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

- Vault (for client and superuser passwords).
- S3 for backups.

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

None.

Disaster Recovery
=================
.. RTO/RPO expectations for application.

In case of disaster the content of database can be restored from the latest backup.
Recovery procedure consists of running ``medusa-cassandra`` service in a special recovery mode which copies data from S3 to the Cassandra hosts.
Cassandra cluster needs to be configured with the same number of nodes and preferrably with the same IPs.
Recovery of the data from S3 depends on the amount of data and location of backup (on-site vs off-site) and it could take anywhere between few hours and a day or longer.
