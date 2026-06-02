#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

The goal of the service is to ingest raw science detector, wavefront, and guider images into the ``embargo`` Butler repo as rapidly and reliably as possible.
It is also used to ingest selected Large File Annex objects into the ``main`` Butler repo.

The input to the service is notification webhooks (HTTP requests) from Ceph S3 storage.
Each notification indicates that an object has been created in an S3 storage bucket.

The webhooks land on an ``enqueue`` service that records their object names in a Redis list (one per bucket) if they match a configured regular expression.
The regexp allows fast filtering of undesired objects such as JSON files.

Multiple instances of an ``ingest`` worker service atomically retrieve object names from the Redis list and batch them for ingest into the Butler.
These also do visit definition (where appropriate) and load the Redis database with group identifier mappings for the microservice.

An ``idle`` service looks for abandoned worker batches and reinserts their contents into the main Redis list.
This is intended to provide automatic recovery from worker crashes.

The ``presence`` microservice handles lookups into the group identifer mapping.
If a particular detector image for a group(+snap) has not arrived, it will return "not present".
If the image has arrived, it will return an S3 URL (ResourcePath) pointing to it.

The ``enqueue`` service needs to be visible in the ``sdf-rubin-ingest`` network (or ``sdf-services``, but this is deprecated) so that it can be contacted by Ceph instances.
The ``presence`` service needs to be visible to the Prompt Processing instance that will contact it.
If this is in the same vcluster, then no special network is required.
If it is in a different vcluster (as is the case in production), then the ``sdf-rubin-ingest`` network (or ``sdf-services``, again deprecated) is required.


Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

.. mermaid::
   :caption: Auto-ingest architecture

   architecture-beta
     group vcluster(cloud)[vcluster]

     service redis(database)[Redis] in vcluster
     service enqueue(server)[Enqueue] in vcluster
     service ingest(server)[Ingest] in vcluster
     service idle(server)[Idle] in vcluster
     service presence(server)[Presence] in vcluster
     service ceph(disk)[Ceph]
     service butler(database)[Butler Registry]
     service prompt(server)[Prompt Processing]

     ceph:R --> L:enqueue
     enqueue:R --> L:redis
     idle:L <--> R:redis
     ingest:T <--> B:redis
     butler:T <-- B:ingest
     presence:B <-- T:redis
     prompt:B --> T:presence

Associated Systems
==================
.. Describe other applications are associated with this applications.

Prompt Processing relies on the ``presence`` microservice to determine whether an image for a given group identifier and detector has arrived, and, if it has, what its name is.

Rapid Analysis running at USDF relies on Butler ingestion to indicate the presence of images and to enable processing of the images.

Daily Prompt Processing catch-up and other analysis relies on Butler ingestion.


Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - ``slaclab/usdf-embargo-deploy/kubernetes/overlays/{namespace}``
   * - Ceph Configuration
     - ``slaclab/usdf-embargo-deploy/bucket-notifications/prod``
   * - Vault Secrets Dev
     -
   * - Vault Secrets Prod
     - ``rubin/usdf-embargo-dmz/{namespace}``


The secret contains a ``db-auth.yaml`` file with a credential for accessing the Butler repo Registry database; a shared secret between the notification topic in Ceph and the ``enqueue`` service; a Redis password shared between the services and the database deployment; and a "profile" URL containing a read-only credential used to access the Butler Datastore.

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

When objects are created in the Ceph bucket, ``ObjectCreated`` notification webhooks are sent to the ``enqueue`` service.
This service selects notifications of interest based on a regexp in its configuration and writes them to a per-bucket list (queue) in Redis.

Workers do blocking waits for additions to the per-bucket list.
When anything is available, a worker will atomically move it to its own queue.
If there are multiple available objects, the worker will take them until it hits a configured maximum limit.

The worker queue batch is then processed.

First, if this is an image (non-LFA) bucket, the groups of the images are recorded for the presence microservice.

Next, the ingest task is run on the batch of objects.
Guider images are sorted to the end of the batch so that the necessary dimension records are likely to be in place when their ingestion is attempted.
Callbacks are used to handle success, ingest failure, and metadata translation failure cases.
For success, the processed objects are removed from the worker queue, and a Summit webhook is triggered for each exposure that they belong to.
On ingest failure, a count is incremented in Redis for the uningested object.
If the count reaches a configured maximum, the object is removed from the worker queue.
Metadata failure always removes the object from the worker queue, as it is not a recoverable error.

Finally, if any objects were successfully ingested, the visit definition task is called for each of them.


Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

Dependencies include: Ceph, Weka Kubernetes PV storage for Redis, Butler database


Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

None

Disaster Recovery
=================
.. RTO/RPO expectations for application.

All information is still in the original bucket, so manual reingestion can be used to recover from a disaster or failure.
There are two techniques:

- Manually trigger auto-ingest by simulating webhook notifications.
  The ``trigger_ingest.py`` script in ``lsst-dm/data-curation-tools`` does this.

- Manually ingest images using the ``butler ingest-raws`` command.

Note that boresight locations and spatial regions associated with a detector exposure image can be updated within the Butler Registry; this is now expected to take place daily as part of the Alert Production catch-up processing.
If the Butler Registry database has been lost and is re-created using either of these mechanisms, the original values will be restored.
If some but not all of the detectors for an exposure have been ingested and had their metadata updated, later ingestion of other detectors from the raws will generally fail due to metadata conflicts.
``butler ingest-raws --update-records`` can override this at the cost of losing the updated metadata values.
