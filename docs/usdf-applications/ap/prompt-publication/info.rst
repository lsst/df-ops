#######################
Application Information
#######################

Architecture
============

Async Python worker with 5 concurrent tasks: Kafka ingestion, Unembargo, Repo Main copy, Google Publish, and Dimension Record Copy. State tracked in a PostgreSQL database.
See `DMTN-330 <https://dmtn-330.lsst.io/>`_.

Architecture Diagram
====================

See `DMTN-330 <https://dmtn-330.lsst.io/>`_.

Associated Systems
==================

`Prompt Processing Butler Writer <https://github.com/lsst-dm/prompt_processing_butler_writer>`__  service (upstream, produces Kafka events consumed by this service).  See `DMTN-310 <https://dmtn-310.lsst.io/>`__.

Configuration Location
======================

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Config Area
     - Location
   * - Configuration
     - Env vars defined in `ServiceConfig model <https://github.com/lsst-dm/prompt_publication_service/blob/main/python/lsst/prompt_publication_service/service.py#L39>`__, prefix ``promptpub_``; Phalanx chart ``applications/prompt-pub``
   * - Vault Secrets Dev
     -
   * - Vault Secrets Prod
     - state_database_password, kafka password, lsst_db_auth_credentials, S3 credentials, AlloyDB credentials JSON

Data Flow
=========

Consumes ``BatchIngestedEvent`` messages from Kafka (topic ``butler-writer-ingestion-events``) to learn of new datasets. Datasets flow embargo → prompt_prep → main and prompt after embargo period.

Dependencies - S3DF
===================

Weka, Embargo storage, Butler repositories (``embargo``, ``prompt_prep``, ``main``), PostgreSQL state DB, Kafka.

Dependencies - External
=======================

Google Cloud AlloyDB.

Disaster Recovery
=================

.. RTO/RPO expectations for application.
