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

Keda has the following service accounts that are used by the operator.
 * keda-metrics-server
 * keda-operator
 * keda-webhook

Security Incident Response
==========================
.. Information and procedures for handling security incidents.

Keda Scaled jobs can be deleted to remove the Prompt Processing Keda service.

Security Policies
=================
.. Describe relevant policies related to the application or the data it processes.

No relevant security policies.