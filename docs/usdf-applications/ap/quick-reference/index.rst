.. _alert-production-ops-reference:

##############################################
Alert Production — Operational Quick Reference
##############################################

.. contents:: On This Page
   :depth: 2
   :local:

Overview
========

**Service Group**: Alert Production |br|
**Service Tier**: Real Time — failures during observing directly block alert delivery |br|
**Operating Hours**: Nightly observing windows (Chilean night) |br|
**Primary vCluster**: ``usdf-prompt-processing`` (prod) / ``usdf-prompt-processing-dev`` (dev) |br|
**Primary Slack Channel**: ``#lsstcam-prompt-processing`` |br|
**Phalanx ArgoCD**: https://phalanx.lsst.io/applications/prompt.html

.. |br| raw:: html

   <br/>

Pod-Internal Processing Phases
==============================

Each KEDA Scaled Job Pod executes these phases in sequence per visit-detector.

.. note::

   The boundaries between phases are not perfectly sequential. In particular:
   alert packets are sent to Alert Distribution *during* the pipeline phase (before export),
   and Sasquatch metrics dispatch happens *after* export. The table below does not necessarily reflect the
   actual ordering but is a good approximation.

.. list-table::
   :widths: 5 15 30 25 25
   :header-rows: 1

   * - #
     - Phase
     - What Happens
     - Reads From
     - Writes To
   * - 1
     - **Scaled Job Start**
     - Pod starts, consumes a fanned-out event from Redis Stream ``instrument:lsstcam`` with ``lsstcam_consumer_group``.
     - Prompt Redis
     - (nothing)
   * - 2
     - **Preload**
     - Loads a local Butler from a read-only replica of Embargo Butler. Reads calibration data from embargo storage (Ceph) and templates from Weka (``/sdf/data/rubin/templates/``). Queries APDB for pre-existing detections in the visit-detector region. *After preload completes*, queries the Presence microservice for image URLs and listens for ``objectCreated`` events from S3 File Notifications Kafka to confirm raw image arrival.
     - Embargo Butler RO replica, Embargo storage (Ceph — calibrations), Weka (templates), APDB (Cassandra), Presence microservice, S3 File Notifications Kafka
     - Local Repo (pod-local)
   * - 3
     - **Alert Production Pipeline**
     - Runs difference imaging, source detection, association. Queries Sattle to filter satellite trails from DIASources (per DMTN-199 policy — if Sattle is unavailable, no alerts are transmitted). Sends alert packets to Alert Distribution Service during this phase.
     - APDB, Sattle
     - APDB (new DIASources), Local Repo, Alert Distribution Service (alert packets)
   * - 4
     - **Export Outputs**
     - Sends dataset records (processed data) as Kafka messages to Prompt Kafka. Writes outputs to embargo storage. Dispatches metrics to Sasquatch via REST Proxy (after export).
     - Local Repo
     - Prompt Kafka (dataset records), Embargo storage, Sasquatch (metrics)
   * - 5
     - **Loop / Terminate**
     - Listens for another Redis Stream event. If no new event arrives before timeout, the Scaled Job terminates. This avoids churn from creating new pods for each event.
     - Prompt Redis
     - (nothing)

Complete Service Inventory
==========================

The following table lists **every service** required for Alert Production to function, their runtime details, and monitoring status. Services are listed in data flow order.

