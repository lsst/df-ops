########
Security
########

Requesting Access
=================
.. How to request access to the application.

The application is managed through Phalanx and ArgoCD.  Access is granted through ArgoCD.

Service accounts
================
.. Describe Kubernetes, Database, or Application Service accounts used by the application.

No Kubernetes service accounts.

Database service accounts are created for each instrument in Butler Embargo and Butler Main.

Security Incident Response
==========================
.. Information and procedures for handling security incidents.

KEDA Scaled jobs can be deleted to remove the Prompt Processing KEDA service.

Security Policies
=================
.. Describe relevant policies related to the application or the data it processes.

Prompt Processing processes Embargo data.  Embargo annotations are used to schedule pods to the Embargo Kubernetes nodes.