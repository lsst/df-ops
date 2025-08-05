#######################
Application Information
#######################

Prompt Processing application information.

.. _prompt_processing_architecture:

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

Prompt Processing is deployed with KEDA scaled jobs.

.. _prompt_processing_architecture_diagram:

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

.. _prompt_processing_associated_systems:

Associated Systems
==================
.. Describe other applications are associated with this applications.

Next Visit Fan Out
Prompt Redis
Prompt Kafka
Alert Stream Broker

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration LSSTCam
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/prompt-keda-lsstcam
   * - Vault Secrets Dev
     - secret/rubin/usdf-prompt-processing-dev/prompt-processing
   * - Vault Secrets Prod
     - secret/rubin/usdf-prompt-processing/prompt-processing

.. _prompt_processing_data_flow:

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Fanned Out events come from the Summit.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

Below are the S3DF Dependencies for the Prompt Processing.
 * Kubernetes
 * SLAC LDAP to authenticate to vCluster
 * LHN connectivity to the Summit for Next Visit Fan Out
 * Next Visit Fan Out
 * Prompt Kafka
 * Prompt Keda
 * Prompt Redis
 * rubin-summit Ceph bucket
 * Embargo Butler
 * Cassandra Cluster
 * Alert Stream Broker
 * Sattle

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

Below are external dependencies.
 * Internet access to pull Redis docker image
 * Internet access to send alerts

Disaster Recovery
=================
.. RTO/RPO expectations for application.
