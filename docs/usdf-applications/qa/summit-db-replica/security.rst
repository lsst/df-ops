########
Security
########

Requesting Access
=================
.. How to request access to the application.

Existing credentials are stored at ``vault kv get secret/rubin/usdf-summitdb/logical-replica``.  For new credentials request via Service Now Ticket.  Questions can be asked on the ops-usdf-database Slack channel.

Service accounts
================
.. Describe Kubernetes, Database, or Application Service accounts used by the application.

Database accounts are on the database and defined in ``vault kv get secret/rubin/usdf-summitdb/logical-replica``

Security Incident Response
==========================
.. Information and procedures for handling security incidents.

If the replication account is compromised work with the Chile IT team to change the replication user.

Security Policies
=================
.. Describe relevant policies related to the application or the data it processes.

No relevant policies.