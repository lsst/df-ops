#####################
Consolidated Database
#####################
.. Replace heading with application name

Overview
========
.. Include short summary of application, service, or database

The Rubin Observatory Consolidated Database (CDB) supports scientific analysis, calibration, and quality control of astronomical observations by serving as a structured repository for managing and organizing observational data collected by the observatory’s instruments. It provides a standardized framework to store, index, and retrieve key details about exposures, visits, and detector-level observations. The database defines relationships between various observational parameters—such as timestamps, spatial positions, atmospheric conditions, and instrument settings—and has broad applicability throughout the project.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Application Grouping
     - QA
   * - Operating Hours
     - 24x7
   * - Criticality Level
     -
   * - GitHub Application Code Repository
     - https://github.com/lsst-dm/consdb
   * - GitHub Deployment Repository
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/consdb
   * - Slack Support Channel
     - consolidated-database
   * - Slack Alerts Channel
     -
   * - Prod vCluster
     - usdf-rsp
   * - Dev vCluster
     - usdf-rsp-dev

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
