################
Embargo Transfer
################
.. Replace heading with application name

Overview
========
.. Include short summary of application, service, or database

This service is responsible for half of the USDF end of the Summit-to-USDF image transfer system.
(The other half is ingestion into Prompt Processing.)
Its primary goal is to ingest the incoming raw images (science, wavefront sensor, and guider) into the ``embargo`` Butler repository.
It also defines visits that include those raw images.
Finally, it includes an auxiliary microservice used by Prompt Processing that returns image object names based on group identifier and detector (and snap number, if snaps are used) after those images have been received.

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Application Grouping
     - Data Curation
   * - Operating Hours
     - 24x7 (most critical during observing, but daytime calibrations are also important)
   * - Criticality Level
     - Real Time
   * - GitHub Application Code Repository
     - ``lsst-dm/embargo-butler``
   * - GitHub Deployment Repository
     - ``slaclab/usdf-embargo-deploy``
   * - Slack Support Channel
     - ``usdf-data-curation``
   * - Slack Alerts Channel
     -
   * - Prod vCluster
     - ``usdf-embargo-dmz``
   * - Dev vCluster
     - ``usdf-embargo-dmz-dev``

.. toctree::
   :maxdepth: 2

   info
   documentation-training
   security
   procedures
   troubleshooting
