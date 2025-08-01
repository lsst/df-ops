############
Prompt Kafka
############

Overview
========
.. Include short summary of application, service, or database

Kafka Cluster that receives file arrival notifications from the rubin summit S3 bucket.  These notifications are used by :doc:`../prompt-processing/index`.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Application Grouping
     - Alert Production
   * - Operating Hours
     - Observing
   * - Criticality Level
     -
   * - GitHub Repository
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/prompt-kafka
   * - Slack Support channel
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
