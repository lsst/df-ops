###############################
Kubernetes Troubleshooting
###############################

Intended audience: Anyone who is administering application infrastructure at the USDF.

Known Issues
============

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - Increasing Persistent Volume does not increase storage
     - Persistent Volume sizes cannot be increased due to a limitation with vClusters.
     - Open Service Now ticket to increase the Persistent Volume size in the main cluster.  Update the application Kubernetes manifest to reflect the size so that it is the correct size if deployed from scratch later.
   * - New pod will not create
     - New pods do not create in a deployment, stateful set, or with an operator.  The pod will often not be visible in the vCluster.
     - Request in the ops-usdf-infr-support Slack channel to restart the vCluster syncer process.

Cannot Connect to Service
=========================

**Symptoms:**

**Cause:**

**Solution:**
