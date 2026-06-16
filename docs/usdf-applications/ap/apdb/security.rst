########
Security
########


Requesting Access
=================
.. How to request access to the application.

There are two types of access to APDB Cassandra service:

- Regular APDB clients, which is an Alert Production pipeline.
- Service management controlling the service itself.

Regular clients access APDB through a Python API defined and implemented in ``dax_apdb`` package.
Clients need to have credentials of a regular Cassandra account, these are defined in ``~/.lsst/db-auth.yaml`` file, its contents can be retrieved from the Vault.

Management of APDB cluster is done via Ansible which uses SSH for connecting to cluster nodes.
To be able to manage APDB services that run on Cassandra cluster nodes one needs to:

- Have their Kerberos principal added to ``$HOME/.k5login`` of the service account on Cassandra nodes (see below). This is managed by USDF IT, send a message to ``usdf-help@slac.stanford.edu``.
- Have their account enabled on all Cassandra cluster nodes and have ``sudo`` privileges, also managed by USDF IT.
- Have access to the Vault secrets and a valid Kerberos ticket

Cassandra nodes do not have shared home directories for users, to simplify access to the nodes it is advisable to create home directory on each Cassandra node and populate ``~/.k5login``.
This can be done with Ansible from ``dax_apdb_deploy`` package, e.g. for ``prod`` cluster:

.. code-block:: bash

   # Create home directory on remote with correct ownership, directory is the same as on a local host.
   ansible all -i inventory/apdb_prod.yaml -u $USER -b -K -m shell -a "mkdir -p ${HOME}; chown $USER ${HOME}"

   # Create .k5login with user principal.
   ansible all -i inventory/apdb_prod.yaml -u $USER -k -m shell -a "echo ${USER}@SLAC.STANFORD.EDU > ${HOME}/.k5login"

And verify that SSH to any cluster host works without asking for a password after that.

Service accounts
================
.. Describe Kubernetes, Database, or Application Service accounts used by the application.

All APDB services on each cluster node run in Docker containers, the service account ``rubincas`` manages those containers.
This account is restricted to nodes dedicated to Cassandra clusters, USDF IT controls the setup of those nodes.

The nodes belonging to Cassandra clusters do not use shared filesystem, the home directory for the service account (``/sdf/home/r/rubincas``) is created individually on each node.
Access to the service account through SSH is controlled by ``$HOME/.k5login`` list which is populated by USDF Ansible scripts.

Service accounts at USDF are not allowed to have ``sudo`` access, any operations that require ``sudo`` have to be executed from a regular user account.

Deployment tools (``dax_apdb_deploy`` package) create two accounts in Cassandra:

- Regular user account used by all APDB clients, e.g. ``apdb-prod`` account used by Prompt Production.
  This account is allowed to create Cassandra keyspaces and do all sorts of regular CQL queries.
- Cassandra superuser account that can control everything in Cassandra.
- Default superuser ``cassandra`` account is disabled.

The names and passwords for these two accounts have to be defined in the Vault before initializing the database.

Exposed ports
=============

Cassandra service exposes port ``9042`` on each node of the cluster for regular client connections.
Clients need proper credentials to connect to that port.

For inter-cluster communication Cassandra uses port ``7000``.

``cassandra-medusa`` service uses port ``*:50051`` for its gRPC API, no credentials required.


Security Incident Response
==========================
.. Information and procedures for handling security incidents.

APDB traffic is restricted to USDF network.
In case there is a security breach Cassandra clusters may need to be taken down.
If there is a loss of data due to the incident, the cluster may need to be restored from backups.

Security Policies
=================
.. Describe relevant policies related to the application or the data it processes.

APDB itself and its data are considered internal to Alert Production pipeline and are not accessible to other users.
APDB data is replicated to PPDB within a controlled delay where it is exposed to science users.
