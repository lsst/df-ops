#######################
Application Information
#######################

Application Roles & Contacts
============================
.. Describe who is performing the application roles.  Detailed in about section.

.. list-table:: Application Roles
   :widths: 25 25
   :header-rows: 1

   * - Role
     - Person
   * - Application Sponsor
     -
   * - Application Owner
     -
   * - Database Administrator
     -
   * - Application Infrastructure
     -
   * - Operations Support
     -
   * - Documentation Lead
     -

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Associated Systems
==================
.. Describe other applications are associated with this applications.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

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
