############
Prompt Redis
############

Overview
========
.. Include short summary of application, service, or database

Redis Cluster that receives Fanned Out events from :doc:`../next-visit-fan-out/index`.  Redis Streams is the data structure in Redis used to store Fanned Out Events that are consumed by Prompt Processing.   The rate of Fanned Out Events in Prompt Redis is used to determine Prompt Processing autoscaling.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Service Grouping
     - Alert Production
   * - Operating Hours
     - Observing
   * - Service Tier
     - Real Time
   * - GitHub Application Code Repository
     - N/A
   * - GitHub Deployment Repository
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/prompt-redis
   * - Slack Support Channel
     - lsstcam-prompt-processing
   * - Slack Alerts Channel
     -
   * - Prod vCluster
     - usdf-prompt-processing
   * - Dev vCluster
     - usdf-prompt-processing-dev

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
