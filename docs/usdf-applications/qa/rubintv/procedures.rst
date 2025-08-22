##########
Procedures
##########

Intended audience: Anyone who is administering RubinTV.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployed via phalanx with the RubinTV application.  The deployment process is documented in Confluence `here <https://rubinobs.atlassian.net/wiki/spaces/DM/pages/48835912/Rapid+Analysis+RubinTV+Deployments>`__

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

Backup
======
.. Procedures for backup including how to verify backups.

No persistent data is stored in RubinTV.  The data it displays is in Embargo S3.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

RubinTV depends on a connection to Embargo S3.  If Embargo S3 is down when Kubernetes is up then RubinTV will need to be restarted.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No cold shutdown procedures needed.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

Create environment in Phalanx and deploy.
