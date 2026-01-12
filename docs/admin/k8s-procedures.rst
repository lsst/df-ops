#####################
Kubernetes Procedures
#####################

Intended audience: Anyone who is administering application infrastructure at the USDF.

Use Persistent Volume with Weka
===============================
To use persistent volumes set the storage class to use Weka.  Below is what should be added to the kubernetes manifest.

.. rst-class:: technote-wide-content

.. code-block:: yaml

   storageClass: wekafs--sdf-k8s01

Increase Persistent Volume Storage
==================================
There is a limitation with vClusters that persistent volumes cannot be increased.  To increase persistent volumes perform the following.

#. Request increase by :ref:`opening a Service Now Ticket <create_snow_request>`.
#. Update application manifest for updated size.

Make Service Accessible Outside of Kubernetes to S3DF
=====================================================
Kubernetes IP addresses are not accessible from outside Kubernetes.  To make a service accessible from outside of Kubernetes configure the Kubernetes Service to use ``LoadBalancer`` and add an annotation for ``sdf-rubin-ingest``.  Below is how to configure the service.  Note that ``allocateLoadBalancerNodePorts: false`` has to be set since the default is ``true``.

.. rst-class:: technote-wide-content

.. code-block:: yaml

    metadata:
        annotations:
          metallb.io/address-pool: sdf-rubin-ingest
    spec:
        allocateLoadBalancerNodePorts: false
        type: LoadBalancer

Once the IP address is provisioned update the Kubernetes manifest include the IP address allocated with the configuration below.  Replace the ``xxx.xxx.xxx.xxx`` with the IP address.  Setting this is required to request the same IP address.  Note this setting does not reserve an IP address when a service is deleted and another service could use the IP Address.

.. rst-class:: technote-wide-content

.. code-block:: yaml

    metadata:
        annotations:
          metallb.io/loadBalancerIPs: xxx.xxx.xxx.xxx

Make Service Accessible from Outside S3DF
=========================================

Services need approval before being configured as accessible from the USDF.  :ref:`Open a Service Now Ticket <create_snow_request>` to request a DMZ Services Cyber Exemption Request.  Once approved below is the configuration to add.

.. rst-class:: technote-wide-content

.. code-block:: yaml

    metadata:
        annotations:
          metallb.io/address-pool: sdf-dmz
    spec:
        allocateLoadBalancerNodePorts: false
        type: LoadBalancer

Once the IP address is provisioned update the Kubernetes manifest include the IP address allocated with the configuration below.  Replace the ``xxx.xxx.xxx.xxx`` with the IP address.  Note this setting does not reserve an IP address when a service is deleted and another service could use the IP Address.

.. rst-class:: technote-wide-content

.. code-block:: yaml

    metadata:
        annotations:
          metallb.io/loadBalancerIPs: xxx.xxx.xxx.xxx

Route Application Traffic to the Summit
=======================================

Socat proxies are used to move traffic to use the Long Haul Network (LHN) to connect to the Summit.  The S3DF team sets this up.  :ref:`Open a Service Now Ticket <create_snow_request>` to request setup of Socat.  Include the DNS names of what needs to be connected to at the Summit.

Configuring Ingress
===================

When configuring ingress configure the ``host`` the same name as the vCluster DNS name.  Set ingressClassName to ``nginx``.  Use Gafaelfawr Ingress for authenticated access.

Setting Proxy server
====================
For outbound access a proxy server needs to be set.  Add the below environment values to configure a proxy server.  Note the no proxy values should also be set so that internal traffic is not proxied.

.. rst-class:: technote-wide-content

.. code-block:: yaml

    - name: HTTP_PROXY
        value: http://sdfproxy.sdf.slac.stanford.edu:3128
    - name: HTTPS_PROXY
        value: http://sdfproxy.sdf.slac.stanford.edu:3128
    - name: NO_PROXY
        value: localhost,127.0.0.1,::1,10.0.0.0/8,192.168.0.0/16,134.79.0.0/16,172.16.0.0/12,.slac.stanford.edu,.sdf.slac.stanford.edu


Setting Kubernetes Resources and Requests
=========================================

`Setting Resource requests and limits <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>`__ for CPU and Memory is required.  Setting these values helps in both scheduling workloads, preventing a memory leak from affecting other applications on the same node, and oversubscription of nodes.  If ephemeral storage is used a request and limit should also be be set.

The `Kubernetes Workload State dashboard <https://grafana.slac.stanford.edu/d/dd71bcda-7744-4a86-bb10-f3cb65a1255c/kubernetes-workload-state?var-bin=2m&orgId=1&from=now-12h&to=now&timezone=America%2FLos_Angeles&var-node=$__all&var-namespace=$__all&var-topk=10&var-filter_by_pod=&var-filter_by_container=.%2A>`__ in Grafana in the k8s folder provides information on resource usage.  Select the vCluster in the namespace filter and the pod or container to see resource history over time.

Once the resources are determine set the values in the Kubernetes manifest.  This `link details <https://phalanx.lsst.io/developers/resource-limits.html>`__ how to set the values in Phalanx.

Setup Gafealfawr
================
`Gafealfawr <https://gafaelfawr.lsst.io/>`__ is used for authentication and authorization with web applications.  S3DF sets up Gafaelfawr instances in each vCluster if needed.  Below are the steps to setup Gafaelfawr at the USDF.

#. Review `Gafaelfawr scopes <https://gafaelfawr.lsst.io/user-guide/helm.html#scopes>`__.  Validate if existing scopes will work.  If not work with Square team to add scope to Gafaelfawr.
#. Request a Gafaelfawr instance by :ref:`opening a Service Now Ticket <create_snow_request>`.  Include the vCluster name.
