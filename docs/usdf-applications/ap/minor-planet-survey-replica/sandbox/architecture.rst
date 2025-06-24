#######################################
MPC Sandbox Architecture & Dependencies
#######################################

Configuration
=============
SQL configuration is stored

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
The ``mpc-sandbox`` depends on Internet connectivity to receive updates from the MPC.  The SLAC IP ``134.79.23.9`` was shared with the MPC Annex as the NAT addresses used for outbound connectivity with SLAC.  If this address changes the MPC Annex will need to be notified.
