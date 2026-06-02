##########
Procedures
##########

Intended audience: Anyone who is administering the s3proxy.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

Deployment is with ArgoCD and Phalanx.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.


Adding a new bucket
-------------------
From time to time, it may be desirable to allow s3proxy to access a new S3 bucket.
In particular, if HiPS maps for Data Previews and Data Releases are stored in their own buckets (or the release buckets), those should be added.

First, add the bucket credentials to the ``rubin/usdf-rsp/s3proxy`` and ``rubin/usdf-rsp-dev/s3proxy`` application secrets in Vault under ``aws-credentials.ini``.
The Vault GUI is useful for this.
Use a short, descriptive profile name as the section name in brackets, and add ``aws_access_key_id`` and ``aws_secret_access_key`` entries.

Then create a ticket branch to add the profile and its corresponding endpoint URL to the s3proxy application's ``values-usdfprod.yaml`` and ``values-usdfdev.yaml`` files in Phalanx.

Following the `Phalanx development procedure <https://phalanx.lsst.io/developers/deploy-from-a-branch.html>`__, edit the deployment (first dev, then when successful prod) in ArgoCD to deploy from the ticket branch.
Synchronize and verify that the new profile is usable (e.g. by retrieving a file via an ``https://usdf-rsp-dev.slac.stanford.edu/s3proxy/s3/profile@bucket/path/to/file`` URL).
It may be necessary to delete the Kubernetes secret in ArgoCD to ensure that the new version is obtained from Vault.

When the branch works, create a pull request for it, get it reviewed if it's non-trivial, and then merge.
When complete, set the ArgoCD branches back to ``main``.


Backup
======
.. Procedures for backup including how to verify backups.

No backups needed.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

No cold startup procedures needed.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No cold shutdown procedures needed.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

Deploy another environment in Phalanx.
