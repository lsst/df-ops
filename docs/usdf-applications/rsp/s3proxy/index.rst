#######
s3proxy
#######
.. Replace heading with application name

Overview
========
.. Include short summary of application, service, or database

Application to gateway S3 URLs to HTTPS at the USDF.  s3proxy is an interface between the Portal and HiPS maps.

It is used because the Portal requires HTTP/HTTPS URLs, we need to provide authenticated access, and signed URLs might not have a long enough lifetime (otherwise, redirecting to a signed URL and avoiding having the object contents pass through the proxy would be preferable).

.. Include Application Grouping, Operating Hours (24x7, PST daytime, or observing), Criticality Level, a link to the GitHub repository, and Slack channel used for support of the application.

.. list-table::
   :widths: 25 50

   * - Service Grouping
     - Rubin Science Platform
   * - Operating Hours
     - 24x7
   * - Service Tier
     - Operational
   * - GitHub Application Code Repository
     - https://github.com/lsst-dm/s3proxy
   * - GitHub Deployment Repository
     - https://github.com/lsst-sqre/phalanx/tree/main/applications/s3proxy
   * - Slack Support Channel
     - usdf-rsp-support
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
