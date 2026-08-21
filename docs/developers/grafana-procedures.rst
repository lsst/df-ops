##################
Grafana Procedures
##################

Operations and procedures for Grafana at the USDF.

This document describes how Grafana is deployed and operated, including
its components, data sources, alerting configuration, and the day-to-day
procedures for adding data sources and building alerts.


Architecture and Dependencies
=============================

Architecture Diagram
--------------------

.. image:: MonitoringArchitecture.svg
   :alt: Architecture diagram
   :width: 100%


Grafana Deployment
------------------

* **Grafana version:** 13.1.2 (Grafana OSS).
* **Topology:** deployed in **High Availability** mode with **horizontal
  autoscaling** — multiple Grafana replicas run behind a Kubernetes
  Service, and the replica count is adjusted automatically based on
  load.
* **Alerting coordination:** the Grafana replicas form a cluster using
  the built-in **gossip protocol** (memberlist). This is what prevents
  duplicate alert notifications: when an alert fires, only one replica
  is elected to deliver the notification, while the others acknowledge
  it via the gossip layer.

.. note::

   Without the gossip protocol, each HA replica would independently
   evaluate the same alert rule and send its own Slack message,
   producing N duplicate notifications for N replicas. Keep the
   memberlist ports open between Grafana pods; failures in gossip
   convergence are the most common cause of duplicated alerts.

Components and Roles
--------------------
Grafana Server
~~~~~~~~~~~~~~
Provides the UI, dashboards, and alerting engine.

Data Sources
~~~~~~~~~~~~

* **InfluxDB** — Telegraf metrics (internal metrics from all the s3df servers) and Slurm metrics. Retention forever. Supported by S3DF

* **Prometheus** — Kubernetes metrics. Retention 1 year. Supported by S3DF

* **Loki** — additional log aggregation. Using promtail that tail logs and push it to s3. Retention forever. Supported by S3DF

* **Thanos** - New TSDB commisioned as long term solution for Prometheus. Retention forever. Supported by S3DF

* **OpenSearch** — :doc:`../usdf-applications/drp/opensearch/index` TSDB application exclusive datasource used by Rubin. Not supported by S3DF

.. note::

   Application-specific TSDBs that are **not** suported by S3DF are still
   supported at the alerting layer — we only configure their contact
   points in Grafana.

Alerting Engine
~~~~~~~~~~~~~~~

* Contact Points
* Notification Policies
* Alert Templates

Internal Dependencies
---------------------

Configuration Storage
~~~~~~~~~~~~~~~~~~~~~

Grafana persists all of its configuration (dashboards, users, folders,
data source definitions, alert rules, contact points, notification
policies, and templates) in an internal PostgreSQL database managed by
`CloudNativePG <https://cloudnative-pg.io/>`_.

* **Cluster name:** ``cnpg-grafana``
* **Namespace:** ``monitoring-system``
* **Topology:** one primary plus two replicas (HA).


.. warning::

   The Grafana database is the single source of truth for all Grafana
   configuration. Losing it means losing every dashboard, alert rule,
   contact point, and notification policy. Backups are handled by the
   same CNPG / Barman Cloud mechanism.

Infrastructure
~~~~~~~~~~~~~~

* Kubernetes ``Service`` fronting the Grafana pods in
  ``monitoring-system``.
* CNPG-managed PostgreSQL cluster ``cnpg-grafana`` (pods
  ``grafana-db-1``, ``grafana-db-2``, ``grafana-db-3``) as the Grafana
  backing store.

External Dependencies
---------------------

* **Slack API** — used for alert delivery.

Upstream and Downstream Services
--------------------------------

Upstream
~~~~~~~~

* Telegraf plugin running on each server collecting metrics using different plugins (InfluxDB metrics).
* Prometheus scrapers. Prometheus passthrough must be enabled on vcluster to expose prometheus metrics
* Promtail pushing logs. Containers must stdout/stderror information in order that promtail tail the logs

Downstream
~~~~~~~~~~

* Slack notification channels.
* Grafana dashboards consumed by users.

Data Flow
---------

#. TSDB ingest (Telegraf|Slurm → InfluxDB Storage)
#. TSDB Prometheus scrapes → Prometheus Storage.
#. Promtail → tail logs stored on each system under ``/var/log/.*`` → Loki
#. Grafana queries the data sources through the datasource connections.
#. Dashboards and alert rules evaluate the returned time series.
#. Firing alerts are routed to Contact Points by Notification Policies.
#. The gossip-coordinated Grafana cluster elects a single replica to
   send each notification.
#. Slack or email notifications are delivered.


Configuration Details
=====================
To properly show a human readable text of the time-series of the alert S3DF created
a template that automatically will be populated.

Template
---------

Template used in ``ops-usdf-alerts``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: go

   {{ define "titleslack_empty" }}{{ end }}
   {{ define "messageslack_single_fs" }}
     {{ if gt (len .Alerts.Firing) 0 }}
       {{ template "text_alert_list_firing_f" .Alerts.Firing }}
     {{ end }}
     {{ if gt (len .Alerts.Resolved) 0 }}
       {{ template "text_alert_list_resolved_r" .Alerts.Resolved }}
     {{ end }}
   {{ end }}
   {{ define "text_alert_list_firing_f" }}
     {{ range . }}
       <{{ .PanelURL }}|:warning:> {{ .Annotations.description }}
     {{ end }}
   {{ end }}

   {{ define "text_alert_list_resolved_r" }}
     {{ range . }}
       <{{ .PanelURL }}|:white_check_mark:> {{ .Annotations.descriptionresolved }}
     {{ end }}
   {{ end }}



