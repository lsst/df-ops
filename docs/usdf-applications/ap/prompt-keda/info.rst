#######################
Application Information
#######################

Prompt Keda application information.

Application Roles & Contacts
============================
.. Describe who is performing the application roles.  Detailed in about section.

See :ref:`prompt_processing_application_roles`

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

KEDA is deployed with the KEDA operator in the Prompt Processing vClusters in the ``keda`` Kubernetes namespace.

KEDA controls autoscaling for Prompt Processing.  KEDA uses scalars to determine how aggressively to scale up and down.  Prompt KEDA is configured to autoscale based on the number of Fanned Out events in Prompt Redis.

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
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/keda
   * - Vault Secrets Dev
     - secret/rubin/usdf-prompt-processing-dev/prompt-keda
   * - Vault Secrets Prod
     - secret/rubin/usdf-prompt-processing/prompt-keda

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

See :ref:`prompt_processing_data_flow`

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

Below are the S3DF Dependencies.
 * Kubernetes
 * SLAC LDAP to authenticate to vCluster
 * Prompt Redis for creating and scaling scaled jobs.


Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

Below are external dependencies.
 * Internet access to pull Keda docker image.

Disaster Recovery
=================
.. RTO/RPO expectations for application.

The application can be redeployed with not data being needed to be restored.