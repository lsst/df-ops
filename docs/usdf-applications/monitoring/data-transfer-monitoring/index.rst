########################
Data Transfer Monitoring
########################
.. Replace heading with application name

.. _DTM_Overview:

Overview
========
.. Include short summary of application, service, or database

Data Transfer Monitoring is an application deployed in the usdf-embargo-dmz vCluster and Grafana Dashboard that monitors file transfer timing from the Summit to the USDF.

The dashboard for USDF staff is `here <https://grafana.slac.stanford.edu/d/dendnzcn4treoe/>`__

The simplified dashboard for Summit is `here <https://grafana.slac.stanford.edu/d/beyzhpr42z0n4c>`__

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Service Grouping
     - Monitoring and Telemetry
   * - Operating Hours
     - 24x7
   * - Service Tier
     - Operational
   * - GitHub Application Code Repository
     - https://github.com/lsst-dm/data_transfer_monitoring
   * - GitHub Deployment Repository
     - https://github.com/lsst-dm/data_transfer_monitoring
   * - Slack Support Channel
     - usdf-support
   * - Slack Alerts Channel
     -
   * - Prod vCluster
     - usdf-embargo-dmz
   * - Dev vCluster
     - N/A

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
