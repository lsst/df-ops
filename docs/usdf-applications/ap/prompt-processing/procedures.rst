##########
Procedures
##########

Intended audience: Anyone who is administering Prompt Processing.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployment is with Phalanx and ArgoCD.  Details on how to sync ArgoCD are in the Prompt Processing Playbook at (https://github.com/lsst-dm/prompt_processing/blob/main/doc/playbook.rst#development-service)

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

The production hours are during observing.  Maintenance can be performed during the day and should be announced in the *lsstcam-prompt-processing* Slack channel.  For development announce on the *dm-prompt-processing* Slack channel if performing maintenance.

Backup
======
.. Procedures for backup including how to verify backups.

No backup needed.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

Validate that s3-file-notifications Kafka cluster is running for receiving file notifications.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No specific procedures are needed to cleanly shutdown.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

Deploy a new instance of a Keda Scaled Job if needed.  Note there a lot of external dependencies so it is easier to test with one the development services.
