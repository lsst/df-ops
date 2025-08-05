###########################
Minor Planet Survey Replica
###########################

Overview
========
.. Include short summary of application, service, or database

The Minor Planet Survey databases are replicated from the Minor Planet Center Annex.  Logical Replication in Postgres is used to replicate the databases over the Internet.

The USDF replica is also setup as a publication and EPO in Google Cloud subscribes to receive the same data.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Application Grouping
     - Alert Production
   * - Operating Hours
     -
   * - Criticality Level
     -
   * - GitHub Repository
     - https://github.com/slaclab/rubin-usdf-minor-planet-survey
   * - Slack Support channel
     - ops-df-databases
   * - Prod vCluster
     - usdf-minor-planet-survey
   * - Dev vCluster
     - None

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
