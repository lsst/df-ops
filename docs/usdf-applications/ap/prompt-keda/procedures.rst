##########
Procedures
##########

Intended audience: Anyone who is administering Prompt Keda.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployment is with Phalanx and ArgoCD.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

The production hours are during observing.  Maintenance can be performed during the day and should be announced in the *lsstcam-prompt-processing* Slack channel.

For development announce on the
*dm-prompt-processing* Slack channel if performing maintenance.

Backup
======
.. Procedures for backup including how to verify backups.

No backups are needed.  Configuration is stored in GitHub.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

No specific cold startup procedures.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No specific procedures are needed to cleanly shutdown.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

Deploy with Phalanx into a different vCluster or namespace.  A scaled job will need to be created to test functionality.

Upgrading KEDA Operator
=======================
To upgrade the KEDA operator perform the following.
 #. Review the `KEDA Releases <https://github.com/kedacore/keda/releases>`__ page for the correct version.
 #. Update the `KEDA Chart version <https://github.com/lsst-sqre/phalanx/blob/450e400e5ec56a4bd273547b6fa0bd06175bd976/applications/keda/Chart.yaml#L12>`__ in Phalanx with the release number.
 #. Refresh and Sync in ArgoCD

Restarting KEDA Operator
========================

To restart the keda operator run ``kubectl rollout restart deployment keda-operator -n keda``