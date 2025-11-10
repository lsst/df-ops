###############
Troubleshooting
###############

Intended audience: Anyone who is administering Rucio.

Known Issues
============
.. Discuss known issues with the application.

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - Issue
     - Description
     - Workaround
   * - Slow processing of rules and requests
     - Rubin transfers a lot of small files, which if a single rule defines replicas for the many files, i.e. >1 Million files, this could cause some Rucio daemons to hang up, such as ``conveyor-finisher``.
     - Do not use a container/dataset with many files. Reduce each dataset to ~500 files and create rules per dataset.

Monitoring
==========
.. Describe how to monitor application and include relevant links.

* Rucio Overview: https://grafana.slac.stanford.edu/d/000000003/rubin-rucio-overview
* Rucio Transfer Monitoring: https://grafana.slac.stanford.edu/d/YVcucApIk/rucio-transfer-monitoring

.. Template to use for troubleshooting

Sample Troubleshooting
======================

**Symptoms:**

**Cause:**

**Solution:**
