##########
Procedures
##########

Intended audience: Anyone who is administering Embargo Transfer.

Deployment
==========
.. Deployment process for the application.  Included upgrades and rollback procedures

.. code:

   git clone https://github.com/slaclab/usdf-embargo-deploy
   cd kubernetes/overlays/${environment}
   vault login -method=ldap
   make apply

Standard Kubernetes tools like ``k9s`` can be used to dynamically update the deployment including increasing/decreasing replicas, but changes should be committed back to GitHub.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

After creating a pull request or merging to the ``main`` branch in ``lsst-dm/embargo-butler``, a GitHub Action will automatically build a new version of the containers, which can be deployed for testing.

For production, an annotated tag with version "vN.N.N" should always be placed on the ``main`` branch, which will cause a versioned container to be created.
That version can then be deployed by selecting it in the ``kustomization.yaml`` file for the appropriate environment(s).

Backup
======
.. Procedures for backup including how to verify backups.

N/A.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

If necessary, recreate the notification topic and bucket notification configuration in S3 using the configurations and scripts in `GitHub <https://github.com/slaclab/usdf-embargo-deploy/bucket-notifications>`__.
Reapply the application manifests from `GitHub <https://github.com/slaclab/usdf-embargo-deploy/kubernetes/overlays>`__.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

No special tasks.

Reproduce Service
=================
.. How to reproduce service for testing purposes.

Testing should be done in the ``usdf-embargo-dmz-dev`` vcluster.
IP addresses will need to be changed, and appropriate notification configurations for test buckets will need to be applied.
