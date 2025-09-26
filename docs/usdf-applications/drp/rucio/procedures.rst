##########
Procedures
##########

Intended audience: Anyone who is administering Rucio.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployment is through the Makefile and overlays in https://github.com/slaclab/rubin-rucio-deploy

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

`Rucio Transfer Monitoring Dashboard <https://grafana.slac.stanford.edu/d/YVcucApIk/rucio-transfer-monitoring?var-bin=6h&orgId=1&from=now-7d&to=now&timezone=browser&var-fts=$__all&var-dst_rse=$__all&var-src_rse=$__all&var-group_by=payload.dst-rse&var-protocol=$__all&var-filters=&var-del_rse=$__all&refresh=1m>`__


Backup
======
.. Procedures for backup including how to verify backups.

Backups of the Rucio Database are configured.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

Reproduce Service
=================
.. How to reproduce service for testing purposes.