.. list-table::
   :widths: 14 7 12 10 10 35 12
   :header-rows: 1

   * - Service
     - Tier
     - vCluster / Host
     - K8s Namespace
     - Slack Channel
     - Grafana Dashboards
     - Doc Gaps
   * - **Next Visit Fan Out**
     - Real Time
     - usdf-prompt-processing
     - next-visit-fan-out
     - lsstcam-prompt-processing
     - ✅ Incorporated into PP Production dashboards. Alerts configured for Kafka and Schema Registry connectivity.
     -
   * - **Prompt Redis**
     - Real Time
     - usdf-prompt-processing
     - prompt-redis
     - lsstcam-prompt-processing
     - ✅ `Redis Streams KEDA Performance <https://grafana.slac.stanford.edu/d/yKZFx0uIz/prompt-processing-redis-streams-keda-performance>`__
     -
   * - **Prompt KEDA**
     - Real Time
     - usdf-prompt-processing
     - keda
     - lsstcam-prompt-processing
     - ✅ `Redis Streams KEDA Performance <https://grafana.slac.stanford.edu/d/yKZFx0uIz/prompt-processing-redis-streams-keda-performance>`__
     -
   * - **Prompt Processing** (KEDA Scaled Jobs)
     - Real Time
     - usdf-prompt-processing
     - prompt-keda-lsstcam
     - lsstcam-prompt-processing
     - ✅ `Production Overview <https://grafana.slac.stanford.edu/d/feifuf82d6tj4f/prompt-processing-production-overview>`__ ✅ `Output <https://grafana.slac.stanford.edu/d/nk1zxv84z/prompt-processing-production-output>`__ ✅ `I/O Timing <https://grafana.slac.stanford.edu/d/eeimq740rdgjkf/prompt-processing-production-i-o-timing>`__ ✅ `Statistics <https://grafana.slac.stanford.edu/d/c0a9c6d3-4ea8-452d-bb91-962304c1b0d2/prompt-processing-production-statistics>`__
     -
   * - **Prompt Kafka**
     - Real Time
     - usdf-prompt-processing
     - prompt-kafka
     - lsstcam-prompt-processing
     - ⚠️ `Strimzi Kafka Dashboard <https://grafana.slac.stanford.edu/d/86cc98e66c294b299b37102f0cc74ead2/strimzi-kafka>`__
     - Dashboard now functional for dev. Verify prod once PodMonitor is added.
   * - **Butler Writer**
     - Real Time
     - usdf-prompt-processing
     - butler-writer-service
     - *(none)*
     - ⚠️ **None documented**
     - No dashboard, no Slack channel
   * - **APDB (Cassandra)**
     - Real Time
     - bare-metal: sdfk8sk001-006 (prod), sdfk8sk007-012 (dev)
     - N/A
     - ops-apdb-alerts
     - ✅ `Cassandra System Metrics <https://grafana.slac.stanford.edu/d/d7d52e6b-e376-49dc-8ef8-e4742dd229a9/cassandra-system-metrics>`__
     -
   * - **Sattle** (Satellite Catalog)
     - Real Time
     - Embargo Rack (systemd, 2× HA)
     - N/A (not in K8s)
     - *(none)*
     - ⚠️ **None** — logs to local disk only
     - No dashboard, no Slack, no centralized logs, no K8s visibility
   * - **S3 File Notifications Kafka**
     - Real Time
     - usdf-prompt-processing
     - s3-file-notifications
     - usdf-infra-support
     - ⚠️ **None documented**
     - Part of Data Curation group but critical path for AP
   * - **Embargo Transfer / Presence** (Auto-Ingest)
     - Real Time
     - usdf-embargo-dmz
     - summit-new *(LSSTCam data)*
     - usdf-data-curation
     - ⚠️ **None** — metrics in internal Redis, not published externally
     - PP only directly uses Presence microservice (not the ingest workers)
   * - **USDF Sasquatch**
     - Real Time
     - usdf-rsp
     - sasquatch
     - usdf-rsp-support, status-efd
     - ✅ (Sasquatch has its own dashboards)
     - PP publishes metrics via REST Proxy; Schema Registry IP changes are a known issue
   * - **Alert Distribution Service**
     - Real Time
     - usdf-alert-stream-broker-dev *(prod vCluster not documented)*
     - alert-stream-broker
     - *(none)*
     - ⚠️ **None documented**
     - Prod vCluster, dashboard, Slack all missing. Note: "Alert Stream Broker" and "Alert Distribution" are the same service.
   * - **Alert Archive**
     - Critical
     - usdf-alert-stream-broker-dev *(prod vCluster not documented)*
     - alert-stream-broker
     - *(none)*
     - ⚠️ **None documented**
     - Daytime ops only. Prod vCluster, dashboard, Slack all missing.


Infrastructure Dependencies
============================

Every dependency required for nightly alert production, rated by failure impact.

