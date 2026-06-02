################################
Alert Production Database (APDB)
################################
.. Replace heading with application name

Overview
========
.. Include short summary of application, service, or database

This database is used by Alert Production that runs as a part of Prompt Production. Its performance is critical for delivery of the alerts. Due to performance constraints, Apache Cassandra was selected as a backend for production database.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Application Grouping
     - Alert Production
   * - Operating Hours
     - 24x7
   * - Criticality Level
     - Real Time
   * - GitHub Application Code Repository
     - https://github.com/lsst/dax_apdb
   * - GitHub Deployment Repository
     - https://github.com/lsst-dm/dax_apdb_deploy
   * - Slack Support Channel
     -
   * - Slack Alerts Channel
     - ops-apdb-alerts
   * - Prod hosts
     - sdfk8sk001-006
   * - Dev nodes
     - sdfk8sk007-012

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
