##########
OpenSearch
##########
.. Replace heading with application name

Overview
========
.. Include short summary of application, service, or database

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

OpenSearch is an internal metric aggregation service for Rucio, PanDA, and HTCondor.  Display of metrics is in the S3DF Grafana.

.. list-table::
   :widths: 25 50

   * - Application Grouping
     - Data Release Production
   * - Operating Hours
     - 24x7.  Most usage during PDT daytime hours.
   * - Criticality Level
     - Operational
   * - GitHub Application Code Repository
     - Not applicable
   * - GitHub Deployment Repository
     - https://github.com/slaclab/rubin-opensearch-deploy
   * - Slack Support Channel
     - rubinobs-opensearch in Discovery Alliance Slack
   * - Slack Alerts Channel
     -
   * - Prod vCluster
     - usdf-opensearch
   * - Dev vCluster
     - No dev cluster

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
