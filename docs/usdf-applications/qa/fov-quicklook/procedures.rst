##########
Procedures
##########

Intended audience: Anyone who is administering fov-quicklook.

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

No backup is needed.  Data references is in Butler and the rubin-summit S3 bucket.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

No cold startup procedures.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No cold shutdown procedures.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

Create new instance by creating another environment in Phalanx.