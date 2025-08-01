##########
Procedures
##########

Intended audience: Anyone who is administering Next Visit Fan Out.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployment is through Phalanx and ArgoCD.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

Backup
======
.. Procedures for backup including how to verify backups.

No stateful data in Next Visit Fan Out.  Configs are in GitHub.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

Validate that prompt-kafka is running.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No specific procedures are needed to cleanly shutdown.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

Deployment is in Phalanx.
