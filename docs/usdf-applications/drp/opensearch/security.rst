########
Security
########

Requesting Access
=================
.. How to request access to the application.

End users do not directly access OpenSearch.  Access is through Grafana to the pre-existing dashboards and to the dataset in Grafana.  Access to the admin interface is through Kubernetes.

Service accounts
================
.. Describe Kubernetes, Database, or Application Service accounts used by the application.

Each service that uses OpenSearch has its own service account.  The OpenSearch cluster itself also has an admin account.
All the accounts and information to log into the OpenSearch cluster are stored in HashiCorp Vault.

Security Incident Response
==========================
.. Information and procedures for handling security incidents.

Any security incidents should be reported to the LSST Security Team following the procedures outlined in the LSST Security Incident Response Plan.

Security Policies
=================
.. Describe relevant policies related to the application or the data it processes.

No relevant security policies.