########
Security
########

Requesting Access
=================
.. How to request access to the application.

Standard k8s vcluster (``usdf-embargo-dmz``) and Vault access.

Service accounts
================
.. Describe Kubernetes, Database, or Application Service accounts used by the application.

The ``ingest`` account is used for ``embargo`` and ``main`` Butler Registry database access in order to distinguish this service from other users of the Registry databases.

Security Incident Response
==========================
.. Information and procedures for handling security incidents.

Since there is no external access, no incidents are expected.

Security Policies
=================
.. Describe relevant policies related to the application or the data it processes.

The application processes data in the Embargo Rack, but it generally does not access pixel data (only if the JSON sidecar file is not present).
