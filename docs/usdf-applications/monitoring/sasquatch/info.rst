###################
Service Information
###################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

The major components of Sasquatch are Strimzi Kafka and InfluxDB Enterprise.  Kafka events from the Summit are replicated with the USDF Sasquatch MirrorMaker2.  This data is accessible with InfluxDB and Chronograf.  The Kafka Schema Registry is installed and stores the schemas for all topics.  Sasquatch is also used to store metrics from some USDF applications.  Metrics are integrated via push with Kafka events integrated into InfluxDB.

Sasquatch Kafka Brokers and InfluxDB Pods are scheduled with Kubernetes node affinities to specific nodes that have the ZFS file system for local storage.  This was configured due to performance issues with Weka.

The Sasquatch URLs are `here <https://sasquatch.lsst.io/environments.html#usdf>`__

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Architecture diagram is `here <https://sasquatch.lsst.io/developer-guide/architecture.html>`__

Associated Systems
==================
.. Describe other applications are associated with this applications.

Sasquatch is integrated with USDF RSP systems for metrics collection.  Prompt Processing publishes metrics to Sasquatch Dev with the Sasquatch Rest Proxy.  ConsDB and Obsloctap query information from Sasquatch InfluxDB.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/sasquatch
   * - Vault Secrets Dev
     - secret/rubin/usdf-rsp-dev/sasquatch
   * - Vault Secrets Int
     - secret/rubin/usdf-rsp-int/sasquatch
   * - Vault Secrets Prod
     - secret/rubin/usdf-rsp/sasquatch

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

The USDF Sasquatch has Kafka installed with MirrorMaker2 installed to replicate Kafka events from the Summit using the Long Haul Network (LHN).  A socat proxy is installed in the ``kafka-proxy`` namespace in the usdf-rsp vCluster to proxy connections to the Summit.  Traffic is routed to socat with DNS entries in a config map in the ``kube-system`` namespace that resolve connections to the Summit Sasquatch Kafka Cluster external bootstrap and broker addresses to the socat proxy services for the bootstrap and each broker.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* Installation is on nodes with Local ZFS Storage

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

* LHN Connection to the Summit

Disaster Recovery
=================
.. RTO/RPO expectations for application.
