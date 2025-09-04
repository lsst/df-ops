#######################
Summit Database Replica
#######################
.. Replace heading with application name

Overview
========
.. Include short summary of application, service, or database

The consolidated database, exposurelog, narrativelog, and nightreport Postgres databases are replicated from the Summit to the USDF.  The hostname for the summit instance is ``db-lhn.cp.lsst.org``.  Logical Replication in Postgres is used to replicate the databases across the LHN.  Physical Replication was previously set up, but was found to be too unstable in the event of network issues and with rebuilds weekly and sometimes multiple times a week.  Physical Replication also requires the entire contents of the database instance be replicated which was not ideal because extra databases were replicated that are not needed at the USDF.  Logical Replication allows for selective replication of schemas and tables.

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
     - Refer to the ConsDB and ExposureLog/NarrativeLog applications
   * - GitHub Deployment Repository
     - https://github.com/slaclab/rubin-usdf-summit-db-replica-deploy
   * - Slack Support Channel
     - ops-df-databases
   * - Slack Alerts Channel
     - ops-usdf-alerts
   * - Prod vCluster
     - usdf-summitb
   * - Dev vCluster
     - None

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
