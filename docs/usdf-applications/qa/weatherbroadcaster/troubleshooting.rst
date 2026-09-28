###############
Troubleshooting
###############

Intended audience: Anyone who is administering weatherbroadcaster.

Known Issues
============

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - Cache has not been created
     - ``GET /weatherbroadcaster/data`` returns ``503 Service Unavailable``.
     - Verify that the ``weatherbroadcaster-update-weather`` CronJob has run successfully.
   * - Missing EFD values
     - Some fields may be returned as ``-999`` when recent EFD data is unavailable.
     - Check the relevant ESS EFD topics and the update job logs.

Monitoring
==========

Monitor the Kubernetes deployment, service, ingress, and ``weatherbroadcaster-update-weather`` CronJob in the Phalanx environment.
Check the application logs for EFD query failures, cache write failures, and unexpected FastAPI errors.

Cache Missing
=============

**Symptoms:**
``GET /weatherbroadcaster/data`` returns ``503 Service Unavailable`` with ``Weather data has not been cached yet.``.

**Cause:**
The cache file does not exist at the configured ``WEATHERBROADCASTER_WEATHER_DATA_FILE_PATH``.

**Solution:**
Check the update CronJob status and logs.
Rerun the update job or wait for the next scheduled run, then verify that the endpoint returns data.
