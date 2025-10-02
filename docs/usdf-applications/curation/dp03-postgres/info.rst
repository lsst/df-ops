#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

Postgres database with Solar System Objects.  The Mainly accessed from the US DAC at Google Cloud.  A service is created that is restricted to the US DAC IPs.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Associated Systems
==================
.. Describe other applications are associated with this applications.

RSP at US DAC

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/slaclab/rubin-usdf-pg-catalogs-deploy/tree/main/overlays/dp03
   * - Vault Secrets Dev
     - N/A
   * - Vault Secrets Prod
     - secret/rubin/usdf-pg-catalogs/dp03-postgres

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Users access the DP.03 dataset from the US DAC.  Mobu connects to perform test queries for monitoring.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

No S3DF dependencies.

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

Connectivity to the US DAC.

Disaster Recovery
=================
.. RTO/RPO expectations for application.
