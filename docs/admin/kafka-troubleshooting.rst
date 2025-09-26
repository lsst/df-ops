#####################
Kafka Troubleshooting
#####################

Intended audience: Anyone who is administering Kafka at the USDF.

Known Issues
============

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - Kafka will not start gracefully after full hardware or power outages
     - Nodes can come up in any order.  If Kafdrop and/or Kafka brokers come up before the Raft nodes Kafka will be unhealthy.
     - Perform a rollout restart on the Kafka brokers and Kafdrop.

Investigate Kafka Restart
=========================

**Symptoms:**  Kafka has an unexplained restart that is not related to a hardware event.

**Cause:** This could be an issue with a Pod not responding or with Kafka application events.

**Solution:**  Follow the instructions `here <https://strimzi.io/docs/operators/latest/deploying#assembly-deploy-restart-events-str>`__ to identify the restart reason.
