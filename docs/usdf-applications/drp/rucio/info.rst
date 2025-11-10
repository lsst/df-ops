#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

* Postgres via CloudNativePG
* Kafka via Strimzi

A Postgres database is deployed in the rucio-db-16b namespace.

The ``rucio-kafka`` Kafka Cluster is deployed in the Rucio vClusters.  The Rucio-Butler integration uses this to ingest files into Butler.  Kafka MirrorMaker is deployed at the UK and France Data Facilities to synchronize Kafka messages and ingest files locally in each Data Facility into Butler.  To allow this connectivity ``rucio-kafka`` is configured with external IP Addresses on the external bootstrap and brokers.


Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Associated Systems
==================
.. Describe other applications are associated with this applications.

* FTS3
* Cloud Native PG: Postgres Operator
* Strmzi: Kafka Operator

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/slaclab/rubin-rucio-deploy
   * - Vault Secrets Dev
     - ``secret/rubin/usdf-rucio-dev``
   * - Vault Secrets Prod
     - ``secret/rubin/usdf-rucio``

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* Weka Storage

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

Disaster Recovery
=================
.. RTO/RPO expectations for application.
