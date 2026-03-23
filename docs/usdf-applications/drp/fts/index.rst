####
FTS3
####
.. Replace heading with application name

Overview
========
.. Include short summary of application, service, or database

FTS3 is the service responsible for globally distributing the majority of the LHC data across the WLCG infrastructure. It is a low level data movement service, responsible for reliable bulk transfer of files from one site to another while allowing participating sites to control the network resource usage.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Service Grouping
     - Data Release Production
   * - Operating Hours
     - 24x7
   * - Service Tier
     - Critical
   * - GitHub Application Repository
     - https://github.com/cern-fts/fts3
   * - GitHub Deployment Repository
     - https://github.com/slaclab/rubin-fts3-deploy
   * - Slack Support Channel
     - df-data-movement, data-curation-team
   * - Slack Alerts Channel
     -
   * - Prod vCluster
     - usdf-fts3
   * - Dev vCluster
     - usdf-fts3-dev

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
