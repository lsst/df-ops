#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

The S3 Portal on Rubin Science Platform uses it for HIPS tiles.  The s3proxy points to a S3 bucket on embargo.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Associated Systems
==================
.. Describe other applications are associated with this applications.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/s3proxy
   * - Vault Secrets Dev
     - secret/rubin/usdf-rsp-dev/s3proxy
   * - Vault Secrets Prod
     - secret/rubin/usdf-rsp/s3proxy

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

The Portal in RSP connects to the s3proxy also deployed in RSP at the USDF.  The s3proxy proxies connections to S3 storage.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* EmbargoS3

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

No external dependencies.

Disaster Recovery
=================
.. RTO/RPO expectations for application.