.. list-table::
   :widths: 22 18 10 50
   :header-rows: 1

   * - Dependency
     - Consumed By
     - Severity
     - Impact Description
   * - **LHN (Long Haul Network)**
     - Next Visit Fan Out
     - ❌ HALT
     - No nextVisit events reach USDF from Summit. Total pipeline halt.
   * - **Summit Sasquatch Kafka**
     - Next Visit Fan Out (via socat)
     - ❌ HALT
     - No nextVisit events produced by ScriptQueue. Total pipeline halt.
   * - **socat proxy** (``kafka-proxy`` ns)
     - Next Visit Fan Out
     - ❌ HALT
     - DNS in ``kube-system`` ConfigMap routes Summit Kafka addresses to socat. If socat is down, NVFO cannot consume events.
   * - **Kubernetes Cluster + Embargo Nodes**
     - All K8s-based AP services
     - ❌ HALT
     - Nothing runs. Total pipeline halt. PP runs on dedicated embargo nodes.
   * - **SLAC LDAP**
     - vCluster authentication
     - ⚠️ DEGRADED
     - Processing continues normally. However, cluster can only be accessed via an S3DF person — no vCluster authentication for Rubin staff. New deployments/syncs may fail.
   * - **Ceph ``rubin-summit`` bucket**
     - S3 File Notifications, Embargo Transfer
     - ❌ HALT
     - Raw images not stored or accessible. Processing cannot start.
   * - **Embargo Storage (Ceph)**
     - Prompt Processing (preload — calibration data), Export (output writes)
     - ❌ HALT
     - PP reads calibration data from embargo storage during preload and writes outputs during export. Ceph unavailable = preload fails, export fails.
   * - **S3 File Notifications Kafka**
     - Prompt Processing pods
     - ❌ HALT
     - Presence microservice is only queried once after preload and is not consulted again. If S3 File Notifications Kafka is down, PP will not receive ``objectCreated`` events and will not run any pipelines.
   * - **Presence Microservice** (part of Embargo Transfer)
     - Prompt Processing
     - ⚠️ DEGRADED
     - PP queries Presence once after preload to check if images have already arrived. If Presence is unavailable, PP still works via S3 File Notifications Kafka. Note: PP does not directly depend on auto-ingest workers, only on Presence.
   * - **Embargo Butler DB (PostgreSQL)**
     - Prompt Processing (preload), Butler Writer
     - ❌ HALT
     - Cannot load Butler or write results. Preload fails.
   * - **Cassandra Cluster (APDB)**
     - Prompt Processing (preload + pipeline)
     - ❌ HALT
     - Cannot read previous detections or write new DIASources. 6 prod nodes, 12 total. Backups via ``cassandra-medusa`` to S3.
   * - **Weka** ``/sdf/data/rubin/templates/``
     - Prompt Processing (preload)
     - ❌ HALT
     - Cannot load templates. Processing fails immediately. Note: calibration data is stored separately in embargo storage (Ceph), not on Weka.
   * - **Sattle** (Embargo Rack)
     - Prompt Processing (pipeline)
     - ❌ HALT
     - Per DMTN-199 policy (Sec. 3.4): alerts are **not transmitted** if Sattle does not succeed. No Sattle = no alerts.
   * - **Sasquatch (USDF RSP)**
     - Prompt Processing (pipeline metrics)
     - ⚠️ DEGRADED
     - Metrics publication fails but processing continues. Known issue: Schema Registry IP changes during Sasquatch maintenance.
   * - **Vault**
     - All services needing secrets
     - ⚠️ ON REDEPLOY
     - Secrets cached at deploy time. Running services unaffected. New deploys/syncs will fail.
   * - **Internet connectivity**
     - Alert Distribution Service (outbound to brokers), Sattle (space-track.org)
     - ❌ HALT
     - Alerts cannot reach community brokers. Sattle catalog update from space-track.org fails — stale catalog means Sattle may refuse to clear alerts, leading to halt.

Kubernetes Observability
========================

