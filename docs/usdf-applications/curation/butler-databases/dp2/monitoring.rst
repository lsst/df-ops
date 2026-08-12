##########
Monitoring
##########

Monitoring for the **DP2 Butler database** is fully automated and provided
out-of-the-box by the `CloudNativePG <https://cloudnative-pg.io/>`_ operator.
Both the PostgreSQL cluster and the PgBouncer connection pooler expose
Prometheus metrics that are scraped by the shared s3df Prometheus stack and
visualised in the central **CNPG Grafana dashboards**.

.. note::

   No per-cluster dashboard or alerting configuration needs to be maintained
   for DP2 — everything is wired up automatically as long as the CNPG
   ``PodMonitor`` is enabled and Prometheus annotations are present on the
   pods.

Overview
========

.. list-table::
   :widths: 35 65

   * - Metrics source (PostgreSQL)
     - CNPG operator sidecar on each ``dp2-db-*`` instance pod
   * - Metrics source (Pooler)
     - PgBouncer exporter on each ``dp2-db-tx-ro-*`` and ``dp2-db-tx-rw-*`` pod
   * - Scraper
     - Prometheus (S3DF shared stack)
   * - Dashboards
     - `Grafana CNPG monitoring <https://grafana.slac.stanford.edu/d/dbb4a9d9-c71c-4e8b-a2f1-f5f62ba8c0ca/cloud-native-postgresql-cnpg?orgId=1&from=now-2d&to=now&timezone=browser&var-vcluster=vcluster--usdf-butler-dp2&var-cluster_name=$__all&var-instances=$__all&refresh=1m>`_
   * - Alerts destination
     - Slack channel ``#ops-usdf-alerts``

How Metrics Are Exposed
=======================

PostgreSQL cluster
------------------

The ``Cluster`` resource enables the built-in CNPG ``PodMonitor`` and
propagates the standard Prometheus scrape annotations to every instance pod:

.. code-block:: yaml

   apiVersion: postgresql.cnpg.io/v1
   kind: Cluster

   spec:
     monitoring:
       enablePodMonitor: true

What this does:

* ``monitoring.enablePodMonitor: true`` — the operator creates a
  ``PodMonitor`` object in the ``dp2`` namespace that Prometheus discovers
  automatically.

* ``pg_stat_statements`` is enabled in ``postgresql.parameters``
  (``pg_stat_statements.track: "all"``, ``pg_stat_statements.max: "10000"``),
  providing per-query performance metrics through the CNPG exporter.

Connection pooler (PgBouncer)
-----------------------------

The read-only pooler exposes PgBouncer metrics in the same way:

.. code-block:: yaml

   apiVersion: postgresql.cnpg.io/v1
   kind: Pooler

   spec:
     template:
       metadata:
         annotations:
           prometheus.io/scrape: "true"
         labels:
           app: pooler


The CNPG operator injects the PgBouncer metrics exporter into each pooler
pod, so no additional configuration is required.

Dashboards
==========

Typical panels available:

* Cluster status (primary / replica / standby)
* Transactions per second (commit vs rollback)
* Active / idle / waiting backend connections
* Replication lag (bytes and time)
* WAL generation and archive rate
* Buffer cache hit ratio
* Slow queries via ``pg_stat_statements``
* PgBouncer client and server pool utilisation


Alerts
======

Alerting is centrally managed by the CNPG monitoring stack. **DP2 does not
require any per-cluster alert configuration.** Alerts are routed to Slack:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Event
     - Notification
   * - Failover (primary → replica promotion)
     - ``#rubin-alert-channel``
   * - Switchover events
     - ``#rubin-alert-channel``
   * - WAL archiving failures
     - ``#rubin-alert-channel``
   * - Instance unavailability / pod restarts
     - ``#rubin-alert-channel``

.. note::

   Failover and switchover behaviour for DP2 is governed by the timing
   parameters below (from the ``Cluster`` spec). These affect how quickly
   an alert fires:

   * ``failoverDelay: 30`` — seconds before a failed primary is failed over.
   * ``switchoverDelay: 360`` — max seconds allotted to a graceful
     switchover.
   * ``smartShutdownTimeout: 120`` — seconds allowed for a smart shutdown.
   * ``stopDelay: 240`` — seconds before a hard stop.

Verifying Monitoring Is Working
===============================

Check that the ``PodMonitor`` CR exists:

.. code-block:: bash

   kubectl get podmonitors.monitoring.coreos.com

If CR does not exist, submit a ServiceNow ticket asking to enable prometheus
passthrough to that particular vcluster.

Cluster-level status is also available through the CNPG plugin:

.. code-block:: bash

    kubectl cnpg status dp2-db -n dp2

    Cluster Summary
    Name                     dp2/dp2-db
    System ID:               7665540757235400732
    PostgreSQL Image:        ghcr.io/lsst-sqre/cnpg-postgres-images:17.5
    Primary instance:        dp2-db-1
    Primary promotion time:  2026-07-23 02:13:28 +0000 UTC (480h51m27s)
    Status:                  Cluster in healthy state
    Instances:               2
    Ready instances:         2
    Size:                    71G
    Current Write LSN:       8F/2F000000 (Timeline: 1 - WAL File: 000000010000008F0000002F)

    Continuous Backup status (Barman Cloud Plugin)
    ObjectStore / Server name:      dp2-db-objectstore/dp2-db
    First Point of Recoverability:  2026-08-04 06:18:24 -05
    Last Successful Backup:         2026-08-11 06:18:21 -05
    Last Failed Backup:             -
    Working WAL archiving:          OK
    WALs waiting to be archived:    0
    Last Archived WAL:              000000010000008F0000002E   @   2026-07-28T23:32:09.129609Z
    Last Failed WAL:                00000001000000000000000C   @   2026-07-24T01:20:10.002131Z

    Streaming Replication status
    Replication Slots Enabled
    Name      Sent LSN     Write LSN    Flush LSN    Replay LSN   Write Lag  Flush Lag  Replay Lag  State      Sync State  Sync Priority  Replication Slot
    ----      --------     ---------    ---------    ----------   ---------  ---------  ----------  -----      ----------  -------------  ----------------
    dp2-db-2  8F/2F000000  8F/2F000000  8F/2F000000  8F/2F000000  00:00:00   00:00:00   00:00:00    streaming  async       0              active

    Instances status
    Name      Current LSN  Replication role  Status  QoS        Manager Version  Node
    ----      -----------  ----------------  ------  ---        ---------------  ----
    dp2-db-1  8F/2F000000  Primary           OK      Burstable  1.30.0           sdfk8sc036
    dp2-db-2  8F/2F000000  Standby (async)   OK      Burstable  1.30.0           sdfk8sc049

    Plugins status
    Name                            Version  Status  Reported Operator Capabilities
    ----                            -------  ------  ------------------------------
    barman-cloud.cloudnative-pg.io  0.13.0   N/A     Reconciler Hooks, Lifecycle Service, TYPE_INSTANCE_SIDECAR_INJECTION
