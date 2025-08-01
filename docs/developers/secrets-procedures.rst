##############################
Secrets Management Procedures
##############################

Intended audience: Anyone who is developing applications at the USDF.

Requesting Vault Access
=======================

To request access to Vault submit a `Service Now Ticket <https://slacprod.servicenowservices.com/gethelp.do>`__ and specify the Vault secrets path.  If you do not know the secret path ask a colleague who has access or if not known include the application name.

Vault Command Line Interface
============================

To use the Vault Command Line Interface on the USDF interactive nodes use the below commands.  Replace with your username and login with your Windows account.

.. rst-class:: technote-wide-content

.. code-block:: bash

    export VAULT_ADDR=https://vault.slac.stanford.edu
    module load vault
    vault login -method=ldap username=replace


Creating Vault Secrets
======================

Updating Vault Secrets
======================
