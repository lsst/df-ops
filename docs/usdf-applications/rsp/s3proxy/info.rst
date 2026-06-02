#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

The service is a simple FastAPI proxy deployed under Phalanx that takes an object store bucket and path along with a pre-configured profile, retrieves the object into memory, and passes it along to the client.

The primary usage is by the Portal on the Rubin Science Platform to access HiPS tiles.

``s3proxy`` can point to any S3 bucket: in the Embargo Rack, in Weka S3, or on the public s3dfrgw endpoint, with the first two being used most frequently.

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
