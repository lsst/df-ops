##########
Procedures
##########

Intended audience: Anyone who is administering weatherbroadcaster.

Deployment
==========

Deployment is managed with Phalanx and Argo CD from the
``applications/weatherbroadcaster`` Phalanx application.
The container image is ``ghcr.io/lsst-ts/weatherbroadcaster``.

The application is enabled for the ``usdfdev`` Phalanx environment.

Maintenance
===========

Check the Phalanx application values and Argo CD application state before and after maintenance.
The update job schedule is configured by the ``updateWeather.schedule`` Helm value.

Backup
======

No separate backup is required for the weather cache.
The cache is generated from EFD data by the update job.

Cold Startup
============

Sync the Phalanx application with Argo CD and verify that the web deployment and ``weatherbroadcaster-update-weather`` CronJob are healthy.
After the update job runs, verify that ``GET /weatherbroadcaster/data`` returns weather data.

Cold Shutdown
=============

No special shutdown procedure is required.
Stop or disable the Phalanx application if the service must be taken out of service.

Reproduce Service
=================

The application repository includes local Kubernetes manifests under ``k8s/`` for manual testing.
The cache can be refreshed by running:

.. code-block:: bash

   python -m weatherbroadcaster.update_weather
