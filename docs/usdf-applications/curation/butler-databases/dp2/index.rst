###
DP2
###

Overview
========
The postgres database is the Butler *registry* for DP2 - it stores dataset provenance
and metadata (dimension records, dataset type definitions, collections, and
datastore URIs), not the underlying image/table bytes, which are stored as files
in object storage and referenced by URI.

DP2 is Rubin's first data preview built from real on-sky observations with the LSST
Camera, processed with Rubin Science Pipelines v30. Registered dataset types include:

- **Images**: ``raw_exposure``, ``visit_image``, ``deep_coadd``, ``template_coadd``, ``difference_image``
- **Catalogs**: ``object``, ``source``, ``forced_source``, ``dia_object``, ``dia_source``, ``dia_object_forced_source``, ``ss_object``, ``ss_source``, ``mpc_orbits``, ``visit``, ``visit_detector``

See `DP2 <https://dp2.lsst.io/index.html>`_ for more information.

.. list-table::
   :widths: 25 50

   * - Application Grouping
     - Data Curation
   * - Operating Hours
     - 24*7
   * - Criticality Level
     - High
   * - GitHub Application Code Repository
     - Not applicable
   * - GitHub Deployment Repository
     - https://github.com/slaclab/rubin-pg-deploy/tree/main/usdf-butler-dp2
   * - Slack Support channel
     - ops-df-databases
   * - Slack Alerts channel
     - ops-usdf-alerts
   * - Prod vCluster
     - vcluster--usdf-dp2


.. toctree::
   :maxdepth: 2

   access
   backup
   monitoring
