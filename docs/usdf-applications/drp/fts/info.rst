###################
Service Information
###################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

MariaDB is the database for FTS3.  It is installed with the MariaDB database operator.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Associated Systems
==================
.. Describe other applications are associated with this applications.

Rucio

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/slaclab/rubin-fts3-deploy
   * - Vault Secrets Dev
     - secret/rubin/usdf-fts3-dev
   * - Vault Secrets Prod
     - secret/rubin/usdf-fts3

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

Disaster Recovery
=================
.. RTO/RPO expectations for application.
