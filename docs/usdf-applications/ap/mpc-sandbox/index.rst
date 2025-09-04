###########
MPC Sandbox
###########


Overview
========
.. Include short summary of application, service, or database

During commissioning, Rubin will send data to a private, Rubin-only, submission stream at the Minor Planet Center. They’ll process these data and store them into a private, rubin-only, instance of the *MPCORB* database. This will prevent the leakage of private Rubin data to the public before the First Look event. This parallel system called *the sandbox*.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Application Grouping
     - Alert Production
   * - Operating Hours
     - PDT Daytime
   * - Criticality Level
     - Operational
   * - GitHub Database Code Repository
     - https://github.com/slaclab/rubin-usdf-minor-planet-survey
   * - GitHub Deployment Repository
     - https://github.com/slaclab/rubin-usdf-minor-planet-survey
   * - Slack Support Channel
     - ops-df-databases
   * - Slack Alerts Channel
     - ops-usdf-alerts
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
