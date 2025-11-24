###############
Troubleshooting
###############

Intended audience: Anyone who is administering Prompt Redis.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - None
     -
     -

Monitoring
==========
.. Describe how to monitor application and include relevant links.

`Redis Streams KEDA Performance Dashboard <https://grafana.slac.stanford.edu/d/yKZFx0uIz/prompt-processing-redis-streams-keda-performance?orgId=1&from=now-24h&to=now&timezone=browser&var-datasource=940RXge4k&var-job=$__all&var-redis_server=$__all&var-stream=$__all&var-group=$__all&var-consumer=$__all&var-namespace=vcluster--usdf-prompt-processing>`__

No Such Group or Key Error
==========================

**Symptoms:**  A ``redis.exceptions.ResponseError: NOGROUP No such key 'instrument:lsstcam' or consumer group 'lsstcam_consumer_group' in XREADGROUP with GROUP option`` error is reported by Prompt Processing.

**Cause:**  This can happen is the Redis Cluster is recreated and the keys and consumers groups are not bootstrapped.

**Solution:**  Follow the :ref:`Creating Redis Streams` procedure to create the keys and consumer groups.

Prompt Processing Cannot Connect to Redis
=========================================

**Symptoms:**  Prompt Processing is reporting errors that it cannot connect to Redis.

**Cause:**  The internal Kubernetes DNS name of ``prompt-redis.prompt-redis`` is used to connect to Prompt Processing.

**Solution:**  Validate that the name of the service with the command below.

.. rst-class:: technote-wide-content

.. code-block:: bash

   kubectl get svc -n prompt-redis

The issue could be DNS related.  Restart the ``coredns`` deployment in the ``kube-system`` namespace with the ``kubectl rollout restart deployment coredns -n kube-system`` command which will restart the coredns pods.  If neither fixes the issue contact *usdf-infr-support* channel on Slack for assistance.

