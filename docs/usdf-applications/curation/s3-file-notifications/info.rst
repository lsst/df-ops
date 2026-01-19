###################
Service Information
###################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

The `Ceph S3 bucket notification feature <https://docs.ceph.com/en/latest/radosgw/notifications/#create-a-topic>`__ is used to send notifications as Kafka events when Objects are created in the ``rubin-summit`` bucket in production and the ``rubin-pp-dev`` bucket in development.  The bucket notification is configured to send to the S3 File Notifications Kafka cluster.  An instance of S3 File Notifications is deployed in both Prompt Processing prod and dev.

S3 File Notifications Kafka is installed with Phalanx and ArgoCD.  Three brokers are configured for redundancy.  Authentication, Authorization, and SSL are not enabled as these did not work when setting up Ceph notifications.  Load Balancer IPs are provisioned from the ``sdf-rubin-ingest`` network for the Brokers and External Bootstrap to provide connectivity outside of the cluster in S3DF.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

.. mermaid::

   graph TD
      A[Summit Transfer] -->|File Transfers| B[rubin-summit bucket]
      B -->|Notification created for each file| C[S3 File Notifications Kafka]
      C --- D{ }
      D -->|Reads File Notifications| E[Prompt Processing Workers]
      D -->|Reads File Notifications| F[Data Transfer Monitoring]

      style D width:0px,height:0px,display:none

Associated Systems
==================
.. Describe other applications are associated with this applications.

The S3-File-Notifications Kafka cluster is used by Prompt Processing to identify when files are uploaded to the USDF.  The Data Transfer Monitoring application which tracks files transfers from the USDF to the Summit uses file notifications to count the files transferred.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/s3-file-notifications
   * - Vault Secrets Dev
     - N/A
   * - Vault Secrets Prod
     - N/A

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Ceph S3 creates file notifications when objects are created.  Prompt Processing uses these notifications to identify when files are uploaded to the USDF.  The Data Transfer Monitoring application which tracks files transfers from the USDF to the Summit uses file notifications to count the files transferred.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* Ceph

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

No external dependencies.

Disaster Recovery
=================
.. RTO/RPO expectations for application.

Data does not need to be retained in a Disaster Recovery event.  If data is lost or unavailable redeploy the Kafka cluster.