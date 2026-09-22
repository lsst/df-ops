##########################
Prompt Publication Service
##########################

Overview
========

Background worker service that manages the lifecycle of Prompt Data Products, such as enforcing an 80-hour embargo and replicating datasets across Butler repositories (``embargo``, ``prompt_prep``, ``main``, ``prompt``).
See `DMTN-330 <https://dmtn-330.lsst.io/>`_.

.. list-table::
   :widths: 25 50

   * - Application Grouping
     - Alert Production
   * - Operating Hours
     - 24x7
   * - Criticality Level
     - High
   * - GitHub Application Code Repository
     - https://github.com/lsst-dm/prompt_publication_service
   * - GitHub Deployment Repository
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/prompt-pub
   * - Slack Support Channel
     -
   * - Slack Alerts Channel
     - #prompt-data-publication
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
