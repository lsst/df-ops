########
Security
########

Requesting Access
=================
.. How to request access to the application.

Credentials are in Vault at ``vault kv get secret/rubin/minor-planet-survey/postgres``

``rubin`` is setup as the general user account.  ``rubin_rw`` is setup with right permissions.  It was requested to be able to update values for testing.  Grants are managed in `grants.sql in the GitHub Repository <https://github.com/slaclab/rubin-usdf-minor-planet-survey/tree/main/kubernetes/overlays/prod/sql>`__

Service accounts
================
.. Describe Kubernetes, Database, or Application Service accounts used by the application.

No Kubernetes Service Accounts.

The ``epo`` user is setup as the replication user for EPO.

Security Incident Response
==========================
.. Information and procedures for handling security incidents.

The main risk is that the replication password is compromised.  If the password is compromised contact the Minor Planet Center Annex and to reset the password.

Security Policies
=================
.. Describe relevant policies related to the application or the data it processes.
