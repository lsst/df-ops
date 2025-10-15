#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

Obsloctap is a web service written in Python that publishes a JSON representation of the observing schedule and for past observations.  Obsloctap obtains information about upcoming observations from the ``lsst.sal.Scheduler.logevent_predictedSchedule`` Kafka topic on the USDF Summit Sasquatch.  This is replicated from the Summit to the USDF using MirrorMaker.



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
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/obsloctap
   * - Vault Secrets Dev
     - secret/rubin/usdf-rsp-dev/obsloctap
   * - Vault Secrets Prod
     - secret/rubin/usdf-rsp/obsloctap

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* LFA S3 bucket
* Butler Main Postgres
* ConsDB Postgres
* Sasquatch Kafka

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

* LHN to Summmit for Sasquatch to receive events.

Disaster Recovery
=================
.. RTO/RPO expectations for application.
