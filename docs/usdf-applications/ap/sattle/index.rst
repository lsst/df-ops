################################
Sattle Satellite Catalog Service
################################
.. Replace heading with application name

Overview
========
.. Include short summary of application, service, or database

This application manages the catalog of satellite orbits that is used to filter difference image sources to determine which are allowed to be emitted as Alerts.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Application Grouping
     - Alert Production
   * - Operating Hours
     - Observing
   * - Criticality Level
     - Real Time
   * - GitHub Repository
     - https://github.com/lsst-dm/sattle
   * - Slack Support channel
     -
   * - Prod vCluster
     - Not applicable.  Installed on S3DF servers.
   * - Dev vCluster
     - Installed on S3DF servers.

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
