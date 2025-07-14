##################
MPCorb Information
##################

The database is installed in the ``usdf-minor-planet-survey`` Kubernetes vCluster in the ``mpcorb-replica`` namespace.

Usage
=====

Access
======
Credentials are in Vault at ``vault kv get secret/rubin/minor-planet-survey``

Diagram
=======

Data Flow
=========

Configuration
=============
SQL configuration is stored in the GitHub Repo and secrets are stored in Vault.

S3DF Dependencies
=================
  * Kubernetes
  * SLAC LDAP to authenticate to the vCluster
  * Internet connectivity to receive logical replication updates.  Access is tied to the SLAC NAT address of ``134.79.23.9``
  * DNS resolution for the SBN address
  * Weka storage for Kubernetes.  The database uses a persistent volume claim.

Associated Systems
==================

Network
=======
The ``mpcorb-replica`` depends on Internet connectivity to receive updates from the MPC Annex.  The SLAC IP ``134.79.23.9`` was shared with the MPC Annex as the NAT addresses used for outbound connectivity with SLAC.  If this address changes the MPC Annex will need to be notified.
