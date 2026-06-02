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

Make sure that the proper Kubernetes context (``usdf-embargo-dmz`` or ``usdf-embargo-dmz-dev``) for the desired vcluster is selected before applying.

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
If a PR is made against the ``lsst-dm/embargo-butler`` Git repo, containers will automatically be built by a GitHub Action, tagged with the ticket branch name (which should be a DM-NNNNN Jira ticket number).
This tag can then be used in ``kustomization.yaml`` to select the appropriate container for the test deployment.

The IP addresses for the dev services can usually be allowed to float rather than be pinned as in production.
The dynamic IP for the ``enqueue`` service can be retrieved using the command ``kubectl get service embargo-butler-enqueue -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}'``

Testing can be done with the production (``rubin-summit``) bucket and a variant of the ``trigger_ingest.py`` script from ``lsst-dm/data-curation-tools`` that gets the credential from the ``usdf-embargo-dmz-dev`` tree in Vault.
In this case, writes to the bucket would not be performed (or allowed), but triggers can be manually sent as if the write had occurred.
This allows testing with real data but any desired volume and cadence.

Alternatively, if end-to-end testing from bucket write is desired, a test bucket needs to be configured with the appropriate notification topic and webhook.
In this case, a fixed IP for the ``enqueue`` service may be desirable.