.. list-table::
   :widths: 22 12 38 28
   :header-rows: 1

   * - What to Watch
     - Tool
     - Dashboard / Command
     - Notes
   * - Pod status (all AP namespaces)
     - Grafana
     - `K8s Workload State <https://grafana.slac.stanford.edu/d/dd71bcda-7744-4a86-bb10-f3cb65a1255c/kubernetes-workload-state>`__
     - Filter by ``vcluster--usdf-prompt-processing``. Check for CrashLoopBackOff, OOMKilled.
   * - Scaled Job count & scaling
     - kubectl / Grafana
     - ``kubectl get jobs -n prompt-keda-lsstcam`` |br| KEDA Performance dashboard
     - Should scale up ~20s before exposures. ``keda_scaler_active=1`` means scaling is working.
   * - KEDA scaler health
     - Prometheus
     - ``keda_scaler_active``, ``keda_scaler_metrics_latency_seconds``, ``keda_scaled_job_errors_total``
     - High latency suggests Redis Streams scaler is slow. Errors may indicate API connectivity issues.
   * - Redis Stream lag
     - Grafana
     - Redis Streams KEDA Performance dashboard
     - ``pendingEntriesCount`` in ``instrument:lsstcam`` stream with ``lsstcam_consumer_group``. Should clear after processing.
   * - Processing throughput
     - Grafana
     - PP Production Overview + Output dashboards
     - Check per-visit processing time, error rate, alert count per visit.
   * - Prompt Kafka health
     - Grafana / kubectl
     - `Strimzi Kafka Dashboard <https://grafana.slac.stanford.edu/d/86cc98e66c294b299b37102f0cc74ead2/strimzi-kafka>`__ |br| ``kubectl get pods -n prompt-kafka`` |br| ``kubectl get kafkas -n prompt-kafka``
     - Filter by ``vcluster--usdf-prompt-processing`` namespace.
   * - Butler Writer throughput
     - kubectl logs
     - ``kubectl logs -l app=butler-writer -n butler-writer-service``
     - ⚠️ No dashboard. Monitor for batch insert errors, connection timeouts to Embargo Butler.
   * - Cassandra cluster health
     - Grafana
     - Cassandra System Metrics dashboard
     - 6 prod nodes (sdfk8sk001-006). Alerts configured to ``#ops-apdb-alerts``.
   * - S3 File Notifications
     - kubectl
     - ``kubectl get pods -n s3-file-notifications``
     - ⚠️ No dashboard. Three brokers for redundancy. No auth/SSL (Ceph limitation).
   * - Embargo Transfer / Presence
     - kubectl
     - ``kubectl get pods -n summit-new`` (on usdf-embargo-dmz — LSSTCam data)
     - ⚠️ Metrics in internal Redis, not published externally. PP only depends on Presence microservice.
   * - Sattle health
     - SSH / systemd
     - ``systemctl status sattle`` on Embargo Rack hosts
     - ⚠️ No K8s or Grafana. Bare-metal only. Check both HA nodes.
   * - socat proxy
     - kubectl
     - ``kubectl get pods -n kafka-proxy`` |br| ``kubectl get configmap -n kube-system``
     - Verify DNS entries resolve Summit Kafka addresses to socat services.
   * - CoreDNS (vCluster)
     - kubectl
     - ``kubectl get pods -n kube-system -l k8s-app=kube-dns``
     - DNS failures break inter-service connectivity. Restart: ``kubectl rollout restart deployment coredns -n kube-system``.

Known Issues & Failure Modes
============================

Documented failure modes from the troubleshooting runbooks:

