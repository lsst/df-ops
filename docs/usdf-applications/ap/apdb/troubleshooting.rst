###############
Troubleshooting
###############

Intended audience: Anyone who is administering APDB.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * -
     -
     -

Monitoring
==========
.. Describe how to monitor application and include relevant links.

`Dashboard for production Cassandra cluster <https://grafana.slac.stanford.edu/d/d7d52e6b-e376-49dc-8ef8-e4742dd229a9/cassandra-system-metrics>`_ defines a number of graphs that reflect the state of the Cassandra and its host.
It also includes logs for Cassandra and cassandra-medusa services with levels WARNING and ERROR.

Grafana dashboard defines a number of alerts for various conditions:

- client connectivity failures, checked by a cron job every 10 minutes;
- Cassandra monitoring updates, alarm raised when metrics stop to arrive;
- Cassandra generates ``OutOfMemory`` exception;
- ZFS pool status is different from ``ONLINE``.

Alerts go to ``#ops-apdb-alerts`` Slack channel and a Pushover notification system of a responsible person.
Grafana can generate alerts for the ``dev`` and ``int`` clusters as well, but those are less critical and may happen due to those clusters being temporarily down.

A `separate Grafana dashboard <https://grafana.slac.stanford.edu/d/eescgnevzcwsga/pp-apdb-client-side-metrics?var-source=pp_apdb>`_ displays APDB-related metrics collected from Prompt Production clients.
The data for that dashboard are extracted from log files in Loki by a cron job that runs every hour.

Metrics from Cassandra hosts are sent to two InfluxDB servers:

- ``influxdb.slac.stanford.edu`` for general OS metrics,
- ``pp-influxdb.sdf.slac.stanford.edu`` - for Cassandra-specific metrics.

If one or both of those servers experiences a failure, Grafana will generate an alert due to a missing metrics data.

Logs from both Cassandra and Medusa services are sent to Loki, they can be retrieved with the query ``{compose_service="cassandra"}`` and ``{compose_service="medusa"}`` respectively.
Only a subset of Cassandra logging messages is saved in Loki to avoid overloading that service.
Recent Cassandra logs exist on each Cassandra node in folder ``/zfspool/cassandra/logs``.

.. Template to use for troubleshooting

Sample Troubleshooting
======================

**Symptoms:** "Clients connection check" alert is raised but other metrics on dashboard look healthy.

**Cause:** Occasionally cron jobs fail to run resulting in missing data.

**Solution:** Check cron host (``sdfcron001``), if unhealthy report it to USDF support.

----

**Symptoms:** "ZFS pool status" alert is raised but other metrics on dashboard look healthy.

**Cause:** One or more disks in ZFS pool have failed.

**Solution:** Logon to the node, verify pool status (``zpool status``), report to USDF support. There were cases when after a reboot two disks were in OFFLINE state, this was caused by a flaky controller card, it needs to be re-seated.

----

**Symptoms:** "Cassandra OutOfMemoryError" alert is raised.

**Cause:** Usually it is due to heavy load, e.g. too many concurrent jobs in a daily catch-up processing.

**Solution:** If possible reduce the number of concurrent clients.

----

**Symptoms:** Multiple types of alerts from a single host.

**Cause:** The host may be down or services fail to (re-)start.

**Solution:** Try to connect to the host, if it is down report to USDF support. If services are down (``docker compose ps``), restart the services. If Cassandra is in a bad state (``nodetool status``) then restart the service.

----

**Symptoms:** Alerts are generated for multiple hosts, but cluster looks healthy.

**Cause:** InfluxDB services may be down.

**Solution:** Check the state of ``influxdb.slac.stanford.edu`` and ``pp-influxdbpp-influxdb.sdf.slac.stanford.edu``, report to USDF support if any service is not accessible.
