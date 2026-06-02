#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

The Consolidated Database system uses these components:

- Postgres database: This database resides within the same database instance as the exposurelog in order to facilitate joins between the two, but it has distinct schemas.
  At the Summit, this database runs on the ``postgresdb01.cp.lsst.org`` server.
  At USDF, this database runs on the ``usdf-summitdb-logical-replica.sdf.slac.stanford.edu`` server.

- ``hinfo`` service: This service, running at the Summit, reads the output of the HeaderService for each instrument and inserts it into ConsDB, creating the primary keys for exposures and visits.

- ``transformed_efd`` package: This container runs periodically at USDF, querying the Engineering and Facilities Database (EFD) and transforming it into per-exposure records inserted into separate schemas within ConsDB.

- ``pqserver`` service: This service provides a REST API for querying ConsDB and for inserting rows into it.  It runs at both the Summit and USDF.

In addition, a TAP service is configured to query the ConsDB Postgres database, including a TAP Schema database describing the ConsDB schema.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Associated Systems
==================
.. Describe other applications are associated with this applications.

Rapid Analysis at the Summit analyzes images and computes quality and other metrics that are loaded into the ``*_quicklook`` tables within ConsDB schemas.

Other applications may also insert data; each should have its own table suffix.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/consdb
   * - Vault Secrets Dev
     - rubin/usdf-consdb-dev/transformed-efd
   * - Vault Secrets Prod
     - rubin/usdf-consdb/transformed-efd
       rubin/usdf-summitdb/logical-replica

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

- Kubernetes (at Summit and USDF)
- Phalanx (at Summit and USDF)
- Postgres (``usdf-summitdb-logical-replica``)
- EFD (at USDF)

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

- Kubernetes (at Summit)
- Phalanx (at Summit)
- Postgres (``postgresdb01.cp.lsst.org``)
- HeaderService (at Summit)

Disaster Recovery
=================
.. RTO/RPO expectations for application.
