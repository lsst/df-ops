#######################
Application Information
#######################

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

OpenSearch is installed on Kubernetes in a high availability configuration with 3 master, 3 workers, and 1 dashboard instance.  Rucio, PanDA, and HTCondor are all configured to send metrics to the OpenSearch API with Python code in each respective application. The SLAC Grafana is used to display the dashboards with OpenSearch configured as a Grafana data source.  OpenSearch dashboards are installed, but not currently supported for production use.

Dashboards are for end users in Panda and HTCondor.  Dashboards for Rucio are used with Campaign Management to view data between different sites.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

Associated Systems
==================
.. Describe other applications are associated with this applications.

Rucio, PanDA, and HTCondor all send metrics to OpenSearch.  OpenSearch is integrated with the the S3DF Grafana.

Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - https://github.com/slaclab/rubin-opensearch-deploy
   * - Vault Secrets Dev
     - Not applicable.  No dev environment
   * - Vault Secrets Prod
     - secret/rubin/usdf-opensearch/opensearch

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

Rucio, PanDA, and HTCondor use Python code to send metrics to the OpenSearch API.  No OpenSearch agents are currently used.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

* Kubernetes
* S3DF Grafana

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

No external dependencies.

Disaster Recovery
=================
.. RTO/RPO expectations for application.
