###################################
Rucio Storage Element Configuration
###################################

Overview
========
From the `Rucio documentation`_:

    Rucio Storage Element (RSE) is the logical abstraction of a storage system for physical files. It is the smallest unit of storage space addressable within Rucio. It has a unique identifier and a set of meta attributes describing properties such as supported protocols (https, srm, s3, ...), host/port address, quality of service, storage type (disk, tape, ...), physical space properties (used-, available-, non-pledged space), and geographical zone.

.. _Rucio documentation: https://rucio.github.io/documentation/started/concepts/rucio_storage_element/

Current RSEs
============

.. list-table:: Independent Data Access Centers (IDACs)
   :widths: 50 25
   :header-rows: 1

   * - Location
     - RSE Name(s)
   * - IN2P3
     - DESC_IN2P3
   * - NERSC
     - DESC_NERSC
   * - Australia
     - IDAC_AUS-AAL
   * - Brazil
     - IDAC_BRA-LIN
   * - Canada
     - IDAC_CAN-CAN
   * - Spain
     - IDAC_ESP-BCM
   * - Japan
     - IDAC_JAP-JPG
   * - Mexico
     - IDAC_MEX-UNA
   * - Poland
     - IDAC_POL-NCB
   * - UK
     - IDAC_UKD-UKD
   * - University of Washington
     - IDAC_US-UW


Distances
=========
Rucio uses the notion of distance to model preference for transferring data among storage elements when the same file is present in two or more sources. Distance values are not physical measurements, but determine preference. For transfers between RSEs, distances must be set. These distances are unidirectional; for bidirectional transfers, distances to and from the source and destination must be set.

For Rubin, discussion in `DM-45161`_ determined the distances for our RSEs as follows:

.. list-table::
   :widths: 50 25
   :header-rows: 1

   * - Region/Location
     - Distance
   * - Transatlantic/Transpacific
     - 10
   * - Within Europe
     - 4
   * - Same country
     - 2
   * - Same site
     - 1

.. _DM-45161: https://rubinobs.atlassian.net/browse/DM-45161
