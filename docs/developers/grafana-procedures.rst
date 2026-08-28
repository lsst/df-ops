##################
Grafana Procedures
##################

Operations and procedures for Grafana at the USDF.

.. warning::

  If any of the TSDBs is down, alerts will be delivered with null
  values. If Grafana itself is down, **no alerts will be delivered**.

Request access to the Explore tab in Grafana
============================================
The **Explore** menu item in Grafana provides access to logs and to navigate metrics.  :ref:`create_snow_request` with your SLAC ID to request access to the **Explore** menu item in Grafana.

Adding and Modifying Data Source Connections
============================================

:ref:`create_snow_request` to request a new datasource connection.
This datasource connection needs to specify the type of Time Series Database (TSDB) and the service in front of the TSDBs.  Also provide the route in Vault for any authentication needed against the different database/index for the TSDB needed.

.. _creating grafana dashboard:

Creating a Dashboard or Panel
=============================

Grafana dashboard are created from the **Dashboard** menu item on the left side navigation.  When creating a dashboard save the dashboard in the **Rubin folder**.  Dashboard Documentation from Grafana is `here. <https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/create-dashboard/>`__

Labels for Filtering
====================

Pods are labeled in Kubernetes.  These labels propagate to Grafana.  Below are common labels that can be used for filtering in the Loki and Promethus Datasources.  Using appropriate filters help to reduce the data queried and improves performance.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Label
     - Description
   * - app
     - Phalanx adds a label with the name of the application
   * - container
     - Container name in kubernetes manifest
   * - namespace
     - vCluster

Adding an Alert
===============

Grafana periodically evaluates `alert <https://grafana.com/docs/grafana/latest/alerting/>`__ rules by executing data source queries and checking their conditions.  Alerts are typically configured to send a notification to a Rubin Slack channel.  In Grafana the **Rubin** folder is for alerts with Rubin services.  To create a Rubin alert in Grafana follow the instructions below.

#. See :ref:`Creating Grafana Dashboard` to create a dashboard or panel for the alert.  This will be needed later for the notification message.  If not present, the message in Slack will have a warning with an exclamation point.
#. Goto **Alerting** > **Alert Rules**
#. Select **New alert rule**
#. In **Enter alert rule name** type in the rule name.
#. Define the **query and alert condition**.  This is the query for a log, metric, or other data that will trigger the alert.  A useful option to **Preview alert rule condition** to validate against data in the system that the rule will fire.  Below are example queries for common data sources.

   * :ref:`Loki Alert Considerations`
   * :ref:`Prometheus Alert Considerations`
   * :ref:`Telegraf Alert Considerations`

#. Add **folder and labels**.  Select **Rubin** for the folder.

   * Select **Rubin** for the folder.
   * Select **Add Labels**.  Labels route to the appropriate notification policy and  contact point to deliver the alert. For example, ``facility=Rubin`` routes alerts to the ``ops-usdf-alerts`` Slack channel.

#. Set the evaluation behavior.  An evaluation group is a collection of alert rules that share a common evaluation schedule and interval.  It determines how frequently Grafana runs the queries for a set of alert rules.

   *  Set the evaluation or select **New Evaluation Group** to create  new one.
   *  Set the **Pending Period** — how long the condition (for example, usage or metric above a threshold) must persist before the alert fires.
   *  Set **Keep firing for** for how long the alert will show as firing.
   *  Configure **no data and error handling**.  This controls the behavior of the alert if there is no data.  For Loki alerts set the the state to **Normal**.   With Loki if there is no log generated the query will return no data.

#. Configure notifications.  Select a **contact point**
#. Configuration Notification message

   * For the summary
   * Enter text for the description.  The description should include enough information about what is failing so that the delivered template is actionable. This is used when the alert is firing.
   * Add a Custom annotation with the name of ``descriptionresolved``.  This is a custom annotation used when the alert clears that is required by the S3DF templates.  Below is an example.

      **Example** — firing description:

      .. code-block:: text

        {{ $labels.host }} /tmp usage at {{ printf "%.0f" $values.B.Value }} %

      **Example** — resolved description:

      .. code-block:: text

        {{ $labels.host }} /tmp usage back to {{ printf "%.0f" $values.B.Value }} %


#. **Link dashboard and panel**.  This is required for the alert to display correctly in Slack.
#. Select **Save** when complete.

.. _loki alert considerations:

Loki Alert Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~
Below is guidance for adding Loki alerts.

*  Grafana evaluates a single numeric value against a threshold.  Include ``sum by (message)``, ``count_over_time``, and ``[$interval]`` to provide a count of log messages during an interval.  An example below with areas of replacement noted.

.. code-block:: text

   sum by(message) (count_over_time({namespace="<add namespace>", container="<add container name>"}  |= "<log contents>"[$__interval]))

*  A reduce expression is needed to provide numeric value against a threshold.  A reduce function is added for **Sum** with Input of **A** or the query name with Mode **Strict**
*  In the **Threshold** set the Input to be the **Reduce** step.   **Input** from the reduce step can be set to **Is above 0** for whatever count makes sense for the alert rule.

.. _prometheus alert considerations:

Prometheus Alert Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Below is guidance for adding Prometheus alerts.

* Wrap counter metrics in functions like ``rate`` or ``increase`` before making comparisions.  Prometheus handles process restarts with these functions.
* Prometheus scraping is every 30 seconds.  Set the ``rate[window]`` to be at least 4x the scrape interval.  This will smooth out temporary spikes.

.. _telegraf alert considerations:

Telegraf Alert Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

To make alerts **dynamic** (rather than static text), use expressions
such as:

.. code-block:: text

  {{ $labels.host }} /tmp usage at {{ printf "%.0f" $values.B.Value }} %

These variables are populated only for the time series that is firing.

* Use ``$labels.host`` (the label name depends on your query; it may be different in yours).
* The value shown is the one from the firing series.

Adding Contact Points
=====================

In Grafana, **Contact Points** and **Notification Policies** work
together to decide *where* alerts go and *when* they are delivered.

A Contact Point defines **how** an alert is delivered. Examples:

* Slack channel + Slack token.
* Email address.
* Webhook endpoint.

A Contact Point is **only the destination**. It does **not** decide
which alerts should go there.

A Notification Policy decides:

* **Which alerts** should go to which Contact Point.
* **When** alerts should be delivered.
* **How often** they should repeat.
* Whether alerts should be grouped or delayed.

Notification Policies act as routing rules.

A **Contact Point** defines the integration (Slack, email, webhook,
etc.) that will receive an alert. You must specify the destination
(for example, a Slack channel) and provide the corresponding token.

Under **Optional Slack Settings** you can configure:

* a template for the **title**
* a template for the **text body**
