################
Kafka Procedures
################

Intended audience: Anyone who is administering Kafka at the USDF.

.. _Upgrading Strimzi Operator:

Upgrading Strimzi Operator
==========================

Kafka clusters deployed with the Strimzi Phalanx app use the Strimzi version deployed in the Chart.  The renovate bot in the Phalanx repo updates the Strimzi version automatically.  To upgrade the Strimzi operator in ArgoCD follow the below instructions.

#. Before upgrading Strimzi, ensure that the `latest version of the operator`_ is compatible with the Kubernetes and Kafka versions running in your cluster.
#. After validating *Refresh* the Strimzi app in Phalanx and *Sync*.
#. Observe the logs for any issues with the upgrade.  If the currently deployed Kafka version is not supported by the latest operator, the operator will fail to initiate a Kafka rollout and will display an error. See :ref:`Upgrading Kafka` for instructions.

.. _Upgrading Kafka:

Upgrading Kafka
===============

The Kafka upgrade process in Phalanx is detailed below.

#. Before upgrading Kafka, ensure that the `latest version of the operator`_ is compatible with the Kubernetes and Kafka versions running in your cluster.
#. Update the values file for the environment to be upgraded.  Example below.

    .. rst-class:: technote-wide-content

    .. code-block:: yaml

       kafka:
           version: "3.9.0"

#. Deploy the change as a pull request to Phalanx.  When changes are committed run *Refresh* the ArgoCD app for your Kafka instance in Phalanx and *Sync*.

.. _Restart Kafka:

Restart Kafka
=============

A rolling update is used to restart Kafka.  To restart follow the instructions `here <https://strimzi.io/docs/operators/latest/deploying#assembly-rolling-updates-str>`__ to add an annotation to perform a rolling restart.

.. _Shutdown Kafka Gracefully:

Shutdown Kafka Gracefully
=========================

Kafka can be shutdown gracefully if needed.  To shut down gracefully, follow these steps below.  Replace the Kafka cluster name and namespaces.

#. Pause reconciliation of Strimzi resources.  This will prevent the operator from restarting the pods after they are deleted.

    .. rst-class:: technote-wide-content

    .. code-block:: bash

       kubectl annotate --overwrite Kafka <replace with Kafka cluster name> strimzi.io/pause-reconciliation="true" -n <replace with namespace>

#. Terminate the Kafka Controller and Broker Pods.

    .. rst-class:: technote-wide-content

    .. code-block:: bash

       kubectl delete StrimziPodSet <replace with name of cluster>-controller <replace with Kafka cluster name>  -n <replace with namespace>

#. After the intervention, resume reconciliation of Strimzi resources.  This will trigger the operator to start the Pods again.

    .. rst-class:: technote-wide-content

    .. code-block:: bash

       kubectl annotate --overwrite Kafka <replace with Kafka cluster name> strimzi.io/pause-reconciliation="false" -n <replace with namespace>

Add or Remove Kafka Cluster to Strimzi Operator
===============================================

Each time a new Kafka instance is added or removed the ``watchNamespaces`` configuration in Strimzi should be updated.  Below shows an example from the S3-File-Notifications Phalanx Strimzi app.  Follow the normal Phalanx and ArgoCD process to perform a pull request, *Refresh*, and *Sync* changes to apply.

.. rst-class:: technote-wide-content

.. code-block:: yaml

    watchNamespaces:
        - "prompt-kafka"
        - "s3-file-notifications"

Reserving Static IP Addresses
=============================

Once a Kafka cluster is provisioned service IP Addresses are assigned. Obtain these IPs with ``kubectl get services -n <replace with namespace of cluster>``.  Add the ``loadBalancerIP`` fields to the values file in the Phalanx for the bootstrap and the brokers.  An example is below.

.. rst-class:: technote-wide-content

.. code-block:: yaml

    externalListener:
    bootstrap:
        loadBalancerIP: 172.24.10.50
        annotations:
        metallb.io/address-pool: sdf-rubin-ingest
    brokers:
        - broker: 3
        loadBalancerIP: 172.24.10.51
        annotations:
            metallb.io/address-pool: sdf-rubin-ingest
        - broker: 4
        loadBalancerIP: 172.24.10.52
        annotations:
            metallb.io/address-pool: sdf-rubin-ingest
        - broker: 5
        loadBalancerIP: 172.24.10.53
        annotations:
            metallb.io/address-pool: sdf-rubin-ingest

.. _latest version of the operator: https://strimzi.io/downloads/