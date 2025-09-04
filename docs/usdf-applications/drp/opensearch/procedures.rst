##########
Procedures
##########

Intended audience: Anyone who is administering OpenSearch.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployment is with a Makefile at https://github.com/slaclab/rubin-opensearch-deploy

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

Backup
======
.. Procedures for backup including how to verify backups.

No application level backups are configured in OpenSearch.  Backups and restores are done are through the Kubernetes PVCs in Weka.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

No specific cold startup procedures needed.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No specific cold shutdown procedures.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

Specify a different cluster of namespace to install using the Makefile.