##################################################################
Other Imaging Survey Data _(Beta)_
##################################################################

A Butler repository at the USDF serves coadds from surveys other than Rubin
-- currently **DES DR2**, **Euclid Q1** and the **DESI Legacy Survey** (DR9 north and DR10
south) -- through the standard ``lsst.daf.butler``
API, so you can use them next to DP2 in the same RSP kernel. The files are
read in place from their copies on USDF storage; nothing is copied into the
repository.

The coadds are served as ``lsst.images`` objects, like DP2's
``deep_coadd``: the same ``lsst.images.Box`` cutouts, the same
``sky_projection`` component, pixels in nJy, and ``.to_legacy()`` for an afw
``ExposureF`` to run LSST Tasks on.

Available Imaging Data Sets
==============

.. list-table::
   :header-rows: 1

   * - survey
     - dataset type
     - collection
     - skymap
     - bands
     - coverage
   * - DES DR2
     - ``des_tile_coadd``
     - ``DES/DR2/tile_coadds``
     - ``des_dr2_tiles_v1``
     - ``g r i z y``
     - 10,169 tiles, ~5,000 deg² of the southern sky; 0.263″ pixels
   * - Euclid Q1
     - ``euclid_tile_coadd``
     - ``Euclid/Q1/tile_coadds``
     - ``euclid_mer_tiles_v1``
     - ``I_E Y_E J_E H_E``
     - 352 MER tiles: the three Euclid Deep Fields (North, South, Fornax)
       and the LDN 1641 field; 0.1″ pixels
   * - DESI Legacy Survey DR9 north
     - ``legacysurvey_brick_coadd``
     - ``LegacySurvey/DR9/north/brick_coadds``
     - ``legacysurvey_bricks_v1``
     - ``g r z``
     - 93,548 bricks, mostly Dec > 32°; BASS (g, r) and MzLS (z); 0.262″ pixels
   * - Legacy Survey DR10 south
     - ``legacysurvey_brick_coadd``
     - ``LegacySurvey/DR10/south/brick_coadds``
     - ``legacysurvey_bricks_v1``
     - ``g r i z``
     - 366,912 bricks; DECam; 0.262″ pixels

- One **tract** per survey tile or brick; each has a single patch, ``0``.
  For Euclid the tract ID is Euclid's own MER tile ID; for the Legacy Survey
  it is NERSC's ``brickid``. A Legacy Survey brick is 0.25° and 3600 × 3600
  pixels, with all bands on one grid.
- **The two Legacy Survey releases share one dataset type and one brick
  grid**, in separate RUNs. About 16% of north bricks (mostly at Dec 25-35°
  and near the equator) also have a south coadd, so the same brick and band can exist in both (see `Things to
  know`_).
- DES and Legacy Survey bands are lowercase (``y``, as in DP2). Euclid bands
  carry an ``_E`` suffix: ``Y_E`` is Euclid's Y, not LSST's ``y``. Legacy
  Survey north's g, r and z are BASS and MzLS filters, not DECam's; south is
  DECam, like DES. South i is patchier than its other bands: it comes from
  DECam programmes other than DECaLS, and some bricks have none.
- The older per-plane dataset types are also served, for code that needs the
  files' own planes: ``des_tile_image`` (components ``sci``, ``msk``,
  ``wgt``) and ``des_tile_wcs`` in ``DES/DR2/tiles``; ``euclid_tile_image``,
  ``euclid_tile_rms``, ``euclid_tile_flag``, ``euclid_tile_psf``,
  ``euclid_tile_wcs`` and ``euclid_tile_photocalib`` in ``Euclid/Q1/MER``.
  These are in the files' own units, not nJy.

Getting access
==============

You need a USDF RSP session in group ``rubin_users`` with the **LSST**
kernel, and a line for this repository's database in your Postgres
credentials file, ``~/.lsst/postgres-credentials.txt``. The repository is
not one of the standard USDF repos: its credentials line is not created for
you, but it ships one, for a **read-only** database login (``rubin_ro``), in
its shared folder ``/sdf/data/rubin/cosmicdata/cosmic_butler/``. Back up your file first and append the line
with ``>>`` (do not point ``$PGPASSFILE`` at the shared file: Postgres
ignores a credentials file other people can read):

