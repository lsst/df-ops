########
Security
########

Requesting Access
=================

The public API is routed through the Rubin Science Platform ingress.
Production access policy is controlled by the weatherbroadcaster Phalanx ingress configuration.

Service accounts
================

The Phalanx deployment disables service account token mounting for the web deployment and update CronJob.


Security Incident Response
==========================

Follow the standard Rubin incident response process.
Unexpected application failures can be configured to send Slack webhook alerts through the ``WEATHERBROADCASTER_SLACK_WEBHOOK`` secret.

Security Policies
=================

The Kubernetes deployment runs as a non-root user, drops Linux capabilities, and uses a read-only root filesystem.
The ingress is managed by Gafaelfawr.
