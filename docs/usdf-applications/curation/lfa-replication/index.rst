############################
Large File Annex Replication
############################
.. Replace heading with application name

Overview
========
.. Include short summary of application, service, or database

Duplication of Rubin LFA S3 data to USDF.  Rubin Observatory keeps various non-image data in a S3 datastore called the Large File Annex (LFA). It is necessary to replicate the contents of this datastore at the USDF for read-only access to aid Operator analysis.

The application essentially runs an instance of mc that uses mirror to connect to both the telescope systems in Chile and the storage at SLAC.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Service Grouping
     - Data Curation
   * - Operating Hours
     -
   * - Service Tier
     - Operational
   * - GitHub Application Code Repository
     - https://github.com/slaclab/rubin-lfa-replicate-deploy
   * - GitHub Deployment Repository
     - https://github.com/slaclab/rubin-lfa-replicate-deploy
   * - Slack Support Channel
     -
   * - Slack Alerts Channel
     -
   * - Prod vCluster
     - usdf-lfa
   * - Dev vCluster
     - N/A

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
