#################
Prompt Processing
#################

Overview
========
.. Include short summary of application, service, or database

Prompt Processing system is responsible for processing roughly a thousand visits per night, and distributing the results in near real time as alerts.

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
     - https://github.com/lsst-dm/prompt_processing
   * - GitHub Deployment Code Repository
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/prompt-keda-lsstcam
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
