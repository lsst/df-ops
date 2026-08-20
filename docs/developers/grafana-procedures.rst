##################
Grafana Procedures
##################

Operations and procedures for Grafana at the USDF.

.. warning::

  If any of the TSDBs is down, alerts will be delivered with null
  values. If Grafana itself is down, **no alerts will be delivered**.

Adding and Modifying Data Source Connections
============================================

Create a Jira task in the USDFSM space asking to create a new datasource connection.
This datasource connection needs to specify the type of TSDB and the service in front of the TSDBs
Also provide the route in Vault for any authentication needed against the different database/index for the TSDB needed


Adding an Alert
===============

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
