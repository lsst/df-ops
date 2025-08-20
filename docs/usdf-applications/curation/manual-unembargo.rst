################
Manual Unembargo
################

From time to time, faults or bugs may cause images to be taken with ``can_see_sky=True`` or ``can_see_sky=None`` when in fact it was not possible to see the sky.
These images would normally have to wait for the full embargo period before being copied out of embargo, which can significantly hamper the Calibrations Team.
The process below will allow these images to be unembargoed manually.

#. Ensure that a DM Jira ticket has been filed with the observation ids (``day_obs`` and ``seq_num``) of the images that were taken with incorrect metadata.

#. **Check** that the images were in fact taken inside the dome.  This may involve certification from experts and spot-checking images in RubinTV to ensure that they don't have astronomical objects.

#. Add the ``day_obs`` and ``seq_num`` ranges to the ``fix_ranges`` dictionary in the ``obs_lsst`` `translator code <https://github.com/lsst/obs_lsst/blob/main/python/lsst/obs/lsst/translators/lsstCam.py#L164-L171>`__.  Get this reviewed and merge to ``main``.

#. Setup the local version of ``obs_lsst`` and reingest the raw images with ``butler ingest-raws embargo --regex '[W\d]\d.fits$' -t direct -j 10 --output-run LSSTCam/raw/all --update-records s3://embargo@rubin-summit/LSSTCam/${day_obs}/MC_O_${day_obs}_${seq_num}/``.  The ``--regex`` option is to exclude guiders that cannot be ingested using ``ingest-raws``.  The ``-t direct`` option is mandatory because raws do not live in the butler repo's datastore.  The ``-j 10`` option is to speed things up a bit.  The ``--output-run`` is the default, but it's there for safety.  ``--update-records`` is required to fix the ``can_see_sky`` value.

#. Login to the ``usdf-embargo-dmz`` vcluster using ``https://k8s.slac.stanford.edu/usdf-embargo-dmz`` and execute the ``catchup-raw.sh`` script from ``slaclab/usdf-embargo-deploy/kubernetes/overlays/transfer`` with the date.  This will re-scan the exposure dimension and unembargo the data.
