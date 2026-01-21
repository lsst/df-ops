#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

A Kubernetes Pod runs an infinite loop that executes ``mc mirror`` to copy objects from the Summit S3 LFA bucket to the USDF S3 LFA bucket (located in the ``s3dfrgw`` public S3 storage) and then sleeps for a configured time.

Since this service needs to contact the Summit network, it uses a ``socat`` proxy to gain access to IP addresses on the (untunneled) LHN network.
The proxy works by capturing the DNS lookup in the vcluster for ``s3.cp.lsst.org`` and pointing it to the proxy's S3DF-internal end.

Since the Summit LFA bucket (but not the USDF one) is purged of old objects, it is expected that ``mc mirror`` will continue to perform adequately throughout Operations.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

.. mermaid::
   :caption: LFA Replication architecture

   architecture-beta
     group vcluster(cloud)[vcluster]

     service summitCeph(disk)[Summit LFA S3]
     service proxy(server)[socat Proxy] in vcluster
     service mirror(server)[Mirror] in vcluster
     service usdfCeph(disk)[USDF LFA S3]

     summitCeph:R --> L:proxy
     proxy:R --> L:mirror
     mirror:R --> L:usdfCeph


Associated Systems
==================
.. Describe other applications are associated with this applications.

A separate deployment of the "Embargo Transfer" service code is used to ingest certain LFA objects into the ``main`` Butler repo.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/slaclab/rubin-lfa-replicate-deploy/tree/main/kubernetes/overlays/prod
   * - socat Proxy
     - https://github.com/slaclab/lhn-proxy/tree/main/usdf-lfa
   * - Vault Secrets Dev
     - N/A
   * - Vault Secrets Prod
     - secret/rubin/usdf-lfa

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Objects are copied from the ``rubinobs-lfa-cp`` bucket at the Summit to the corresponding bucket at USDF in the ``s3dfrgw`` endpoint.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* ``s3dfrgw`` Ceph S3 object store
* Long Haul Network for connection to Summit
* Kubernetes infrastructure

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

No external dependencies.

Disaster Recovery
=================
.. RTO/RPO expectations for application.

None.  ``mc mirror`` should recover itself when next run.
