##########
Procedures
##########

Intended audience: Anyone who is administering the S3 File Notifications Kafka cluster.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployment is with Phalanx and ArgoCD.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

Maintenance should be announced on the #lsstcam-prompt-processing Slack channel.

Backup
======
.. Procedures for backup including how to verify backups.

No backups required.  The file notifications are not needed after they are processed.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

If the Brokers start before the Controllers restart the Controllers.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No cold shutdown procedures needed.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

Create another environment in Phalanx and deploy to a different namespace.

.. _View_Prompt_Kafdrop_Messages:

View Messages
=============

Topics and messages can be viewed in Kafdrop at:

* `Kafdrop S3 Prod <https://usdfprod-prompt-processing.slac.stanford.edu/kafdrop-s3/>`__
* `Kafdrop S3 Dev <https://usdfdev-prompt-processing.slac.stanford.edu/kafdrop-s3/>`__

Pulling Messages
================

To manually download messages for examination run the below command.  Update the IP to list the topics for dev.

.. rst-class:: technote-wide-content

.. code-block:: bash

    apptainer exec kafka_0.34.0-kafka-3.4.0.sif /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server 172.24.10.54:9094 --topic rubin-summit-notification-6 --group test-1 --from-beginning > prompt-file-notifications.txt

.. _Creating_File_Notifications:

Creating File Notifications
===========================

The ``rubin-pp-dev`` bucket is used in Prompt Processing Dev.  The ``rubin-summit`` bucket is used for Prompt Processing Prod.  To create run the commands in the shell scripts at https://github.com/slaclab/usdf-embargo-deploy/blob/main/bucket-notifications/