#####################
S3 File Notifications
#####################
.. Replace heading with service name

Overview
========
.. Include short summary of the service

The S3 File Notifications Kafka service receives S3 Notifications for new files created.  This is used by Prompt Processing to identify when image files have been transferred to the USDF and for Data Transfer Monitoring to monitor file transfers.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Service Grouping
     - Data Curation
   * - Operating Hours
     - 24x7
   * - Criticality Level
     - Real Time
   * - GitHub Application Code Repository
     - N/A
   * - GitHub Deployment Repository
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/s3-file-notifications
   * - Slack Support Channel
     - lsstcam-prompt-processing
   * - Slack Alerts Channel
     - lsstcam-prompt-processing
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
