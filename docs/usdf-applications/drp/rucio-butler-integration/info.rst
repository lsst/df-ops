#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

rucio-register registers Butler data with Rucio for transfer.  Hermes which sends messages about data transfers was modified to send Kafka events with Butler information. This code is in https://github.com/lsst-dm/ctrl_rucio_ingest and is where modifications to the Rucio Hermes container are developed.

ctrl_ingestd is a Butler/Rucio ingest daemon that listens to Kafka messages from the Rucio Hermes daemons and performs butler ingests.  It is used to automatically ingest registered data to a Butler.  The code for this is in https://github.com/lsst-dm/ctrl_ingestd

The France and UK Data Facilities connect to the Rucio Kafka cluster with MirrorMaker to Rucio Butler ingest events to perform locally.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.


See `DMTN-198 <https://dmtn-198.lsst.io/#federated-message-broker-diagram>`__

Associated Systems
==================
.. Describe other applications are associated with this applications.

The Rucio-Butler integration is installed in Rucio.   Events are sent to the Rucio Kafka.

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
     - Uses Rucio secrets.  No additional secrets.
   * - Vault Secrets Prod
     - Uses Rucio secrets.  No additional secrets.

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* Butler Main

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

* Network connection to France and UK Data Facilities

Disaster Recovery
=================
.. RTO/RPO expectations for application.
