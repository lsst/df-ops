######################
Requests and Incidents
######################

.. _create_snow_request:

Open a SLAC Service Now Ticket
==============================

The `Rubin Jira <https://rubinobs.atlassian.net/>`__ instance is integrated with the SLAC Service Now as a two way integration.  Tasks created in the Jira USDF Service Management space will create Service Now Incidents.  Comments between Jira and Service Now are synchronized both ways.   To create a ticket perform the following.

#. Click **Create**: Look for the teal **Create** button in the top navigation bar.
#. Under **Space** select **USDF Service Management**
#. For work type select **Task**
#. Fill in the below fields.

    .. list-table::
      :widths: 25 25
      :header-rows: 1

      * - Field
        - Purpose
      * - Summary
        - The title of the task.
      * - Description
        - The details/instructions.

#. Once complete with filling in the fields click **Create** at the bottom of the window.
#. A small pop-up will appear in the bottom-left corner with a link.  Click that if you need to go back and add more detail.

Please note the following when opening tasks in Jira.
#. Attachments on the Task will not be sent to Service Now.
#. No assignee needs to be set.  The incident will be assigned in Service Now.
#. The person's name working the Service Now Incident are included in comments.

The ability to create tickets with usdf-help@slac.stanford.edu is being depreciated.  Please open tickets with Jira.

Report Incident in Slack
========================

Slack channels in the Rubin Observatory Slack instance are used to report incidents.  An on call rotation is created to monitor the below Slack channels during daytime working hours.  The on call rotation uses the Slack group handles below and should be used when creating incidents.  Please refrain from @ a specific person when creating the incident.  Note that Slack channels will not be monitored during observing as SLAC is not currently staffed for this.

In the event that Slack is down email and Zoom will be used.

.. list-table:: Slack Channels
   :widths: 10 70 10
   :header-rows: 1

   * - Slack Channel
     - Purpose
     - Slack User Group Handle
   * - usdf-on-sky-support
     - Channel for issues, questions, and support requests for USDF related to LSSTCam on-sky commissioning.  Should be limited to issues have an impact on decisions about commissioning activities at the summit on roughly 12- to 48-hour timescales
     - usdf-help
   * - usdf-support
     - USDF user support channel. Intended for issues by end users
     - usdf-help
   * - usdf-infra-support
     - USDF infrastructure support channel, i.e., intended for developers of USDF-hosted services to raise support <br>issues related to USDF infrastructure
     - usdf-help
   * - usdf-rsp-support
     - USDF Rubin Science Platform support
     - usdf-rsp-help
