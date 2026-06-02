###############
Troubleshooting
###############

Intended audience: Anyone who is administering the Prompt Keda.

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

`Redis Streams KEDA Performance Grafana Dashboard <https://grafana.slac.stanford.edu/d/yKZFx0uIz/prompt-processing-redis-streams-keda-performance?orgId=1&from=now-24h&to=now&timezone=browser&var-datasource=940RXge4k&var-job=$__all&var-redis_server=$__all&var-stream=$__all&var-group=$__all&var-consumer=$__all&var-namespace=vcluster--usdf-prompt-processing>`__

Included in this dashboard are the following metrics.
# ``keda_scaler_active`` Prometheus metric is set to 1 when the KEDA scalar is active and 0 when the scalar is not active.
# ``keda_scaler_metrics_latency_second`` Prometheus metric shows the latency of the KEDA Scalar.  A high latency suggests the scaler (Redis Streams for Prompt Processing) is
# ``keda_scaled_job_errors_total`` The number of errors for each Scaled Job

Full metrics are `here <https://keda.sh/docs/2.16/integrations/prometheus/>`__  Update the path to the KEDA version running to see those metrics.


KEDA Cannot Connect to Kubernetes API
=====================================

**Symptoms:** KEDA will report errors in the log that it cannot connect to the Kubernetes API.

**Cause:**  This can happen if the Kubernetes API is unavailable or there is an issue with vCluster syncer.

**Solution:**  This will sometimes correct itself.  See :ref:`restarting_keda_operator` to restart the KEDA operator.  If it does not help request for help in the *usdf-infra-support* Slack channel.  Restarting DNS in the vCluster or restarting the vCluster syncer has resolved the issue in the past.