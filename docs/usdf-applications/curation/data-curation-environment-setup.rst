###########################################
Setup Data Curation Environment at the USDF
###########################################

Most of Rubin data curation activities can be done via individual member's own account.

Login Nodes and Profiles
========================

Use interactive node ``rubin-devl`` in most case. In some specially cases, you can use DTN node
``sdfdtn001`` or ``sdfdtn002``.

Create symlinks in your ``$HOME/.profile.d`` directory that point to files in ``/sdf/group/rubin/sw/profile.d``.
These login configuration profiles should be run before additional data curation related environment setup
profiles are run. A good way to do this to created a file ``$HOME/.profile.d/99-data-curation.conf``.

To obtain the lastest LSST tools (butler), and Rucio tools, add the following to the
``99-data-curation.conf`` file:

.. code-block:: bash

    source /cvmfs/sw.lsst.eu/almalinux-x86_64/lsst_distrib/w_2026_02/loadLSST.sh
    setup lsst_distrib

Access Embargo S3 Storage
=========================

In many cases, we use the MinIO client tool to access the Embargo S3 storage directly. To load the MinIO
client tools, run command

.. code-block:: bash

    module load mc

The MinIO client configuration file is located at ``$HOME/.mc/config.json``. Put the following content
in the file:

.. code-block:: json

    {
      "version": "10",
      "aliases": {
        "embargo": {
          "url": "https://sdfembs3.sdf.slac.stanford.edu:443",
          "accessKey": "<get from Vault>",
          "secretKey": "<get from Vault>",
          "api": "s3v4",
          "path": "auto"
        }
      }
    }

Note on conventions: "embargo" is used in some commands. In ``mc ls embargo/rubin-summit`` this means
the ``embargo`` alias defined above. In ``butler query-dataset embargo "raw"``, this means the
``embargo`` repository defined in the butler configuration file (see file ``$DAF_BUTLER_REPOSITORY_INDEX``).

Files in $HOME/.lsst used by Butler
===================================

Butler uses several credential files in your ``$HOME/.lsst`` directory to access S3 storage and Bulter
databases.

Remove ``$HOME/.lsst/db-auth.yaml`` file. It is obsolted and should NOT be used.

AWS S3 Credentials
------------------

Butler uses credebtials in ``$HOME/.lsst/aws-credentials.ini`` to access the S3 storge
(`Reference <https://pipelines.lsst.io/v/daily/modules/lsst.resources/s3.html>`__).
For exmaple, the following contains access credentials for the Embargo S3 storage:

.. code-block:: ini

    [embargo]
    aws_access_key_id = <your access key id from Vault>
    aws_secret_access_key = <your secret access key from Vault>

Postgres Credentials
--------------------

Bulter uses info in ``$HOME/.lsst/postgres-credentials.txt`` to access the Bulter databases. The following two
lines give exampes of the content of the file:

.. code-block:: ini

    usdf-butler.slac.stanford.edu:5432:lsstdb1:rubin:<repo main's DB password in Vault>
    usdf-butler-embargo-db-tx.sdf.slac.stanford.edu:5432:lsstdb1:rubin:<repo embargo's DB password in Vault>


The Rucio Configuretion
=======================

If you will need to work with Rucio, add the following to the ``99-data-curation.conf``.

.. code-block:: bash

    export RUCIO_CONFIG=$HOME/.config/rucio-rubin.config
    export RUCIO_ACCOUNT=$(id -un)

The ``$RUCIO_CONFIG`` file will look like this:

.. code-block:: ini

    [client]
    rucio_host = https://rubin-rucio.slac.stanford.edu:8443
    auth_host = https://rubin-rucio.slac.stanford.edu:8443

    auth_type = ssh
    ssh_private_key = $HOME/.ssh/id_rsa

In the above example we use SSH authentication for Rucio. Most team members use this method but other
authentcation methods such as X.509 are also
supported. If you don't have an account in Rucio, you will need to ask another member of the team to create
one for you with appropriate privileges in Rucio. The above example also assume that your Rucio account name
is the same as your Unix user name (``id -un``).

Access Privileges
=================

Ask other members of the team and S3DF for access to various secrets in Vault, access to Kubernetes vClusters
and Rucio/FTS/RSEs

Vault
-----

For convenience, define the following environment variable in the ``99-data-curation.conf``

.. code-block:: bash

    export VAULT_ADDR="https://vault.sdf.slac.stanford.edu:8200"

Each time you start using vault, do the following:

.. code-block:: bash

    module load vault
    vault login -method=ldap username=$(id -un)

Type in your S3DF ``Windows AD`` password when prompted.

Kubernetes
----------

Likely Kubernetes vClusters that you will need access:

.. code-block:: text

    usdf-embargo-dmz
    user-rucio (and -dev)
    usdf-fts3 (and -dev)

Accessing to ``usdf-rucio`` and ``usdf-fts3`` vClusters are needed only for the purpose of configuation, etc.
It is not needed for day-to-day use of Rucio/FTS and RSEs.

Kubernetes access tokens expires in a day or two. So you will need to re-generate the access tokens from
time to time. To do so, go to ``https://k8s.slac.stanford.edu/<vcluster-name>`` and following the instructions
there.

FTS and RSEs
------------

To register to VOMS, access the FTS and RSEs via command lines, you will need X.509 certificates. Ask other
members of the team for help.
