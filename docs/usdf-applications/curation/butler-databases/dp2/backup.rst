######
Backup
######

This page describes the backup strategy for the **DP2 Butler database**.
Backups are managed by `CloudNativePG <https://cloudnative-pg.io/docs/1.30/>`_ using
the `Barman Cloud plugin <https://cloudnative-pg.io/plugin-barman-cloud/docs/0.13.0/intro/>`_,
which streams base backups and WAL archives to S3-compatible object storage
at SLAC (S3DF Rados Gateway).

Overview
========

* **Backup method:** ``plugin`` → ``barman-cloud.cloudnative-pg.io``
* **Object store:** ``s3://usdf-butler-dp2/rubin-usdf-dp2/dp2-db``
* **S3 endpoint:** ``https://s3dfrgw.slac.stanford.edu``
* **Retention policy:** ``7d`` (7 days)
* **Schedule:** Daily at ``00:00:11`` UTC
* **Target:** ``prefer-standby`` (offloads backup I/O from the primary)

Retention Policy
================

The retention policy is **7 days**, defined in the ``ObjectStore`` resource
(``retentionPolicy: 7d``). Backups and WAL segments older than 7 days are
automatically pruned by the sidecar container, which enforces retention
every hour (``retentionPolicyIntervalSeconds: 3600``).

.. note::

   Because retention is enforced on the object store — not on the
   ``ScheduledBackup`` — changing the schedule does **not** change how
   long backups are kept. To keep backups for longer, edit the
   ``retentionPolicy`` field of the ``ObjectStore`` resource.

S3-Credentials
================
The S3 credentials are stored in Vault under ``secret/rubin/usdf-butler-dp2/s3``.
If you need access to the credentials submit a ServiceNow ticket requesting that
access to the DBA.
