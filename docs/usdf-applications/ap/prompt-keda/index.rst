###########
Prompt KEDA
###########

Overview
========
.. Include short summary of application, service, or database

Autoscaler for Prompt Processing that creates KEDA Scaled Jobs in Kubernetes as Next Visit Fanned Out Events arrive.  KEDA stands for Kubernetes Event-driven Autoscaling.

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
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/keda
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
