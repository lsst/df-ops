#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

HTCondor is installed as a service on the Rubin development nodes (``rubin-devl``) with Ansible.  The HTCondor central collector service is installed on ``sdfiana12``.  If there is a failure on ``sdfiana12`` then the central collector is installed on ``sdfiana13``.

HTCondor interfaces with Slurm and creates a Condor Pool on the Slurm nodes.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Associated Systems
==================
.. Describe other applications are associated with this applications.

`ctrl_bps_htcondor <https://github.com/lsst/ctrl_bps_htcondor>`__ is a HTCondor pluguin for LSST PipelineTask execution.  HTCondor interacts with Slurm for job execution.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     -
   * - Vault Secrets Dev
     - None
   * - Vault Secrets Prod
     - None

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* Weka Filesystem for data for jobs.  HTCondor can run without Weka, but would have no data for jobs.
* Slurm
* Rubin Development Nodes.  ``sdfiana12`` is most important because it runs the HTCondor central collector service
* CVMFS Software stack

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

No external dependencies. HTCondor is currently not integrated with multi-site processing.

Disaster Recovery
=================
.. RTO/RPO expectations for application.
