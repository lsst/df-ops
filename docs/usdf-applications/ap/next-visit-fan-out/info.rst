###########
Information
###########

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

Next Visit Fan out is deployed as deployment in the Prompt Processing vClusters in the ``next-visit-fan-out`` Kubernetes namespace.  No Kubernetes Services are deployed.

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
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/next-visit-fan-out
   * - Vault Secrets Dev
     - secret/rubin/usdf-prompt-processing-dev/next-visit-fan-out
   * - Vault Secrets Prod
     - secret/rubin/usdf-prompt-processing/next-visit-fan-out



Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

See :ref:`prompt_processing_data_flow`

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

Below are the S3DF Dependencies for the Next Visit Fan Out.
* Kubernetes
* SLAC LDAP to authenticate to vCluster
* LHN connectivity to the Summit for Next Visit Fan Out

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

Below are external dependencies.
* Internet access to pull Next Visit Fan out docker image.

Disaster Recovery
=================
.. RTO/RPO expectations for application.
