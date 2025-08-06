############################################
Rubin Science Platform Debugging Cheat Sheet
############################################

Has the USDF Rubin Science Platform failed for you? Listed here are some of the most common issues that have arisen in the past and possible solutions. Hopefully, this will help resolve your issue, or at least remove some of the most common options from the possibilities.

I’m getting a spawn failed error!
=================================

There are a number of reasons that can cause a spawn failed error. Some common ones include:

#. *If you had attempted to access the RSP prior to registering for Coact,* you may have a known permissions error. You can confirm this issue by going to an s3dfiana node and checking to see if your home directory is owned by root. This problem requires admin intervention and you should leave a message in #usdf-rsp-support.

#. *If you have exceeded your disk quota,* you may not be able to spawn notebooks. Log-in to s3dflogin.slac.stanford.edu and make certain that you are under the 25 GB disk quota in your home directory.

#. *Have you tried resetting the user environment?* In some limited cases, choosing the “reset user environment” option on the RSP can help to make the notebook server load correctly.

#. *Have you checked to see if you have a notebook to shutdown?* Sometimes a hard restart by choosing to shutdown the server at (https://usdf-rsp.slac.stanford.edu/nb/hub/home) can fix the problem.

#. *Leave a message in #usdf-rsp-support!* At this point, the remaining possibilities are fairly arcane and this may require further examination. Please take a screenshot of your error event, ideally identifying if you were assigned to a specific kubernetes node or the like. This will help with quicker analysis of your problem and hopefully fast resolution!

I’m getting an Invalid Response: Internal Server Error message!
===============================================================
#. These tend to be a little trickier to debug, but there are some tricks!

#. Try to load the RSP in an incognito window! Sometimes, caching issues result in not being able to load the RSP. If the RSP loads correctly in an incognito window, you may need to clear your browser cache.

#. Try resetting the user environment! It is possible that this will help the RSP notebook server load correctly.

#. Leave a message in #usdf-rsp-support! Beyond these two solutions, it is more likely to be something more esoteric, so please do not hesitate to let us know!

My RSP Notebook works, but it is going really slow!
===================================================
This can sometimes happen if your notebook has “gone stale”. Please shutdown the server and reload it. You may need to go to https://usdf-rsp.slac.stanford.edu/nb/hub/home in order to do so. If slow behavior continues, please carry out the following steps.

#. Try to confirm if it is the entire notebook or specific Butler/library requests. In some cases, even print statements can have surprisingly long run times — play around a little to determine if you can see where the Notebook is being slow.

#. Pass this information into #usdf-rsp-support. We’ll happily look into it further!