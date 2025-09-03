#####
Roles
#####

Application Team Roles
======================

Each Rubin application will have the following roles defined in the table below to manage and operate the application.  A person can hold more than one role.

The roles are documented in Confluence `here <https://rubinobs.atlassian.net/wiki/spaces/LSSTOps/database/869499108?atl_f=PAGETREE>`__.  Views are available on the tabs to filter by the Application Grouping.

.. list-table:: Application Roles
   :widths: 25 25
   :header-rows: 1

   * - Role
     - Responsibilities
   * - Application Sponsor
     - Responsible for assigning resources.  This person is an Ops Team Leader or designate.
   * - Application Owner
     - Responsible for the overall application functionality, data, and user experience.  Similar to a product owner.
   * - Database Administrator
     - Responsible the database’s design, performance, security, and maintenance.  Absent if no database.
   * - Application Infrastructure
     - Responsible for the infrastructure configuration, deployment, and routine maintenance
   * - Operations Support
     - Responsible for the support of the application.  Handles alerts, application monitoring, application incident response
   * - Documentation Lead
     - Ensures all documentation is created and up to date.

SLAC and Rubin Team Infrastructure Roles
========================================

Below are the roles and responsibilities for the SLAC and Rubin Infrastructure teams.

.. list-table:: SLAC and Rubin Team Infrastructure Roles
   :widths: 25 25
   :header-rows: 1

   * - Role
     - Responsibilities
   * - Infrastructure Services Support (Physical)
     - Responsible for physical datacenter, servers, storage, and networking.  This includes Weka and Ceph.
   * - Applications and Users (Virtual)
     - Responsible for the virtual infrastructure, Kubernetes cluster, vClusters and Kubernetes Weka Storage.  The DBA is on this team and is responsible for Butler and providing subject matter expertise to help the App DBAs.
   * - Astro Domain / Rubin Specific
     - Understanding Science Operations, Teams, and Roles.  They may also be application owners.