.. list-table::
   :widths: 22 38 40
   :header-rows: 1

   * - Issue
     - Symptom
     - Resolution
   * - **Missing raw data at USDF**
     - PP workers time out waiting for images. No data in embargo bucket.
     - Upstream issue (Summit transfer). PP auto-skips after timeout.
   * - **Missing fanned-out events**
     - No fanned-out events received in Redis Stream. KEDA doesn't scale.
     - Check Next Visit Fan Out pods. Check socat proxy. Check Summit Sasquatch.
   * - **Schema Registry IP change**
     - ``RegistryBadRequestError (404)`` or ``httpx.ConnectError`` in NVFO logs.
     - Get new IP: ``kubectl get service sasquatch-schema-registry -n sasquatch`` on RSP vCluster. Update ``schemaRegistryUrl`` in `NVFO values file <https://github.com/lsst-sqre/phalanx/blob/main/applications/next-visit-fan-out/values-usdfprod-prompt-processing.yaml>`__, PR, merge, ArgoCD sync.
   * - **Missing file arrival notifications**
     - Bucket notifications silently disabled. PP will not run pipelines — S3 File Notifications Kafka is essential (HALT). Presence is only queried once after preload and cannot substitute for ongoing S3 notifications.
     - Reconfigure Ceph bucket notifications if not a wider storage issue. This is a HALT-level failure.
   * - **Missing dataset types**
     - New dataset types not registered in ``embargo`` Butler.
     - Manual registration: `playbook <https://github.com/lsst-dm/prompt_processing/blob/main/doc/playbook.rst#adding-new-dataset-types>`__.
   * - **Stack version mismatch**
     - Auto-ingest and PP running different stack versions. Write conflicts.
     - Auto-ingest may need stack version update.
   * - **KEDA cannot connect to K8s API**
     - KEDA log errors about API connectivity.
     - Restart KEDA operator. If persists: restart ``coredns`` in ``kube-system`` or restart vCluster syncer. Escalate to ``#usdf-infra-support``.
   * - **Redis NOGROUP error**
     - ``redis.exceptions.ResponseError: NOGROUP No such key 'instrument:lsstcam'``
     - Redis cluster was recreated. Run the **Creating Redis Streams** procedure to recreate keys and consumer groups.
   * - **PP cannot connect to Redis**
     - Connection errors to ``prompt-redis.prompt-redis``.
     - Verify ``kubectl get svc -n prompt-redis``. May be DNS — restart ``coredns``. Escalate to ``#usdf-infra-support``.
   * - **Images rejected as unprocessable**
     - Inconsistency between nextVisit and actual exposure. Missing metadata.
     - Upstream issue. PP raises RuntimeError, skips the image.
   * - **PipelineExecutionError**
     - Errors from pipeline payload (science code), framework is working correctly.
     - Non-urgent. Report to Pipelines team.
   * - **Prompt service bugs**
     - Major regression in stack or middleware.
     - Rollback to previously working version. Report to PP team.

Observability Gaps — Priority Action Items
==========================================

Services that are **Real Time critical** but lack adequate observability:

.. list-table::
   :widths: 22 10 68
   :header-rows: 1

   * - Service
     - Priority
     - What's Missing & Recommended Actions
   * - **Next Visit Fan Out**
     - 🟡 MEDIUM
     - Now incorporated into PP Production dashboards with alerts for Kafka and Schema Registry connectivity. Kafka dashboard panels not yet populated — investigating with infra. **Still need**: event throughput per detector, socat proxy latency, reconnection events.
   * - **Prompt Kafka**
     - 🟡 MEDIUM (improved)
     - `Strimzi Kafka Dashboard <https://grafana.slac.stanford.edu/d/86cc98e66c294b299b37102f0cc74ead2/strimzi-kafka>`__ now functional on dev after adding Kafka resource PodMonitor. Being rolled out to prod. **Still need once prod is live**: ``butler-writer`` topic lag, ``butler-writer-ingestion-events`` topic lag, partition status, under-replicated partitions.
   * - **Butler Writer**
     - 🔴 HIGH
     - No Grafana dashboard, no Slack channel. **Need**: batch insert throughput, error rate, Embargo Butler DB connection pool health, queue depth.
   * - **Sattle**
     - 🔴 HIGH
     - No centralized monitoring. Bare-metal with local logs only. **Need**: request latency, error rate, satellite catalog freshness (time since last space-track.org sync), HA failover status, centralized log shipping.
   * - **S3 File Notifications Kafka**
     - 🟡 MEDIUM
     - No dashboard. **Need**: broker health, notification throughput, consumer lag for PP workers.
   * - **Embargo Transfer / Presence**
     - 🟡 MEDIUM
     - Internal Redis metrics not published. PP only directly depends on Presence microservice. **Need**: presence microservice latency and availability, ingestion throughput, worker error rate, queue depth.
   * - **Alert Distribution Service**
     - 🟡 MEDIUM
     - No dashboard, no Slack channel, prod vCluster not documented. **Need**: alert throughput, broker connection count, consumer lag per community broker.
   * - **Alert Archive**
     - 🟡 MEDIUM
     - No dashboard, no Slack channel. Daytime service, not on nightly critical path.

