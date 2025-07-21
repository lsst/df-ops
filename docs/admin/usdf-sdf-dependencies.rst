##########################
USDF and S3DF Dependencies
##########################

Application and user dependencies with the USDF and S3DF infrastucture.  Organized the infrastructure component for easier identification during outage restoration what to validate.

Butler Database Embargo
=======================
Butler Embargo database registry.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Application
     - vCluster
     - Description
   * - Prompt Processing
     - usdf-prompt-processing
     - Prompt Processing connects to the standby replica for reads.  Writes are to the primary replica until the Butler writer service is implemented.
   * - Butler Writer Service
     - usdf-prompt-processing
     - Batches writes to Butler from Prompt Processing

Butler Database Main
====================
Butler Main database registry.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Application
     - vCluster
     - Description
   * - Prompt Processing
     - usdf-prompt-processing
     -


Cassandra
=========
Alert Production Cassandra cluster.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Application
     - vCluster
     - Description
   * - Prompt Processing
     - usdf-prompt-processing
     - Prompt Processing connects to Cassandra for reads and writes during processing.

htcondor
========
.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Application
     - vCluster
     - Description
   * - Data Release Processing
     - n/a
     - Data Release Processing run in Slurm

Internet
========
Connection to the Internet.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Application
     - vCluster
     - Description
   * - ArgoCD - All instances
     - Multiple vClusters
     - ArgoCD connects to GitHub for configurations to deploy.
   * - Alert Stream Broker
     - usdf-alert-stream-broker
     - Brokers connect to the Alert Stream Broker to download alerts with Kafka Consumers.
   * - Minor Planet Survey - MPCorb Replica
     - usdf-minor-planet-survey
     - Postgres Logical replication connects to the Minor Planet Center.
   * - Minor Planet Survey - MPC Sandbox
     - usdf-minor-planet-survey
     - Postgres Logical replication connects to the MPC.


LDAP
====
LDAP is used for authorization to Kubernetes and ArgoCD.  When it is down no changes can be made to running applications.

Long Haul Network and Socat Proxies
===================================
Long haul network from the USDF to Chile.  Socat proxies all these connections.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Application
     - vCluster
     - Description
   * - Prompt Processing - Next Visit Fan Out
     - usdf-prompt-processing
     - Next Visit Fan Out connects to the Summit Sasquatch for Next Visit Kafka events.
   * - Sasquatch
     - usdf-prompt-processing
     - Mirrormaker at USDF replicates data from the Summit Sasquatch.
   * - Summit Database Replica
     - usdf-summitdb
     - Postgres Logical replication from the Summit database.


Grafana and Loki
================
Many application teams use Grafana and Loki to manage and track the status of their applications.

sdfdata3
========
S3 Interface for Weka that is outward facing.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Application
     - vCluster
     - Description
   * - QServ
     - usdf-rsp, usdf-rsp-dev
     - Connections from US DAC to images stored in S3 at the USDF.

s3dfrgw
=======
S3 gateway

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Application
     - vCluster
     - Description
   * - Large File Annex
     -
     - Files from summit saves to S3
   * - CNPG Database WAL archiving and backups
     - All vClusters with CNPG
     - WAL archives and backups configured to send to buckets per database instance.  When down database storage could fill up and crash database.


SDFData Filesystem
==================
SDFData filesystem on Weka.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Application
     - vCluster
     - Description
   * - Access to Rubin project data
     - n/a
     - Image files, code, and any files not cached.  Users largely cannot do work when this is down.

SDFData Ceph Tiering Cluster
============================

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Application
     - vCluster
     - Description
   * - Access to non cached SDF data
     - n/a
     - Image files, code, and any files not cached.  Users largely cannot do work when this is down.
   * - Unembargo process
     - n/a
     - Unembargo process frees up space.  Critical process or otherwise cache tier will run out of space.

sdfcron001
==========
Cron server that runs tasks on a schedule.

Container Image Cache
=====================
Cache for container images.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Application
     - vCluster
     - Description
   * - Nublado
     - usdf-rsp
     - Container images are pointed to use cache at USDF.

QServ
=====
.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Application
     - vCluster
     - Description
   * - US DAC Rubin Science Platform
     - Not in a vCluster at USDF
     - US DAC at Google Cloud

