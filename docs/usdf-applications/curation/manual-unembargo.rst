################
Manual Unembargo
################

From time to time, there may be errors within obs headers, such as faults or bugs that cause images to be taken with ``can_see_sky=True`` or ``can_see_sky=None`` when in fact it was not possible to see the sky.
These images would normally have to wait for the full embargo period before being copied out of embargo, which can significantly hamper the Calibrations Team.
The process below will allow these images to be unembargoed manually.

#. Ensure that a DM Jira ticket has been filed with the observation ids (``day_obs`` and ``seq_num``) of the images that were taken with incorrect metadata.

#. **Check** what the header should be changed to. This may involve certification from experts. For ``can_see_sky``, check that the images were in fact taken inside the dome, which may require experts spot-checking images in RubinTV to ensure that they don't have astronomical objects.

#. Add the ``day_obs`` and ``seq_num`` ranges to the ``fix_ranges`` dictionary in the ``obs_lsst`` `translator code <https://github.com/lsst/obs_lsst/blob/main/python/lsst/obs/lsst/translators/lsstCam.py#L164-L171>`__.  Get this reviewed and merged to ``main``.

#. Setup the local version of ``obs_lsst``

   .. code:: bash

      # update environment
      source /cvmfs/sw.lsst.eu/almalinux-x86_64/lsst_distrib/w_2025_29/loadLSST.sh
      setup lsst_distrib

      # Add obs_lsst to eups environment
      git clone https://github.com/lsst/obs_lsst.git && cd obs_lsst
      git checkout main

      scons

      # add to eups
      setup -r .

      # verify local obs_lsst, should say LOCAL:{path}
      eups list --setup obs_lsst

#. Ensure s3 and database credentials are set

   .. code:: bash

      # s3 credentials are located in $HOME/.lsst/aws-credentials.ini
      export AWS_PROFILE=embargo_rw

      # postgres credentials
      export PGPASSFILE=$HOME/.lsst/postgres-credentials.txt
      export PGUSER=rubin


#. Reingest the raw images (``echo`` is for a dry-run)

   .. code:: bash

      # Remove echo when ready
      day_obs=20250715; for seq_num in $(seq -w 000205 001218); do echo butler ingest-raws embargo --regex '[W\d]\d.fits$' -t direct -j 10 --output-run LSSTCam/raw/all --update-records s3://embargo@rubin-summit/LSSTCam/${day_obs}/MC_O_${day_obs}_${seq_num}/; done

      # Verifying the ingest
      # Exposure sequence numbers are 5 digits and need to be padded with zeroes
      butler query-datasets --collections LSSTCam/raw/all embargo --where "instrument='LSSTCam' and exposure=YYYYMMDDXXXXX"


   * ``--regex``: Exclude guiders that cannot be ingested using ``ingest-raws``

   * ``-t direct``: Mandatory because raws do not live in the butler repo's datastore

   * ``-j 10``: Speed things up a bit

   * ``--output-run``: the default, but it's there for safety

   * ``--update-records``: is required to fix headers

#. Login to the ``usdf-embargo-dmz`` vcluster using ``https://k8s.slac.stanford.edu/usdf-embargo-dmz`` and execute the ``catchup-raw.sh`` script from ``slaclab/usdf-embargo-deploy/kubernetes/overlays/transfer`` with the date. This script deploys a Kubernetes Job to the cluster that re-scans the exposure dimension and unembargo the data.

   .. code:: bash

      git clone https://github.com/slaclab/usdf-embargo-deploy

      # script is in this branch
      git checkout tickets/DM-51916

      cd kubernetes/overlays/transfer

      bash ./catchup-raw.sh <YYYY-MM-DD>
