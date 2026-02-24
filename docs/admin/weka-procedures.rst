###############
Weka Procedures
###############

Intended audience: Anyone who is administering or using shared data space at USDF.

Storage Organization
====================

/sdf/group/rubin
----------------

This space is hosted on the same storage cluster as ``/sdf/home``.
It is entirely flash-based, with no disk.
As a result, storage here has slightly higher performance but is more expensive.
Rubin is provided space in this cluster through overhead, not direct purchases (as of 2025), so the quantity and quality of service is determined by S3DF, not Rubin directly.

Most items in this filesystem are symbolic links to other locations, usually on ``/sdf/data/rubin``.

 * ``/sdf/group/rubin/services``: space for particular infrastructure services such as PanDA and HTCondor that need it

 * ``/sdf/group/rubin/sw``: storage for the "shared stack" installation of the Rubin Science Pipelines.

 * ``/sdf/group/rubin/web_data``: public space published under https://s3df.slac.stanford.edu/data/rubin

/sdf/data/rubin
---------------

This is the primary location for Rubin data.
It is disk-based in one or more Ceph object stores with a flash metadata and caching layer.
Rubin directly purchases storage in this cluster, so the quantity and quality of service is more directly controlled.

It includes:

 * Permanent archives
 * Released data
 * Common reference and test data
 * Working space for in-progress productions
 * Working space (personal and group-shared) for development and analysis

 * ``/sdf/data/rubin/app``: unused
 * ``/sdf/data/rubin/data``: data for the Camera, DP0.3, and files used to load Qserv from 2022.
 * ``/sdf/data/rubin/ddn``: data moved from the legacy Lustre filesystem, mostly related to moving data from NCSA in August 2022.
 * ``/sdf/data/rubin/g``: unused.
 * ``/sdf/data/rubin/gpfs``: data moved from the legacy GPFS filesystem, related to moving data from NCSA in August 2022.
 * ``/sdf/data/rubin/lsstdata``: archival data from LSST instruments (LSSTCam, LSSTComCam, LATISS).
 * ``/sdf/data/rubin/panda_jobs``: working space for the PanDA workflow management system.
 * ``/sdf/data/rubin/public_html``: unused
 * ``/sdf/data/rubin/qserv-backup``: unused
 * ``/sdf/data/rubin/repo``: Data Butler repositories for released data, campaigns, and development and analysis
 * ``/sdf/data/rubin/repo-tarballs``: unused
 * ``/sdf/data/rubin/rses``: Rucio storage elements (mostly symlinks to other storage to remap into Rucio's organization)
 * ``/sdf/data/rubin/shared``: shared group space and common reference and test data
 * ``/sdf/data/rubin/temp``: administrator scratch space
 * ``/sdf/data/rubin/templates``: templates used for Prompt Processing
 * ``/sdf/data/rubin/test``: administrator scratch space
 * ``/sdf/data/rubin/test-nfs``: administrator scratch space
 * ``/sdf/data/rubin/user``: large per-user personal working space

Storage Requests
================

Requests for storage will generally be for new Butler repos (under ``/sdf/data/rubin/repo``) or new shared group space (under ``/sdf/data/rubin/shared``).
Some directories may need to live directly under ``/sdf/data/rubin`` if they require hard links to files in ``/sdf/data/rubin/repo``, as hard links appear to not be able to span quota boundaries, even within the same filesystem.

In some cases, users may request increased quotas for their personal space for files that are not going to be shared with others and are not in a Butler repo.
This personal space should always be their ``/sdf/data/rubin/user/{username}`` space, not their ``/sdf/home`` home directory.
These quota increase requests should be approved by USDF management and implemented by the storage team.

Butler repos should be created at the request of the Campaign Management or Pipelines teams.

Requests for shared group space should contain at least the following information:

- Requesting username
- Suggested directory name
- Type of data to be stored, where the data comes from, and its expected uses
- Who will curate/maintain the data
- Expected maximum data size (quota) and/or current size and growth rate
- Additional users needing write privileges for the directory
- Users or group(s) needing read privileges for the directory

This information should be placed in a ServiceNow ticket as a permanent record.

Ensure that the data is in fact going to be shared across multiple users and is not just an expansion of user home directory space to avoid quotas.
Ensure that the directory name properly represents the data it contains and that it will not be confusing.


Procedure:

.. code-block:: bash

   ssh s3dflogin
   kinit
   ssh rubinmgr@rubin-devl
   cd /sdf/data/rubin/shared
   mkdir $DIR
   chgrp rubin_users $DIR
   chmod 2750 $DIR

After creating the directory, request (via the same or another ServiceNow ticket) that the storage team apply a quota to it (if hard links are not an issue).
This quota not only guards against excessive usage by the group, it also allows us to more easily monitor the usage within the directory via quota reports.

Access Control
==============

If data is embargoed, it must *not* live in the Weka filesystems but must instead be kept in the Embargo Rack S3 object store, generally in the ``rubin-summit-users`` bucket.

If data in a Weka filesystem is pre-release, make sure that the directory is owned by the ``rubin_users`` group or something more restrictive.
The user ownership can either be ``rubinmgr`` or a particular curator/maintainer, with additional group members added via ACL (``setfacl -d -m u:{user}:rwx``).
The set-gid bit should also be set on the directory so that group ownership is propagated.

If the data is pre-release or proprietary, make sure that the "other" permissions on the directory are removed.

If proprietary data is to be published to Data Rights Holders via the Weka S3 gateway, it should live in a directory by itself, with no pre-release data.
A Weka S3 bucket can then be defined by the storage team on the directory using the ``rubins3`` user.


.. note::

   The ``rubins3`` user is currently a member of the ``rubin_users`` group.
   This is excessive, as ``rubin_users`` has access to pre-release as well as proprietary data.
   Once a separate group is created for SLAC users with only proprietary (data rights) access, ``rubins3`` should be moved to that group, as well as all directories underlying Weka S3 buckets.
