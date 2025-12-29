#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

The Alert Archive database's design is described in detail in `DMTN-183 <https://dmtn-183.lsst.io/>`_.
The Alert Archive is a combination of three systems, the Ingester, Server, and S3 bucket.  The Ingester
is a Kafka consumer running alongside the Alert Stream and reads alerts from active Alert Stream topics.
The Ingester worker checks the Alert Stream topic at regular intervals, consumes new alerts, compresses
the individual alerts, and posts them to the S3 bucket located at USDF. To retrieve these alerts, the
Alert Archive server allows for retrieval based on the source ID of the alert via an http handler.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Associated Systems
==================
.. Describe other applications are associated with this applications.

The alert archive is dependant on the Alert Stream Broker <https://github.com/lsst-sqre/phalanx/tree/main/applications/alert-stream-broker> __.,
which recieves its alert packets from the Prompt Processing pipelines <>

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

The Alert Archives configuration is split between three different Github repositories. The Server and
Ingester are in separate LSST DM repositories, and their deployment is managed
via Phalanx helm charts.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - GitHub Application Code Repository
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/alert-stream-broker/charts/alert-database
     - https://github.com/lsst-dm/alert_database_ingester
     - https://github.com/lsst-dm/alert_database_server
   * - Vault Secrets Dev
     - secret/rubin/usdf-alert-stream-broker-dev/alert-stream-broker/
   * - Vault Secrets Prod
     -

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

The Alert Archive relies on the `Alert Stream <https://github.com/lsst-sqre/phalanx/tree/main/applications/alert-stream-broker>`_.
Alerts are read from the alert stream via the Ingester. The Ingester
checks for alerts every 60 minutes, and when it begins reading new alerts will continue read until
all alerts have been read and sent to the alert-archive S3 bucket and a 30 minute timeout has been reached.
Here, the alerts can be retrieved via the Server, which allows for simple key retrieval.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* ArgoCD
* S3 Storage
* Phalanx

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

None

Disaster Recovery
=================
.. RTO/RPO expectations for application.

If the Alert Archive Ingester or the Alert Archive Server goes down, follow instructions in `DMTN-214 <https://dmtn-214.lsst.io/>`_ for recovery steps.
