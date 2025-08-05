#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

Prompt Redis is deployed as statefulset in the Prompt Processing vClusters in the ``prompt-redis`` Kubernetes namespace.

The Next Visit Fan Out Service sends fanned out events to Redis Streams. Within Redis Streams a stream is configured for each instrument along with a corresponding consumer group and Prompt Processing is configured with a consumer group to read pending messages. The naming for the streams is ``instrument:<instrument_name>``.  LSSTCam for example is ``instrument:lsstcam``

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

See :ref:`prompt_processing_architecture_diagram`

Associated Systems
==================
.. Describe other applications are associated with this applications.

See :ref:`prompt_processing_associated_systems`

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/prompt-redis
   * - Vault Secrets Dev
     - No Secrets
   * - Vault Secrets Prod
     - No Secrets

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

See :ref:`prompt_processing_data_flow`

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

Below are the S3DF Dependencies for Prompt Redis.
 * Kubernetes
 * SLAC LDAP to authenticate to vCluster
 * Next Visit Fan Out to receive Fanned Out events

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

Below are external dependencies.
 * Internet access to pull Redis docker image.

Disaster Recovery
=================
.. RTO/RPO expectations for application.

The application data does not need to be restored in a DR event.  The application can be redeployed and then follow the the :ref:`Creating Redis Streams` procedure to create the keys and consumer groups.