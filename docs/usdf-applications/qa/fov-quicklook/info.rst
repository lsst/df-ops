#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

Users login into the front end to access images.  Gafaelfawr Ingress is used for authentication.  Images are accessed from the ``rubin-summit`` bucket.  An image metadata cache is stored in a Postgres database in the fov-quicklook namespace.  No pixel data is stored in the database.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Associated Systems
==================
.. Describe other applications are associated with this applications.

Butler Embargo and Main.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/fov-quicklook
   * - Vault Secrets Dev
     - secret/rubin/usdf-rsp-dev/fov-quicklook
   * - Vault Secrets Prod
     - secret/rubin/usdf-rsp/fov-quicklook

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* Embargo S3.   Images in the ``rubin-summit`` bucket.
* Butler Embargo and Main

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

Disaster Recovery
=================
.. RTO/RPO expectations for application.
