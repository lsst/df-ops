#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

The service runs on computers in the Embargo Rack to ensure physical and network security of the Satellite Catalog.  Two machines in a high-availability configuration are used since Alerts cannot be issued if the service is not available.

The service is a standard Web server with a Python main program using the aiohttp package and a calculation shared library written in C++ for speed.  It will be packaged in a container stored in the ghcr.io registry (which could be mirrored to a SLAC registry).

The service will be deployed using systemd so that it starts when the machine is booted.

The service, at startup and periodically thereafter, contacts an HTTPS API at space-track.org to download new versions of the Satellite Catalog.  The credentials for this are stored on the machine's system disk, which is full-disk-encrypted at rest.  The credentials will not be placed in the S3DF Vault instance.  The catalog itself resides in the service's memory and is never stored on non-volatile storage.

The service will use port 443 for encrypted HTTPS connections, with source IPs limited to SLAC networks.  No authentication is anticipated to be needed, but a secret shared with the Alert Production could be used.

Outbound connections will go to port 443 for encrypted HTTPS connections to space-track.org and ghcr.io and possibly github.com for deployment configuration files.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Associated Systems
==================
.. Describe other applications are associated with this applications.

The Alert Production running in the Prompt Processing framework depends on this service.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

Service configuration will be stored in the container.  Deployment configuration files will be stored in GitHub.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     -
   * - Vault Secrets Dev
     -
   * - Vault Secrets Prod
     -

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

The service responds to requests via HTTPS from internal SLAC IP addresses only.  The requests will primarily come from the Alert Production that runs on every science image taken; it is running under the Prompt Processing framework in S3DF Kubernetes.

Visit request
-------------
This is used to pre-cache the satellites visible in a given field of view to make later matching faster.

Parameters:
  * visit_id
  * exposure_start_mjd
  * exposure_end_mjd
  * boresight_ra
  * boresight_dec

Response:
* HTTP status 200 or 500

DIASource request
-----------------
This is used to determine which difference image sources do not match satellite orbits and hence are allowed to have alerts issued.

Parameters:
  * visit_id
  * detector_id
  * diasources (list of diasource_id and bbox bounding box pairs)

Response:
  * id_allow_list (list of allowed diasource_ids)

This request design ensures that the Satellite Catalog never leaves the service, that it is infeasible to determine the contents of the catalog by issuing requests, and that the service "fails safe" by returning the list of allowed difference image sources (so that Alerts are not transmitted if the service does not succeed).

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

  * Embargo Rack for power and network
  * S3DF networking for inbound connections
  * SLAC networking for outbound connections to space-track.org and GitHub for retrieving the service container
  * S3DF administrators for machine and OS maintenance as well as HTTPS certificate maintenance

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

Disaster Recovery
=================
.. RTO/RPO expectations for application.