Deployment Repos & Configuration
=================================

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Service
     - Deployment / Config Repo
     - Vault Secrets (Prod)
   * - Prompt Processing
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/prompt-keda-lsstcam
     - ``secret/rubin/usdf-prompt-processing/prompt-processing``
   * - Next Visit Fan Out
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/next-visit-fan-out
     - ``secret/rubin/usdf-prompt-processing/next-visit-fan-out``
   * - Prompt Redis
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/prompt-redis
     - *(no secrets)*
   * - KEDA
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/keda
     - ``secret/rubin/usdf-prompt-processing/prompt-keda``
   * - Prompt Kafka
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/prompt-kafka
     - ``secret/rubin/usdf-prompt-processing/prompt-kafka``
   * - Butler Writer
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/butler-writer-service
     - *(not documented)*
   * - S3 File Notifications
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/s3-file-notifications
     - *(no secrets)*
   * - Embargo Transfer
     - ``slaclab/usdf-embargo-deploy``
     - ``rubin/usdf-embargo-dmz/{namespace}``
   * - Alert Distribution Service
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/alert-stream-broker
     - *(not documented)*
   * - APDB (Cassandra)
     - https://github.com/lsst-dm/dax_apdb_deploy
     - ``rubin/usdf-apdb-dev/apdb-prod``
   * - Sattle
     - https://github.com/lsst-dm/sattle
     - *(on-host, not in Vault)*


**Source Code Repos**:

- Prompt Processing: https://github.com/lsst-dm/prompt_processing
- Next Visit Fan Out: https://github.com/lsst-dm/next_visit_fan_out
- Butler Writer: https://github.com/lsst-dm/prompt_processing_butler_writer
- APDB: https://github.com/lsst/dax_apdb
- Sattle: https://github.com/lsst-dm/sattle
- Alert Archive: https://github.com/lsst-dm/alert_database_server
- Alert Distribution Service: https://github.com/lsst-dm/alert_database_ingester

Slack Channels
==============

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Channel
     - Purpose
   * - ``#lsstcam-prompt-processing``
     - Primary channel for AP/PP operations (Prompt Processing, NVFO, Redis, KEDA, Kafka)
   * - ``#ops-apdb-alerts``
     - Automated Cassandra alerts from Grafana
   * - ``#usdf-data-curation``
     - Embargo Transfer / Auto-Ingest support
   * - ``#usdf-infra-support``
     - Kubernetes / vCluster / DNS infrastructure escalation
   * - ``#usdf-rsp-support``
     - Sasquatch / Schema Registry support
   * - ``#status-efd``
     - EFD / Sasquatch status updates

Technical Reference
===================

**DMTN-310**: `Reducing Butler database contention in Prompt Processing <https://dmtn-310.lsst.io/>`__ — explains the Prompt Kafka / Butler Writer architecture.

**DMTN-199**: `Rubin Observatory Data Security Standards Implementation <https://dmtn-199.lsst.io/>`__ — defines data security standards including the satellite-catalog scrub policy (Sec. 3.4) implemented by Sattle.

**Key technical details**:

- **KEDA scaling strategy**: ``eager`` with ``pendingEntriesCount=1`` — one pending Redis message triggers a new Scaled Job.
- **Redis Stream naming**: ``instrument:lsstcam`` with ``lsstcam_consumer_group``.
- **Prompt Kafka topics**: ``butler-writer`` (dataset records), ``butler-writer-ingestion-events`` (ingestion events consumed by Prompt Publication Service).
- **socat proxy DNS**: ConfigMap in ``kube-system`` namespace resolves Summit Sasquatch Kafka bootstrap/broker addresses to socat services in ``kafka-proxy`` namespace.
- **Next Visit timing**: Events available ≥20s before first exposure, allowing pre-scaling.
- **Scaled Job lifecycle**: Jobs listen in a while loop; after processing, they wait for the next event. Timeout → termination. Reduces pod churn.
- **Sattle policy**: Two machines in HA on Embargo Rack (source: ``docs/usdf-applications/ap/sattle/info.rst``). Per DMTN-199 Sec. 3.4 and the Sattle ``info.rst``: the service "fails safe" — alerts are **not transmitted** if the service does not succeed. This is a halt condition, not a graceful degradation.
- **APDB backups**: ``cassandra-medusa`` to S3 bucket. Off-site backup not yet implemented. Recovery can take hours to a day.
- **Embargo Transfer recovery**: Re-trigger ingest via ``trigger_ingest.py`` in ``lsst-dm/data-curation-tools``, or ``butler ingest-raws``.
