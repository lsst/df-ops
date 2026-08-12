######
Access
######

This page describes how to access the DP2 Butler database. Access is granted
within SLAC only network.


Endpoints
=========

.. list-table::
   :header-rows: 1
   :widths: 20 40

   * - Type
     - DNS

   * - read-only
     - ``usdf-butler-dp2-db-ro.sdf.slac.stanford.edu``

   * - read-write
     - ``usdf-butler-dp2-db-rw.sdf.slac.stanford.edu``


Connecting
==========

Using ``psql`` for read-only connections:

.. code-block:: bash

   psql -h usdf-butler-dp2-db-ro.sdf.slac.stanford.edu -U rubin -d lsstdb1

Using ``psql`` for read-write connections:

.. code-block:: bash

   psql -h usdf-butler-dp2-db-rw.sdf.slac.stanford.edu -U rubin -d lsstdb1

Only the role ``rubin`` was created for this database. If other role is needed,
you have to requested it via ServiceNow ticket to the DBA. During this request
include what attributes this role will require. The password will be stored in
Vault under ``secret/rubin/usdf-butler-dp2/roles/<role_name>``

.. note::

   Credentials are managed via Vault. Path for rubin role is at ``secret/rubin/usdf-butler-dp2/roles/rubin``
