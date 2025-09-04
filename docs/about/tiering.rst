###################
Application Tiering
###################

Application tiering is defined to align the operations model to supporting key Rubin processes and capabilities.  This are used as decision support for the following type of scenarios:
  * When there are multiple issues occurring and the team is constrained on what they can work on.  Real Time applications will be prioritized over critical and operational tier applications.
  * When there are hardware issues and there are limited resources to run everything
  * During disaster recovery to prioritize which applications to restore

THe below table details the application criticality levels.  The application tiering can change over time and will change for some applications after commissioning.

The application pages on this site document the criticality level for each application or database.  A combined list of the applications by tier is documented in Confluence `here <https://rubinobs.atlassian.net/wiki/spaces/LSSTOps/database/869499108?atl_f=PAGETREE>`__.  Views are available on the tabs to filter by the tier.

.. list-table:: Application Tiering
   :widths: 10 50 20 20
   :header-rows: 1

   * - Tier
     - Definition
     - Impact of Failure
     - Examples
   * - Real Time
     - Essential applications for operations that are required to run real time or supports a real time application.  They are required run in a time frame which is measured in minutes.
     - The application cannot be rerun because it is based on a real time process
     - Prompt Processing, QServ, Embargo Butler
   * - Critical
     - Essential application for operations that are not real time.  An interruption is recoverable.
     - Can cause significant delays, disruptions, or reduced productivity
     - Panda, HTCondor, Alert Archive
   * - Operational
     - Applications that support science functions, but are not considered essential for the immediate functioning of work.
     - May cause disruptions, but not major ones
     - RubinTV, Campaign Management Service
