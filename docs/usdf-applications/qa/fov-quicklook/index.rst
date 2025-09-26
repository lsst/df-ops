#############
fov-quicklook
#############
.. Replace heading with application name

Overview
========
.. Include short summary of application, service, or database

A tile-cache image viewer of both raw and calexp images in the USDF storage. It can display the full focal plane image as fast as 4 seconds with access to a pixel-level resolution. It has user-friendly capabilities such as changing the dynamic range on-the-fly, inspecting pixel values, taking a slice of the image, and showing the FITS header.

The application is an In Kind contribution from the National Astronomical Observatory of Japan (NAOJ).

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Application Grouping
     - QA
   * - Operating Hours
     - 24x7
   * - Criticality Level
     - Operational
   * - GitHub Application Code Repository
     - https://github.com/lsst-sqre/fov-quicklook
   * - GitHub Deployment Repository
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/fov-quicklook
   * - Slack Support Channel
     -
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
