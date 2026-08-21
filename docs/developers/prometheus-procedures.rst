#####################
Prometheus Procedures
#####################

Intended audience: Anyone who is developing applications at the USDF.

Integrating metrics with Prometheus
===================================

Prometheus metrics are scraped within USDF Kubernetes vClusters.  Prometheus is a datasource in the S3DF Grafana.  To integrate metrics add the following annotation to your kubernetes manifest so that metrics are scraped.


.. rst-class:: technote-wide-content

.. code-block:: yaml

    podAnnotations:
      prometheus.io/scrape: 'true'
      prometheus.io/port: '8000'

Creating metrics with Prometheus
================================

Prometheus has client libraries for many programming languages including Python.  The Prometheus python library is `here <https://pypi.org/project/prometheus-client/>`__.  When developing metrics here are some considerations:

* Identify what type of metric to create.   An overview of Prometheus metric types is `here <https://prometheus.io/docs/concepts/metric_types/>`
* If you are creating reports with log filters consider creating a metric for better performance
* The Prometheus python client has an implementation of context manager. This makes it easier to handle exceptions and prevents prometheus gauges that are stuck due to an exception