.. code-block:: bash

   cp "$PGPASSFILE" "$PGPASSFILE.bak-$(date +%Y%m%d)"
   cat /sdf/data/rubin/cosmicdata/cosmic_butler/postgres-credentials.txt >> "$PGPASSFILE"

The same folder holds the repository's read-only configuration
(``butler.yaml``, which logs in as ``rubin_ro``), the code its storage
classes need (``code/``) and the tutorial (``doc/``); its ``README.md`` has
the steps. Nothing needs installing: put ``code/`` on Python's path.

.. code-block:: python

   import sys

   sys.path.insert(0, "/sdf/data/rubin/cosmicdata/cosmic_butler/code")

Opening the repository
======================

Open it read-only, through ``GuardedButler``, with **every survey's
collections you will use**:

.. code-block:: python

   import des_dr2_config
   from butler_surveys.serving.guarded_butler import GuardedButler

   butler = GuardedButler.from_config(
       des_dr2_config.load().repo,
       writeable=False,
       collections=[
           "DES/DR2/tile_coadds",
           "Euclid/Q1/tile_coadds",
           "LegacySurvey/DR9/north/brick_coadds",
           "LegacySurvey/DR10/south/brick_coadds",
       ],
   )

``GuardedButler`` is a drop-in wrapper around ``Butler``. It refuses a lookup
by data ID that matches in both Legacy Survey releases, and it re-infers the
default data ID when a call names its own ``collections=`` (see `Things to
know`_); a bare ``Butler`` gets both of these silently wrong.

Finding data
============

The same spatial ``where`` clause as for DP2, on ``tract`` rather than
``patch``:

.. code-block:: python

   ra, dec = 53.13, -28.10  # ECDFS
   refs = butler.query_datasets(
       "des_tile_coadd",
       where="tract.region OVERLAPS POINT(ra, dec) AND band = b",
       bind={"ra": ra, "dec": dec, "b": "r"},
       limit=10,
       explain=False,
   )

Neighbouring tiles overlap, so a position near an edge is in two tracts.
Pick the tile whose centre is nearest your target, so a cutout sits well
inside it; ``butler_surveys.tutorial.des_ref`` and ``euclid_ref`` do that.

Legacy Survey brick regions do not overlap, so a position is in one brick
per release. Where both releases cover it, a query through ``GuardedButler``
returns both; a bare ``Butler``, or ``find_first=True``, keeps only the first
collection's match for each data ID:

.. code-block:: python

   lrefs = butler.query_datasets(
       "legacysurvey_brick_coadd",
       where="tract.region OVERLAPS POINT(ra, dec) AND band = b",
       bind={"ra": 40.125, "dec": -0.5, "b": "z"},
       limit=10,
       explain=False,
   )
   [
       (r.run, r.dataId["tract"]) for r in lrefs
   ]  # DR9 north and DR10 south, same brick

``butler_surveys.tutorial.legacy_ref(butler, ra, dec, band)`` searches both
releases and returns the one covering the position; where both do, it raises
``AmbiguousReleaseError`` and you choose with ``release="north"`` or
``release="south"``.

Cutouts
=======

Read the WCS from the header-only ``sky_projection`` component, then pass a
``bbox`` that is an ``lsst.images.Box`` in the tile's own pixels -- exactly
as for DP2's ``deep_coadd``:

.. code-block:: python

   from lsst.images import Box
   from butler_surveys import tutorial as T

   ref = refs[0]
   wcs = butler.get(
       "des_tile_coadd.sky_projection", dataId=ref.dataId
   ).to_legacy()
   box = T.pixel_box(wcs, ra, dec, arcmin=2.0)  # an lsst.geom.Box2I
   cut = butler.get(
       "des_tile_coadd",
       dataId=ref.dataId,
       parameters={"bbox": Box.from_legacy(box)},
   )

``cut`` is a ``DesTileImage`` (Euclid: ``EuclidTileImage``; Legacy Survey:
``LegacySurveyBrickImage``), an ``lsst.images.MaskedImage`` subclass with:

- ``image`` and ``variance`` in nJy and nJy²; pixels with no data have
  variance 1e30 and the ``NO_DATA`` mask bit;
- ``mask``: DES's own mask as ``BAD``, plus ``NO_DATA``; for Euclid,
  ``NO_DATA``, ``SAT`` and ``BAD`` from Euclid's FLAG bits; for the Legacy
  Survey, ``SAT``, ``BAD``, ``SUSPECT`` and ``BRIGHT_OBJECT`` from NERSC's
  ``maskbits``, plus ``NO_DATA``;
