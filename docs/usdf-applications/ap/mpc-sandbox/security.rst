########
Security
########

Requesting Access
=================
.. How to request access to the application.

Credentials are in Vault at ``vault kv get secret/rubin/minor-planet-survey/postgres-mpc-sandbox``

``rubin`` is setup as the general user account.

Service accounts
================
.. Describe Kubernetes, Database, or Application Service accounts used by the application.

No service accounts are setup.

Security Incident Response
==========================
.. Information and procedures for handling security incidents.

The main risk is that the replication password is compromised.  If the password is compromised contact the Minor Planet Center and to reset the password.


Security Policies
=================
.. Describe relevant policies related to the application or the data it processes.
