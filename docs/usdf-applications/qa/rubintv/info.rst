#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

RubinTV is a web application with a front end and back end.  RubinTV connects to the ``rubin-rubintv-data-usdf`` Embargo S3 bucket to display images.  There is no application database.  Gafaelfawr is used for authentication.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

.. image:: RubinTV_buckets.png
   :width: 2000
   :alt: RubinTV Buckets

Associated Systems
==================
.. Describe other applications are associated with this applications.

Rapid Analysis at the Summit creates and and transfers images that RubinTV displays.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     -
   * - Vault Secrets Dev
     -
   * - Vault Secrets Prod
     -

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Rapid Analysis at the Summit performs ongoing data transfers of images to the ``rubin-rubintv-data-usdf`` Embargo S3 bucket at USDF.  There is a RubinTV is a web application that displays these images.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* Embargo S3
* Kubernetes
* DEX and LDAP for user authentication

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

* File Transfers from the Summit

Disaster Recovery
=================
.. RTO/RPO expectations for application.
