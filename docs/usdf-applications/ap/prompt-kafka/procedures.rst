##########
Procedures
##########

Intended audience: Anyone who is administering the service.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployment is with Phalanx and ArgoCD.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

The production hours are during observing.  Maintenance can be performed during the day and should be announced in the *lsstcam-prompt-processing* Slack channel.  For development announce on the *dm-prompt-processing* Slack channel if performing maintenance.

Backup
======
.. Procedures for backup including how to verify backups.

No Kafka backups are taken.  Snapshots are done at the Weka storage level.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

Validate that both the controllers and brokers are running.  Depending on when nodes are started controllers and brokers may need to be restarted.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No specific procedures are needed to cleanly shutdown.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

Create another values file to deploy a new environment.

View Messages
=============

Topics and messages can be viewed in Kafdrop at:

* `Kafdrop S3 Prod <https://usdfprod-prompt-processing.slac.stanford.edu/kafdrop/>`__
* `Kafdrop S3 Dev <https://usdfdev-prompt-processing.slac.stanford.edu/kafdrop/>`__


Create New Kafka Topics
=======================

Kafka topics are created with Helm subcharts.  To create a new Kafka topic perform the following.

#. Create a new folder in the Phalanx repo under ``prompt-kafka/charts``.  An existing folder like ``butler-writer`` or ``prompt-publication`` could be reviewed for an example and copied.
#. Configure the topic and users Kubernetes manifests
#. Add a dependency to the ``strimzi-kafka`` chart.  Add in template.  Replace with name of subchart.

    .. rst-class:: technote-wide-content

    .. code-block:: yaml

        - name: <name of subchart>
            condition: <name of subchart>.enabled
            version: 1.0.0

#. Enable for the environment.  Add in template.  Replace with name of subchart.

    .. rst-class:: technote-wide-content

    .. code-block:: yaml

        - <name of subchart>:
            enabled: true

Restarting Kafka
================

See :ref:`Restart Kafka`

Upgrading Kafka
===============

See :ref:`Upgrading Kafka`

Upgrading Strimzi Operator
==========================

See :ref:`Upgrading Strimzi Operator`