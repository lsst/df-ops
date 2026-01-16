###################
Service Information
###################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

Prompt Kafka is deployed with Strimzi in the Prompt Processing vCluster.  The Strimzi Schema Registry is not used.  Schemas are managed with Pydantic in Butler Writer.

Prompt Processing sends events containing dataset records to Prompt Kafka as Kafka messages.  The Butler Writer Services batches up these messages and inserts into the Embargo Butler.

The Prompt Publication services reads Butler Ingestion events.

Further details in `DMTN-310 Reducing Butler database contention in Prompt Processing <https://dmtn-310.lsst.io/>`__

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

.. mermaid::

   graph TD
      %% Node Definitions
      PPS[Prompt Publication Service]
      PKJ[prompt-keda-lsstcam<br/>KEDA Scaled Jobs]
      PK(prompt-kafka)
      BWS[Butler Writer Service]
      EB[(Embargo Butler)]

      %% Connections and Labels

      PKJ -- "Sends Dataset Records" --> PK
      PPS -- "Reads Butler Ingestion Events" --> PK
      PK --> BWS
      BWS -- "Batch Insert Dataset Records" --> EB

Associated Systems
==================
.. Describe other applications are associated with this applications.

The Butler Writer Service in the Butler Writer Service Namespace in the Prompt Processing vClusters sends events to the ``butler-writer`` and ``butler-writer-ingestion-events`` topics.

The Prompt Publication Service consumes events from the ``butler-writer-ingestion-events`` topic.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/prompt-kafka
   * - Vault Secrets Dev
     - secret/rubin/usdf-prompt-processing-dev/prompt-kafka
   * - Vault Secrets Prod
     - secret/rubin/usdf-prompt-processing/prompt-kafka


Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Details in Architecture diagram above.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* Weka for Persistent Volume Storage

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

No external dependencies

Disaster Recovery
=================
.. RTO/RPO expectations for application.
