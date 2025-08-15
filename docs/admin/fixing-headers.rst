Updating obs_lsst headers
=========================

1. Update https://github.com/lsst/obs_lsst

   - ``obs_lsst/python/lsst/obs/lsst/translators/lsstCam.py:fix_header``

2. Setup environment on ``rubin-devel``

.. code:: bash

   source /cvmfs/sw.lsst.eu/almalinux-x86_64/lsst_distrib/w_2025_29/loadLSST.sh
   setup lsst_distrib

3. Add local obs_lsst to ``eups`` environment

.. code:: bash

   git clone https://github.com/lsst/obs_lsst.git && cd obs_lsst

   git checkout main

   scons

   # add to eups
   setup -r .

   # verify local obs_lsst, should say LOCAL:{path}
   eups list --setup obs_lsst

4. Run script (remove echo when ready)

.. code:: bash

   day_obs=20250715; for seq_num in $(seq -w 000205 001218); do echo butler ingest-raws embargo --regex '[W\d]\d.fits$' -t direct -j 10 --output-run LSSTCam/raw/all --update-records s3://embargo@rubin-summit/LSSTCam/${day_obs}/MC_O_${day_obs}_${seq_num}/; done
