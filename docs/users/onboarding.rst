#########################
SLAC Onboarding Procedure
#########################

Overview
========

The SLAC onboarding procedure involves the following steps:

#. Make sure your Rubin Onboarding Form has been submitted on your behalf.
#. Request an invitation to the SLAC Gateway.
#. Complete SLAC cyber training
#. Complete VCR100 Access Control Training and send the certificate.
#. Register your SLAC Account in S3DF
#. Fill out the `Rubin Observatory Staff Access Form <https://ls.st/staff-access-form>`__ (if you have not already done so as part of Rubin onboarding)

SLAC IT will create Active Directory (AD) and unix accounts (for the same username). The AD account needs to be accessed every 60 days; notifications are sent out.  Once IT creates the accounts, a link will be emailed to reset the passwords.

Notes:

* If you already have a SLAC unix account, you do not need to be re-onboarded via the SLAC Gateway. However, you may need to follow steps 1, 4, and 5 below.
* If you only have a SLAC Confluence account (e.g., for DESC or LSSTCam), you will still need to be onboarded as a user, **and** there may be complications with your accounts. SLAC and Rubin Confluence sites are independent installations.

  - If your existing Confluence account name is longer than 8 characters (or if for some reason your unix account name did not match your Confluence one), you will need a different name. In that case, a new Confluence identity is created using your unix account name, added to DESC permissions, and your old account is deleted.
  - Otherwise, you will need to login to Confluence once with the unix password, then the Confluence admins will merge the unix and Confluence identities.
  - Once all this happens, Confluence will use your unix account password for authentication; if it expires, it's the unix account password that will need to be changed. There are no longer Confluence-specific accounts/passwords.

Onboarding Steps
================

Please follow the steps below to complete the onboarding process.

1. Have a Completed Rubin Onboarding Form
"""""""""""""""""""""""""""""""""""""""""

New users are required to USDF are required to have been onboarded onto Rubin Project. As such, the user's supervisor in Rubin should fill out the `Rubin Onboarding Form <https://project.lsst.org/onboarding/form>`__ and select the USDF Account Needed option.

2. Request an Invitation from SLAC Gateway
"""""""""""""""""""""""""""""""""""""""""""

Once a Rubin Onboarding Form has been completed on your behalf, simply reach out to Sierra Villarreal to request an invitation via the SLAC Gateway. She can be reached via Slack (LSST Discovery Alliance or Rubin Project) or e-mail at sierrav@slac.stanford.edu.

3. Cyber Training
"""""""""""""""""

Cyber training comes up annually. You will need to use your Active Directory (aka Windows) account to log into the training website.  Note that you will need to use your SLAC SID wherever a "username" is requested.

The SLAC training website is https://slactraining.csod.com/ and the interim training password is "SLACtraining2005!". If it does not work, email slac-training via the link on that entry page and ask them to reset it. Then go back to the original link, enter your SID and this password, and do course CS100.  DO NOT click on "Forgot Password?".

Note that if you have received an email saying that your training is coming due, the SLAC System ID (SID) is embedded in the url in the email as "sid=xxxxxx".

If you still have problems, ask your SLAC POC for help.

**SLAC cyber training must be done within 2 weeks to keep the account enabled.**

4. Access Control Training
""""""""""""""""""""""""""

Access Control Training needs to be completed prior to be granted access to Rubin USDF resources. You will need to use your Active Directory (aka Windows) account to log into the `training website <https://slactraining.csod.com/>`__ (same as in previous step). The training is listed as VCR100. Please inform Sierra Villarreal (sierrav@slac.stanford.edu) upon completion of this training, or if you find that the training has not been assigned to you.

5. Register your SLAC Account in S3DF
""""""""""""""""""""""""""""""""""""""""""

This is the same as step 4 of the `S3DF Accounts and Access page <https://s3df.slac.stanford.edu/#/accounts>`__.   This step should be performed *before* accessing any resources, including S3DF accounts and the USDF Rubin Science Platform.

6. Fill out the Rubin Observatory Staff Access Form
"""""""""""""""""""""""""""""""""""""""""""""""""""

Some of the resources and data accessible from the USDF are meant to be only available to Rubin staff.  Please fill out the `Rubin Observatory Staff Access Form <https://ls.st/staff-access-form>`__ to help us determine whether you can be regarded as a Rubin team-member for the purposes of accessing these staff-only resources.

Troubleshooting Accounts
========================

From an S3DF node, check that you are a member of the ``rubin_users`` group::

  $ id <your username>

Contact your SLAC POC to request access to that group.

Accounts can get disabled a number of ways:

- Out-of-date password (`unix password reset <https://unix-password.slac.stanford.edu/>`__).
- Out-of-date cyber training (`training link <https://slactraining.skillport.com/skillportfe/login.action>`__)
- Accounts can also be locked out if too many attempts with the wrong password are made.  File a `Service Now ticket <https://slacprod.servicenowservices.com/gethelp.do>`__ to request a reset.  Alternatively, it's often quicker to call the `SLAC IT Service Desk <https://it.slac.stanford.edu/support>`__ directly for help with passwords.

Users are warned via several emails about these events, but in case those emails have been ignored/forgotten, the following resources can be used to find any issues:

- The `accounts site <https://www-internal.slac.stanford.edu/comp/admin/bin/account-search.asp>`__  can tell us if the account is disabled.  If it's not disabled, then the password has expired.
- The `training site <https://www-internal.slac.stanford.edu/esh-db/training/slaconly/bin/ETA_ReportAll.asp?opt=6>`__ can tell us if cyber training has expired.

Currently, both of these sites are only available within the SLAC internal network.