- ``sky_projection``, ``psf`` and ``band``; ``tile`` for DES and Euclid,
  ``brick`` and ``release`` (``"DR9 north"`` or ``"DR10 south"``) for the
  Legacy Survey.

Legacy Survey pixels are NERSC's nanomaggies × 3631. A Legacy Survey
``bbox`` must lie inside the brick: one past the edge is refused rather than
read short. ``butler_surveys.tutorial.legacy_cutout`` clips the box to the
brick for you.

.. note::

   Read cutouts, not whole tiles. A DES tile-band is 10000 × 10000 pixels; a
   Euclid tile is 19200 × 19200 and takes about 9 GB to read, a large part
   of an RSP session's memory. A Legacy Survey brick is 3600 × 3600.

Running LSST Tasks
==================

LSST Tasks take afw objects. Convert at the boundary with ``.to_legacy()``,
as Rubin does for ``CellCoadd``:

.. code-block:: python

   exp = cut.to_legacy()  # afw ExposureF: WCS, FilterLabel, PhotoCalib, mask, PSF

The ``ExposureF`` has a ``PhotoCalib`` of 1 (its pixels are nJy), the mask
planes above under afw's names, and the PSF where there is one. Asking the Butler for
``storageClass="ExposureF"`` does **not** work for these dataset types; use
``.to_legacy()``. Tasks run in-process (``Task.run()``); ``pipetask`` does not
read these dataset types.

PSFs
====

- **DES:** DES DR2 publishes no per-tile PSF model. The PSF served with
  ``des_tile_coadd`` was **computed for this Rubin-USDF deployment, not by DES**: PSFEx fitted
  to each tile-band's own stars, and kept only where it passed checks
  against DES's own stars (size, shape, and PSF photometry against DES's
  ``WAVG_MAG_PSF``). 97.5% of tile-bands have one: 95.8% from a first pass
  and 1.7% from a second pass, with stricter star selection, over the
  tile-bands the first failed. ``metadata["PSF_VERSION"]`` says which
  (``v1`` or ``v1-redo-strict``); in the ``ExposureF``'s metadata it is
  tagged ``PSF_TIER`` 5, with a ``PSF_TIER_DESC`` naming the pass. Elsewhere
  ``psf`` is ``None``; for
  detection there, ``T.des_detection_sigma(band)`` gives a smoothing width
  from DES DR2's published seeing.
- **Euclid:** Euclid's own MER PSF grid, one stamp per 12″ cell, served as an
  ``lsst.images`` cell PSF (an afw ``StitchedPsf`` after ``.to_legacy()``).
  It changes in steps from cell to cell. A few cells have no stamp; their
  pixels are served, but evaluating the PSF there raises an error.
- **Legacy Survey:** no PSF. NERSC publishes no coadd PSF model, so ``psf``
  is ``None`` and ``hasPsf()`` is False after ``.to_legacy()``.

Things to know
==============

- **Open with every survey's collections you will use.** A Butler opened on
  one survey's collections takes that survey's skymap as a default data ID,
  and a bare ``Butler`` then returns **no rows, without an error**, for the
  other survey -- even when you name its collection. ``GuardedButler`` handles
  a ``collections=`` passed in a call, but not ``query_data_ids`` or
  ``query_dimension_records``. If one survey comes back empty, check
  ``butler.registry.defaults.dataId``.
- **One Legacy Survey brick and band can be in both releases.** With both
  RUNs in your collections, ``GuardedButler`` refuses a ``get`` (or
  ``getURI``, ``find_dataset``) by data ID that matches in both, with
  ``AmbiguousReleaseError`` naming the RUNs; a bare ``Butler`` silently
  returns the first. Name one release's collection, or pass the
  ``DatasetRef`` from a query. Queries are not refused and return every
  release through ``GuardedButler``; a bare ``Butler``'s query keeps only
  the first collection's match per data ID.
- **Use** ``GuardedButler``, **not bare** ``Butler``: with a bare ``Butler``
  the two traps above give wrong or empty answers with no error.
- **A query hit does not guarantee the bytes.** The files are read in place;
  if a ``get()`` fails, check ``butler.stored(ref)`` before suspecting the
  query.
