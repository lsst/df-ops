#############################
Fixing Metadata in Raw Images
#############################

**Caution:** The fix described here actually happens in butler repos that have those problematic
raw images in their datastores. The raw images themselves are never altered.

From time to time, there may be errors within obs headers, typical issues are:

* Faults or bugs that cause images to be taken with ``can_see_sky=True`` or ``can_see_sky=None`` 
  when in fact it was not possible to see the sky. These images would normally have to wait for
  the full embargo period before being copied out of embargo, which can significantly hamper the
  Calibrations Team.

* Wrong filter information in the image headers

This results in wrong dimension records be ingested to the embargo butler repo. The process below
will allow the dimension records in butler to be fixed. The procedure to report and obtain a fix
for these issues is as follows:

#. An issue is usually identified and reported by someone who notice the problem. Data Curation
   team should file a JIRA ticket to the OBS team to report the problem, and a JIRA ticket to
   the DM Data Engineering team to obtain a fix in ``obs_lsst`` (usually in ``lsstCam.py``). 
   Information in thos ticket usually include observation ids (``day_obs`` and ``seq_num``) of
   the images that were taken with incorrect metadata.

#. The Data Engineering team usually confirms this issue and provides a fix. In some simple cases, 
   The Data Curation team can also fix those issues by **Checking** what the header should be 
   changed to (It is best to check with experts). For ``can_see_sky``,
   check that the images were in fact taken inside the dome, which may require experts spot-checking
   images in RubinTV to ensure that they don't have astronomical objects.

#. **Skip this step if the Data Engineering team will provide a fix in ``obs_lsst``**: Add the
   ``day_obs`` and ``seq_num`` ranges to the ``fix_ranges`` dictionary in the ``obs_lsst``
   `translator code <https://github.com/lsst/obs_lsst/blob/main/python/lsst/obs/lsst/translators/lsstCam.py#L164-L171>`__.  
   Get this reviewed and merged to the ``main`` branch.

The following uses butler repo ``embargo`` as an example, but the same process applies to any
butler repo that has the affected images in its datastore.

#. Setup the local version of ``obs_lsst``

   .. code:: bash

      # update environment
      source /cvmfs/sw.lsst.eu/almalinux-x86_64/lsst_distrib/w_2026_17/loadLSST.sh
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


#. Update the butler dimension records (``echo`` is for a dry-run)

   .. code:: bash

      # Make sure SHELL is bash
      # Remove echo when ready
      day_obs=20250715 
      REPO=embargo
      for seq_num in $(seq -w 000205 001218); do 
          # Old command
          #echo butler ingest-raws $REPO --regex '[W\d]\d.fits$' -t direct -j 10 --output-run LSSTCam/raw/all --update-records s3://embargo@rubin-summit/LSSTCam/${day_obs}/MC_O_${day_obs}_${seq_num}/;
          # New command
          echo butler update-exposures-from-raws $REPO LSSTCam --where "exposure=${day_obs}${seq_num: -5}"
      done

      # Verifying the ingest
      # Exposure sequence numbers (XXXXX below) are 5 digits and need to be padded with zeroes
      butler query-datasets --collections LSSTCam/raw/all $REPO --where "instrument='LSSTCam' and exposure=YYYYMMDDXXXXX"


   * ``--regex``: Exclude guiders that cannot be ingested using ``ingest-raws``

   * ``-t direct``: Mandatory because raws do not live in the butler repo's datastore

   * ``-j 10``: Speed things up a bit

   * ``--output-run``: the default, but it's there for safety

   * ``--update-records``: is required to fix headers

If the raw images haven't been unembargoed, the following process can manually unembargo the
data after the metadata is fixed.

#. Login to the ``usdf-embargo-dmz`` vcluster using ``https://k8s.slac.stanford.edu/usdf-embargo-dmz`` and execute the ``catchup-raw.sh`` script from ``slaclab/usdf-embargo-deploy/kubernetes/overlays/transfer`` with the date. This script deploys a Kubernetes Job to the cluster that re-scans the exposure dimension and unembargo the data.

   .. code:: bash

      git clone https://github.com/slaclab/usdf-embargo-deploy

      # script is in this branch
      git checkout tickets/DM-51916

      cd kubernetes/overlays/transfer

      bash ./catchup-raw.sh <YYYY-MM-DD>

If the raw images has been unembargoed, then the downstream butler repos (USDF ``main`` bulter
and FrDF and UKDF butlers) will need those updated butler dimension records as well.i

Each exposure has a corresponding Rucio dataset (e.g. ``raw:Dataset/LSSTCam/raw/Obs/20250715/MC_O_20250715_000205``).
This dataset has a .zip file that contains the raw .fits files and json files, and a _dimensions.yaml
file that contains the (incorrect) dimension records for that exposure. We will need to create 
a new _dimensions.1.yaml file with the correct dimension records, and add it to the same Rucio dataset.
To do so:

#. Download and run `create_rawdata_dimensions_yaml.py <https://github.com/lsst-dm/data-curation-tools/blob/main/bin.src/create_rawdata_dimensions_yaml.py>`_

    .. code:: bash

       git clone https://github.com/lsst-dm/data-curation-tools.git && cd data-curation-tools/bin.src

       day_obs=20250715
       seq_num=000205

       python create_rawdata_dimensions_yaml.py ${day_obs}${seq_num: -5}
       # This will create a file named ``MC_O_20250715_000205_dimensions.1.yaml`` in the current directory.

#. Upload the new dimensions yaml file to Rucio

    .. code:: bash

       day_obs=20250715
       seq_num=000205

       # instrCode="MC"
       # controller="O"
       # obsId=${instrCode}_${controller}
       obsId="MC_O"   # !!! sometimes this could be "MC_C". Check what was created above.

       newDimensionsYaml="${obsId}_${day_obs}_${seq_num}_dimensions.1.yaml"
       didName="LSSTCam/${day_obs}/${newDimensionsYaml}"
       obsDataset="raw:Dataset/LSSTCam/raw/Obs/${day_obs}/${obsId}_${day_obs}_${seq_num}"

       # Note "rucio upload" (below) will not work unless you login to `rubinmgr` and temporarily change
       # the permission of /sdf/data/rubin/lsstdata/offline/instrument/20250715 to world-writeable (777). 
       # Remember to change the permission back after running the rucio upload command in the next step.

       echo rucio upload --rse SLAC_RAW_DISK --scope raw --dataset $didName $newDimensionsYaml

       echo rucio did update --open $obsDataset
       echo rucio did content add --to-did $obsDataset $lfn
       echo rucio did metadata set --key SafeCopies --value "" $obsDataset
       echo rucio did metadata set --key arcBackup --value SLAC_RAW_DISK_BKUP:need $obsDataset
       echo rucio did update --close $obsDataset

The present of this new _dimensions.1.yaml is an indication that the butler dimesion records has been 
updated. If a DF hasn't ingested the raw data yet, it can directly use the new _dimensions.1.yaml to
ingest the data. If the raw data has been ingested, then the DF will need to update the dimension 
records in their butler repos using a similar process as described above for the embargo butler repo.
