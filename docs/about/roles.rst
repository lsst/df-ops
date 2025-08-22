#####
Roles
#####

Application Team Roles
======================

Each Rubin application will have the following roles defined to manage and operate the application.  A person can hold more than one role.

.. list-table:: Application Roles
   :widths: 25 25
   :header-rows: 1

   * - Role
     - Responsibilities
   * - Application Sponsor
     - Responsible for assigning resources
   * - Application Owner
     - Responsible for the overall application functionality, data, and user experience
   * - Database Administrator
     - Responsible for the database schema design, identifying capacity needs, and active monitoring of the database performance.  Absent if no database.
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
     - Responsible for the virtual infrastructure, Kubernetes cluster, vClusters and Kubernetes Weka Storage.  The DBA role is on this team and is Database Administration and providing subject matter expertise to help the App DBAs.
   * - Astro Domain / Rubin Specific
     - Understanding Science Operations, Teams, and Roles.  They may also be application owners.

Database Management Responsibilities
====================================

The S3DF Infrastructure DBA is responsible for the following activities.
  * Installation of Cloud Native Postgres Operator and Postgres instances.
  * Database version and operator upgrades.  The Application DBA will be consulted on the what time to perform the upgrades.
  * Database maintenance tasks.  This includes setting up backups, monitoring backups, performing restores, monitoring index performance, and rebuilding indexes.
  * Setting up of database monitoring tools, alerts, and dashboards.  These will be used by Application DBAs to identify performance issues.

The Application DBA is responsible for the following activities:
  *  Definition of the database data model.
  *  Capacity requirements.  Identifying resource needs for the database.
  *  Defining what to monitor and what is important for application database performance.
  *  Active monitoring of the database performance and identifying performance issues.
  *  Testing of database restores if this is required.  The S3DF Infrastructure DBA monitors backups.