Operational Procedures
======================

.. warning::

  If any of the TSDBs is down, alerts will be delivered with null
  values. If Grafana itself is down, **no alerts will be delivered**.

Adding and Modifying Data Source Connections
--------------------------------------------

Create a SN ticket asking to create a new datasource connection.
This datasource connection needs to specify the type of TSDB and the service in front of the TSDBs
Also provide the route in Vault for any authentication needed against the different database/index for the TSDB needed


Alerts
------

Contact Points
~~~~~~~~~~~~~~

A **Contact Point** defines the integration (Slack, email, webhook,
etc.) that will receive an alert. You must specify the destination
(for example, a Slack channel) and provide the corresponding token.

Under **Optional Slack Settings** you can configure:

* a template for the **title**
* a template for the **text body**

Define Query and Alert Condition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alerts must be based on time series. When creating an alert, the
description should include enough information about what is failing so
that the delivered template is actionable.

**Example** — track ``/tmp`` usage across all hosts, using Telegraf
disk metrics stored in InfluxDB. The query time range should be kept
short, since alerts are evaluated on a short interval.

.. code-block:: sql

   SELECT max("used_percent") FROM "disk"
   WHERE "path" = '/tmp' AND :timeFilter
   GROUP BY time(1m), "host" fill(null)

.. note::

   In InfluxQL the placeholder is written ``$timeFilter`` (with a
   ``$``). It has been rendered as ``:timeFilter``

The ``GROUP BY "host"`` clause produces one time series per host.

Always add:

* a **Reduce** expression
* a **Threshold** expression

These collapse the per-host time series into a single evaluated series,
so one alert covers many hosts instead of firing one alert per host.

To make alerts **dynamic** (rather than static text), use expressions
such as:

.. code-block:: text

  {{ $labels.host }} /tmp usage at {{ printf "%.0f" $values.B.Value }} %

These variables are populated only for the time series that is firing.

* Use ``$labels.host`` (the label name depends on your query; it may be different in yours).
* The value shown is the one from the firing series.

Set Evaluation Behaviour
~~~~~~~~~~~~~~~~~~~~~~~~

* Pick the folder where the alert rule will be stored.
* Choose the evaluation group and interval.
* Set the **pending period** — how long the condition (for example, ``/tmp`` usage above threshold) must persist before the alert fires.
* Configure **No Data** and **Error** handling:

.. note::
  If your workflow allows *no data* without generating an alert, set both to **Normal**.

Labels and Contact Point Routing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Labels determine which Contact Point delivers the alert. For example,
``facility=Rubin`` routes alerts to the ``ops-usdf-alerts`` Slack channel.

The notification message requires two annotations:

* ``description`` — used when the alert is firing.
* ``descriptionresolved`` — a custom annotation used when the alert clears (required by our templates). Unless no nothification of resolved alert is needed.

**Example** — firing description:

.. code-block:: text

  {{ $labels.host }} /tmp usage at {{ printf "%.0f" $values.B.Value }} %

**Example** — resolved description:

.. code-block:: text

  {{ $labels.host }} /tmp usage back to {{ printf "%.0f" $values.B.Value }} %

How Contact Points Relate to Notification Policies
--------------------------------------------------

In Grafana, **Contact Points** and **Notification Policies** work
together to decide *where* alerts go and *when* they are delivered.

What Contact Points Are
~~~~~~~~~~~~~~~~~~~~~~~

A Contact Point defines **how** an alert is delivered. Examples:

* Slack channel + Slack token.
* Email address.
* Webhook endpoint.

A Contact Point is **only the destination**. It does **not** decide
which alerts should go there.

What Notification Policies Are
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Notification Policy decides:

* **Which alerts** should go to which Contact Point.
* **When** alerts should be delivered.
* **How often** they should repeat.
* Whether alerts should be grouped or delayed.

Notification Policies act as routing rules.

How Alerts Are Routed
~~~~~~~~~~~~~~~~~~~~~

When an alert fires:

#. The alert includes a set of **labels** (for example,``facility=Rubin``).
#. Grafana evaluates the Notification Policies and finds the policy that matches those labels.
#. The matching policy sends the alert to the corresponding Contact Point.

**Example**

* An alert carries the label ``facility=Rubin``.
* A Notification Policy states: *"If ``facility = Rubin``, send to Contact Point ``ops-usdf-alerts-slack``."*
* Result: the alert is delivered to the Rubin Observatory ``#ops-usdf-alerts`` Slack channel.

Why Labels Matter
~~~~~~~~~~~~~~~~~

Labels are the **keys used for routing**. If a Notification Policy is
looking for ``facility=s3df``, the alert must carry that label for the
rule to match.

Labels let you:

* Send different alerts to different Slack channels.
* Separate alerts by team or system.
* Control delivery based on alert type or severity.
