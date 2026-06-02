###############
Troubleshooting
###############

Intended audience: Anyone who is administering Prompt Processing.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - Missing data at USDF
     - No prompt processing can be done if raw data did not arrive USDF embargo bucket within the waiting time.
       This is an upstream issue.
     - Prompt Processing workers would time out after waiting a configurable amount of time.
   * - Missing nextVisit events
     - No fanned out nextVisit are received after their publication.
       This is an upstream issue.
     - See :doc:`../next-visit-fan-out/index`.
   * - Missing dataset types in the ``embargo`` butler repo
     - Typically new dataset types are registered in the ``embargo`` repo during the release process.
     - Register manually: https://github.com/lsst-dm/prompt_processing/blob/main/doc/playbook.rst#adding-new-dataset-types
   * - Missing file arrival notifications
     - The bucket is configured to send Kafka notifications when new objects are created.
       It has got disabled for unknown reasons in the past.
       Prompt Processing relies on these notifications together with the raw presence microservice
       to know that a raw file is available.
       This is a storage issue.
     - If this is confirmed not to be a wider embargo storage issue and no other storage issues
       are present, one can try to reconfigure the bucket notifications.
   * - Images rejected as unprocessable
     - Sometimes the nextVisit and the actual exposure are too inconsistent, or necessary exposure
       metadata is missing; these exposures are unprocessable.
       This is an upstream issue.
     - Prompt Processing raises RuntimeError and skips the image.
   * - Incompatible stack versions between auto-ingest and prompt service.
     - It could cause problems for Prompt Processing to write data to the embargo repo.
     - Auto-ingest may need to update the stack version.
   * - Prompt service software bugs
     - Major stack regression, middleware interface or activator bugs that are not discovered
       during testing and release process.
     - Rollback to the previously working version and report to the Prompt Processing team.
   * - PipelineExecutionError
     - Errors from pipeline payload execution, but the framework is correctly executing.
     - Non-urgent but report to the Pipelines team

Monitoring
==========
.. Describe how to monitor application and include relevant links.

`Prompt Processing Production Overview <https://grafana.slac.stanford.edu/d/feifuf82d6tj4f/prompt-processing-production-overview?orgId=1&from=now-6h&to=now&timezone=browser&var-instrument=lsstcam&var-alertstream=lsst-alerts-.%2B>`__

`Prompt Processing Production output <https://grafana.slac.stanford.edu/d/nk1zxv84z/prompt-processing-production-output?orgId=1&from=now-6h&to=now&timezone=browser&var-instrument=lsstcam&var-pod=$__all&var-level=$__all>`__

`Prompt Processing Production I/O timing <https://grafana.slac.stanford.edu/d/eeimq740rdgjkf/prompt-processing-production-i-o-timing?orgId=1&from=now-6h&to=now&timezone=browser&var-instrument=lsstcam>`__

`Prompt Processing Production statistics <https://grafana.slac.stanford.edu/d/c0a9c6d3-4ea8-452d-bb91-962304c1b0d2/prompt-processing-production-statistics?orgId=1&from=now-7d&to=now&timezone=browser&var-instrument=lsstcam&var-interval=1h>`__


Sample Troubleshooting
======================
.. Template to use for troubleshooting

**Symptoms:**

**Cause:**

**Solution:**
