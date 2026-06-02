####################
Database Information
####################

The following sections provide detail on the Minor Planet Center Replica.

Architecture
============
.. Describe the architecture of the application including key components (e.g API servers, databases, messaging components and their roles).  Describe relevant network configuration.

The ``mpcorb`` Postgres database is installed in the ``usdf-minor-planet-survey`` Kubernetes vCluster in the ``mpcorb-replica`` namespace with the Cloud Native Postgres Operator.  Some of the data comes from Rubin, but is sent to the MPC Annex first via HTTP, loaded into the database, then replicated back to Rubin.

Postgres Logical Replication is used to replicate data from the MPC annex to the USDF.  There are two Postgres subscriptions at the MPC annex.  ``sbn146_obs_table_pub`` has the ``obs-sbn`` table.  The ``sbn146_other_tables_pub`` has all other tables.  The Postgres subscription names at the USDF includes ``rubin-usdf``.  The University of Washington has also has an instance of the MPC replica that they support.  The Postgres subscription names at the University of Washington includes ``rubin`` without the ``-usdf``.

``mpcorb`` depends on Internet connectivity to receive updates from the MPC Annex.  The SLAC NAT IP was shared with the MPC Annex as the NAT addresses used for outbound connectivity with SLAC.  If this address changes the MPC Annex will need to be notified.

``mpcorb`` is also setup as a Postgres publication to replicate data to the EPO.  Further details are in the Architecture Diagram and Data Flow sections of this page.

``mpc_orbits`` table is largest table with 1 million rows.  It will grow to 5 million rows over the course of the survey.

Architecture Diagram
====================
.. Include architecture diagram of the application either as a mermaid chart or a picture of the diagram.

.. mermaid::

   graph TD

      %% Node Definitions using Database Shapes
      MPC[(<b>MPC Annex</b><br/><br/>Postgres Logical Replication Publication<br/><br/>Access restricted to USDF NAT IP)]

      USDF[(<b>USDF</b><br/><br/>Subscription to MPC Annex<br/><br/>Publication for EPO<br/>for EPO)]

      GCP_LB[GCP Access Kubernetes<br/>Load Balancer<br/><br/>Access restricted to EPO<br/>GCP NAT IPs with Load<br/>Balancer Source IP Ranges]

      EPO[(<b>EPO in Google Cloud</b><br/><br/>Subscription to the USDF)]

      %% Flow Connections
      MPC --> USDF
      USDF --- GCP_LB
      GCP_LB --> EPO

      %% Legend Section (Placed at bottom)
      subgraph Legend
         direction LR
         L1[MPC Annex] ~~~ L2[USDF] ~~~ L3[EPO Google Cloud]
      end

      %% Anchor Legend to the bottom by creating an invisible connection from the end of the flow
      EPO ~~~ Legend

      %% Styling for Environment Differentiation
      style MPC fill:#e1f5fe,stroke:#01579b,stroke-width:2px
      style USDF fill:#f5f5f5,stroke:#616161,stroke-width:2px
      style GCP_LB fill:#f5f5f5,stroke:#616161,stroke-width:2px
      style EPO fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px

      %% Styling for Legend Nodes
      style L1 fill:#e1f5fe,stroke:#01579b
      style L2 fill:#f5f5f5,stroke:#616161
      style L3 fill:#e8f5e9,stroke:#2e7d32

      %% Make the anchor link invisible
      linkStyle 3 stroke-width:0px;

Associated Systems
==================
.. Describe other applications are associated with this applications.

A cronjob is run to each night before observing with moving objects objects in the Solar System.  This is used by Prompt Processing.

Pipelines code interacts with this database to review for potential new objects to submit to the the Minor Planet Center.


Configuration Location
======================
.. Detail where the configuration is stored.  This is typically in GitHub, Kubernetes Configuration Maps, and/or Vault Secrets.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Kubernetes Configuration
     - https://github.com/slaclab/rubin-usdf-minor-planet-survey/tree/main/kubernetes/overlays/prod
   * - SQL Configuration
     - https://github.com/slaclab/rubin-usdf-minor-planet-survey/tree/main/kubernetes/overlays/prod/sql
   * - Vault Secrets Dev
     - secret/rubin/usdf-minor-planet-survey/postgres
   * - Vault Secrets Prod
     - N/A

Data Flow
=========
.. Describe how data flows through the system including upstream and downstream services

The Minor Planet Center Annex is the Postgres Logical Replica publication.  The USDF Minor Planet Center replica is configured with subscription to the Obs table and to the other tables at the Annex.

Rubin EPO also needs a copy of this data.  It was not an option to connect directly from EPO to the Minor Planet Center Annex so a double hop Postgres Replication is setup.  The USDF Minor Planet Center replica is also setup as a Postgres publication to replicate the same tables that it subscribes to.  EPO has a development, integration, and production environments setup as subscriptions in the Google Cloud with the Cloud Native Postgres (CNPG) Operator.  Currently only dev is connected.

A separate pipeline is run to identify new objects and their orbits.  These are sent to an HTTP endpoint at the Minor Planet Center which is the clearinghouse for new discoveries.  Once the data is accepted it sent back to the USDF through logical replication.

Dependencies - S3DF
===================
.. Dependencies at USDF include Ceph, Weka Storage, Butler Database, LDAP, other Rubin applications, etc..  This can be none.

Below are S3DF Dependencies.

* Kubernetes
* SLAC LDAP to authenticate to the vCluster
* DNS resolution for the SBN address
* Weka storage for Kubernetes.  The database uses a persistent volume claim.

Dependencies - External
=======================
.. Dependencies on systems external to S3DF including in US DAC, France or UK DF, or other external systems.  This can be none.

Below are External Dependencies.

* Internet connectivity to receive logical replication updates.  Access is tied to the S3DF NAT IP.

Disaster Recovery
=================
.. RTO/RPO expectations for application.

The sync for the ``sbn146_rubin_usdf_obs_table_sub`` took seven hours and forty minutes when the table size was 234 GB.  There is one replication slot from the Minor Planet Center Annex.
