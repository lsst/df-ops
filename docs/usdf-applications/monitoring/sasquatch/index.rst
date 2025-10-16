#########
Sasquatch
#########
.. Replace heading with application name

Overview
========
.. Include short summary of application, service, or database

Sasquatch is the Rubin Observatory’s service for metrics and telemetry data.  Sasquatch is built on Kafka and InfluxDB and provides collecting, storing, and querying of time-series data.  This instance has EFD data replicated in real-time from the Summit.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Service Grouping
     - Monitoring and Telemetry
   * - Operating Hours
     - 24x7
   * - Service Tier
     - Critical
   * - GitHub Application Code Repository
     - N/A
   * - GitHub Deployment Repository
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/sasquatch
   * - Slack Support Channel
     - sasquatch-support
   * - Slack Alerts Channel
     -
   * - Prod vCluster
     - usdf-rsp
   * - Int vCluster
     - usdf-rsp-int
   * - Dev vCluster
     - usdf-rsp-dev

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
