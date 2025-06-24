###########################
Minor Planet Survey Replica
###########################
.. Short summary of application, service, or database

The Minor Planet Survey databases are replicated from the Minor Planet Center Annex.  Logical Replication in Postgres is used to replicate the databases over the Internet.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 25
   :header-rows: 1

   * - Area
     - Description
   * - Grouping
     - Alert Production
   * - Operating Hours
     -
   * - Criticality Level
     -
   * - Slack Support channel
     - ops-df-databases


.. toctree::
   :maxdepth: 2
   :caption: Overview

   roles
   mpc-replica/architecture
   sandbox/architecture
   documentation-training
   security

.. toctree::
   :maxdepth: 2
   :caption: Procedures

   mpc-replica/procedures
   sandbox/procedures

.. toctree::
   :maxdepth: 2
   :caption: Troubleshooting

   mpc-replica/troubleshooting
   sandbox/troubleshooting
