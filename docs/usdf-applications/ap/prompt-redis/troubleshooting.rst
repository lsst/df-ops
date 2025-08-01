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

No Such Group or Key Error
==========================

**Symptoms:**  A ``redis.exceptions.ResponseError: NOGROUP No such key 'instrument:lsstcam' or consumer group 'lsstcam_consumer_group' in XREADGROUP with GROUP option`` error is reported by Prompt Processing.

**Cause:**  This can happen is the Redis Cluster is recreated and the keys and consumers groups are not bootstrapped.

**Solution:**  Follow the :ref:`Creating Redis Streams` procedure to create the keys and consumer groups.

Prompt Processing Cannot Connect to Redis
=========================================

**Symptoms:**  Prompt Processing is reporting errors that it cannot connect to Redis.

**Cause:**  The internal Kubernetes DNS name of ``prompt-redis.prompt-redis`` is used to connect to Prompt Processing.

**Solution:**  Validate that the name of the service with ``kubectl get svc -n prompt-redis``  Example output below.

.. rst-class:: technote-wide-content

.. code-block:: bash

   kubectl get svc -n prompt-redis

   NAME           TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
   prompt-redis   ClusterIP   10.107.219.6   <none>        6379/TCP   164d

The issue could be DNS related.  Restart the ``coredns`` deployment in the ``kube-system`` namespace with the ``kubectl rollout restart deployment coredns -n kube-system`` command which will restart the coredns pods.  If neither fixes the issue contact *usdf-infr-support* channel on Slack for assistance.

