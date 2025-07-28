###############
Troubleshooting
###############

Intended audience: Anyone who is administering the application.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - Sasquatch Schema Registry IP changes
     - During maintenance and upgrades the Sasquatch Schema Registry IP changes
     - :ref:`schema_registry_connectivity_issue`

Monitoring
==========
.. Describe how to monitor application and include relevant links.

.. _schema_registry_connectivity_issue:

Schema Registry Connectivity Issue
==================================
.. Template to use for troubleshooting

**Symptoms:** There are errors generated for connectivity to the Schema Registry.  Some examples are ``kafkit.registry.errors.RegistryBadRequestError: Registry error (404). 40403 - Schema 317 not found`` or ``httpx.ConnectError``.

**Cause:** The Schema Registry is deployed on Sasquatch in the USDF RSP with a Cluster IP service.  During Sasquatch maintenance the IP can change.

**Solution:**
 #. Determine the new Sasquatch IP Address with ``kubectl get service sasquatch-schema-registry -n sasquatch`` on the USDF RSP vCluster.  If you do not have access to the vCluster ask on *usdf-rsp-support* Slack channel.
 #. Update the ``schemaRegistryUrl`` IP address in the URL of the `USDF Prompt Processing Prod Values File <https://github.com/lsst-sqre/phalanx/blob/main/applications/next-visit-fan-out/values-usdfprod-prompt-processing.yaml>`__.
 #. Open a PR, merge the changes, then sync in the *Next Visit Fan Out App* in Argo CD.
