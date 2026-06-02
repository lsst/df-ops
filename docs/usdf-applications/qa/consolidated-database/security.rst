########
Security
########

Requesting Access
=================
.. How to request access to the application.

All Summit and USDF users should by default have access to ``pqserver`` via Gafaelfawr authentication/authorization.

Credentials for direct database access are also added by default to the ``~/.lsst/postgres-credentials.txt`` file in both environments.

For Phalanx management access, ask the Phalanx environment administrator.
At USDF, this is via ServiceNow ticket.

Kubernetes vcluster access at USDF is also requested via ServiceNow ticket.

Service accounts
================
.. Describe Kubernetes, Database, or Application Service accounts used by the application.

The Summit uses database user ``oods``.
The USDF uses database user ``usdf`` for reading, ``oods`` for writing by the Transformed EFD.

Security Incident Response
==========================
.. Information and procedures for handling security incidents.

Security Policies
=================
.. Describe relevant policies related to the application or the data it processes.

Much of the data within ConsDB is derived from the EFD and thus is currently considered proprietary according to RDO-013, although the subset that is published via ObsLocTAP and Alerts is world-public.
