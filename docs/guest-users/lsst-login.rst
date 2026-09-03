##################################################
S3DF: SLAC Shared Science Data Facility Hosts USDF
##################################################

The USDF is hosted on the S3DF cluster at SLAC. The resource is shared amongst projects, and is documented here:

https://s3df.slac.stanford.edu/public/doc/#/

The following login load-balancer is run by SLAC to jump to select Rubin Observatory development resources at SLAC.  Note that almost nothing useful can be done on the login nodes themselves:

- ``s3dflogin.slac.stanford.edu``

USDF usage questions can be posted to the LSST Discovery slack in the #usdf-rac-users channel.

Connecting and Authenticating to Rubin servers
==============================================

You'll need to be a member of the ``rg`` unix group to access RAC resources. If you're finding that you cannot, this is probably why. Ask to be added in the ``#usdf-rac-users`` slack channel or contact your SLAC POC.

You can use `NoMachine <https://s3df.slac.stanford.edu/#/tutorials?id=graphics-and-remote-visualization>`__ for ssh access as well:

https://s3dfnx.slac.stanford.edu/

You should ssh into servers at SLAC with your unix account and password. It is only visible from the s3df login nodes. Use the load balancer:

ssh ``iana`` (note: do not add the .slac.stanford.edu postfix!)

Outbound Access
===============

Currently the s3df is in private IP space, so a squid proxy is used to access the outside world. Your .bashrc was configured when your account got created to set environment variables to make use of the proxy. You should not overwrite the section of your .bashc that sets HTTPS_PROXY (and similar).

Should you have overwritten your .bashrc, this snippet is what set up the environment variables:

.. code-block:: text

   # SLAC S3DF - source all files under ~/.profile.d
   if [[ -e ~/.profile.d && -n "$(ls -A ~/.profile.d/)" ]]; then
      source <(cat $(find -L  ~/.profile.d -name '*.conf'))
   fi

Guest RSP
=========

An RSP has been deployed. Your SLAC Windows credential will be used for authentication.

https://usdf-lsstsci.slac.stanford.edu/

