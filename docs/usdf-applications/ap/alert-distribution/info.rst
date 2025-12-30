#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

Rubin alerts are distributed by the Alert Stream service. The service is composed of an Schema Registry, Kafka messaging stream,
and a producer located in `ap_association <https://github.com/lsst/ap_association/blob/main/python/lsst/ap/association/packageAlerts.py>`_
where alerts are packaged and sent to the Kafka stream.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Associated Systems
==================
.. Describe other applications are associated with this applications.

The Alert Stream is used by the Alert Archive Ingester and the Alert Archive Server.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - GitHub Application Code Repository
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/alert-stream-broker
   * - Vault Secrets Dev
     - secret/rubin/usdf-alert-stream-broker-dev/alert-stream-broker/
   * - Vault Secrets Prod
     -

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Alerts are created and processed by the Prompt Processing pipeline. Once alerts have been generated within
`packageAlerts <https://github.com/lsst/ap_association/blob/main/python/lsst/ap/association/packageAlerts.py>`_,
they are serialized, compressed, and sent to the Kafka Alert Stream by a producer. The alerts are read into a Kafka Topic
based on the current schema used by the pipelines. These topics are made available to our downstream Community Alert Brokers. Alerts
are then held for a period of time defined in the Alert Stream Broker's
`value.yaml <https://github.com/lsst-sqre/phalanx/blob/main/applications/alert-stream-broker/charts/alert-stream-broker/values.yaml>`_
helm chart before expiring.

The Alert Archive reads active Alert Stream topics via an ingester and sends the alerts to the Alert Archive.

The `Alert Stream Schema Registry
<https://github.com/lsst-sqre/phalanx/tree/main/applications/alert-stream-broker/charts/alert-stream-schema-registry>`_
is used to serialized and deserialize the alerts.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

The following are systems hosted at USDF that the Alert Stream relies on.

* ArgoCD
* Phalanx
* Confluent Schema Registry
* Prompt Processing

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.


Disaster Recovery
=================
.. RTO/RPO expectations for application.

If any part of the Alert Stream or Schema registry has failed, follow instructions in `DMTN-214 <https://dmtn-214.lsst.io/>`_ for recovery steps.
