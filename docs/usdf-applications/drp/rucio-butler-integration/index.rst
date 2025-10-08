########################
Rucio-Butler Integration
########################
.. Replace heading with application name

Overview
========
.. Include short summary of application, service, or database

Registers Butler files with Rucio at the USDF, France, and UK Data Facilities.  Installed as modification to Rucio container.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Service Grouping
     - Data Release Production
   * - Operating Hours
     - 24x7
   * - Service Tier
     - Critical
   * - GitHub Application Code Repository
     - * https://github.com/lsst-dm/ctrl_ingestd
       * https://github.com/lsst-dm/ctrl_rucio_ingest
   * - GitHub Deployment Repository
     - https://github.com/slaclab/rubin-rucio-deploy
   * - Slack Support Channel
     - df-data-movement
   * - Slack Alerts Channel
     -
   * - Prod vCluster
     - usdf-rucio
   * - Dev vCluster
     - usdf-rucio-dev

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
