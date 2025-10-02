##########
Procedures
##########

Intended audience: Anyone who is administering the application.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployment is with Phalanx and ArgoCD.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

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