- ``query_datasets`` **raises** ``EmptyQueryResultError`` on an empty result;
  pass ``explain=False`` to get an empty list.
- **Different filter systems.** LSSTCam, DECam, BASS/MzLS and Euclid bands
  differ: compare structure and positions across surveys, not fluxes.
  Legacy Survey south and DES are both DECam, and inside DES the Legacy
  Survey reuses many DES exposures, so agreement between the two there is
  not an independent check.
- **Legacy Survey** ``BRIGHT_OBJECT`` marks pixels near a bright star, a
  large galaxy or a globular cluster, not bad pixels: around a large galaxy
  it is set on every pixel.
- **Euclid flags:** only no-data, saturation and invalid pixels become mask
  planes. Euclid's other FLAG bits are an OR over all the inputs of a median
  coadd and mostly do not mark bad mosaic pixels; they are available, as
  published, in ``euclid_tile_flag``.
- **Euclid coverage:** 12 of Euclid Q1's 1,402 MER tile-bands are not in
  ``euclid_tile_coadd``, because one of their files is incomplete on the
  USDF copy.

For your agent
==============

If you use Claude Code, the shared folder includes an agent skill,
``survey-butler``, that tells your agent how to use this repository: open it
read-only through ``GuardedButler``, keep queries bounded, read cutouts
rather than whole tiles, avoid the traps above, and report which survey,
release and PSF its results came from. Install it once:

.. code-block:: bash

   cd /sdf/data/rubin/cosmicdata/cosmic_butler/code && python -m butler_surveys.install_skill

That writes one file, ``~/.claude/skills/survey-butler/SKILL.md``; re-run it
after the shared folder is refreshed. The skill does not include the
repository's location: point your agent at the shared folder's
``code/des_dr2_config`` as above.

Tutorial
========

A step-by-step notebook, ``butler_tutorial.ipynb``, is in the shared folder's ``doc/``:
DP2, DES DR2, Euclid Q1 and the Legacy Survey side by side -- coverage,
cutouts, ``ExposureF``\ s, ``SourceDetectionTask``, several surveys on one
pixel grid, colour images from Euclid and from Legacy Survey DR10 south, and
the two Legacy Survey releases side by side.
Copy it to your home before running it:

.. code-block:: bash

   cp /sdf/data/rubin/cosmicdata/cosmic_butler/doc/butler_tutorial.ipynb ~/

Acknowledging the data
======================

If you publish results that use these data, acknowledge and cite each survey
you used, as its team asks (checked 2026-11-10; follow the linked pages if
they have changed):

- **DES DR2:** the acknowledgement on the DES `Data Access
  <https://www.darkenergysurvey.org/the-des-project/data-access/>`__ page
  ("This project used public archival data from the Dark Energy Survey
  (DES). ..."), and cite the DR2 paper, `Abbott et al. 2021, ApJS 255, 20
  <https://doi.org/10.3847/1538-4365/ac00b3>`__, with the pipeline and camera
  papers listed on that page where relevant. _Note that the DES PSFs served here are
  not a DES product._
- **Euclid Q1:** ESA's `Q1 credits <https://www.cosmos.esa.int/web/euclid/q1-data-credits>`__
  page requires the statement "This work has made use of the Euclid Q1 data
  from the Euclid mission of the European Space Agency (ESA), 2025,
  https://doi.org/10.57780/esa-2853f3b", with that DOI also cited in the
  text, and asks you to cite the Q1 papers for the products you used, starting
  with the data release overview, `Euclid Collaboration: Aussel et al. 2025
  <https://doi.org/10.1051/0004-6361/202554610>`__. Q1 data are licensed
  CC BY-NC 3.0 IGO.
- **DESI Legacy Survey (DR9 north, DR10 south):** the acknowledgement on the
  DESI Legacy Surveys' `acknowledgment <https://www.legacysurvey.org/acknowledgment/>`__
  page (a shorter version is offered there for papers that already carry the
  DESI acknowledgements), and cite `Dey et al. 2019, AJ 157, 168
  <https://doi.org/10.3847/1538-3881/ab089d>`__.

Getting help
============

Ask in ``#usdf-support`` on the Rubin Observatory Slack, and say that your
question is about the non-Rubin survey Butler repository. The repository is
maintained by Ana Ennis.
