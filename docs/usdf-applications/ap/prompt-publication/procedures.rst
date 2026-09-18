##########
Procedures
##########

Intended audience: Anyone who is administering the Prompt Publication Service.

Deployment
==========

Deployed via Phalanx.
Scheduled scale up and down daily via CronJobs.

Maintenance
===========
.. Maintenance tasks. How maintenance is communicated and carried out.

Backup
======
.. Procedures for backup including how to verify backups.

Cold Startup
============
.. Steps if needed to recover application after downtime or disaster.

Set up prompt repo
------------------

1. Enable the AlloyDB cluster via Terraform by setting ``butler_prompt_data_products_enabled = true`` in
   ``idf_deploy/environment/deployments/science-platform/env/<env>-cloudsql.tfvars``.
   Open a Pull Request and ensure the Terraform Plan of the GitHub Actions is correct.
   Merging to ``main`` auto-applies via the corresponding GitHub Actions
   workflow and creates:

   - AlloyDB cluster ``butler-prompt-<env>``
   - Primary instance ``butler-prompt-<env>-primary`` (public IP enabled)
   - Read pool instance ``butler-prompt-<env>-readpool`` (private IP only)
   - Private DNS record ``alloydb-butler-prompt.rsp-sql-<env>.internal`` pointing
     at the read pool IP
   - Service account ``usdf-alloydb-auth-proxy`` with ``roles/alloydb.client``

2. Obtain postgres admin access, via GCP console or via ``gcloud`` commands.

3. Create the database ``prompt`` and required extension ``btree_gist``.
   One way to do it is via AlloyDB Studio.
   In AlloyDB Studio, connect as ``postgres`` and run:

   .. code-block:: sql

      CREATE DATABASE prompt;

   Switch the database ``prompt``, then:

   .. code-block:: sql

      CREATE EXTENSION btree_gist;

4. Create postgres user ``prompt_pub`` and grant it privileges to the ``prompt`` database.

5. Verify connection from SLAC via the `AlloyDB Auth Proxy <https://docs.cloud.google.com/alloydb/docs/auth-proxy/connect>`_.
   Generate a key for the ``usdf-alloydb-auth-proxy`` service account, then:

   .. code-block:: shell

      alloydb-auth-proxy \
        --credentials-file=<key.json> --public-ip \
        --address=127.0.0.1 --port=5432 \
        "projects/<project-id>/locations/us-central1/clusters/butler-prompt-<env>/instances/butler-prompt-<env>-primary"

   A key can be found at SLAC's vault:

   .. code-block:: shell

      vault kv get secret/rubin/<vCluster-name>/prompt-pub

   Then one way to test the connection is ``psql "host=127.0.0.1 port=5432 user=prompt_pub dbname=prompt"``.

6. Obtain a template prompt butler config yaml from phalanx ``applications/butler/templates/configmap-private.yaml``, at RSP supply a temporary ``~/.lsst/db-auth.yaml`` locally, and create a butler repo by ``butler create repo --seed-config prompt.yaml`` where a direct IP, not the read pool, to the postgres is given.

7. Run ``lsst.prompt_publication_service.scripts.initialize_google_repo`` to finish initializing the butler repo from ``prompt_prep`` to ``prompt``. Creation of temporary tables in the database is needed.

Cold Shutdown
=============
.. Any procedures needed to cleanly shutdown application before USDF downtime.

Reproduce Service
=================
.. How to reproduce service for testing purposes.
