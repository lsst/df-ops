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

  #. Request increase by opening Service Now Ticket.
  #. Update application manifest for updated size.

Make Service Accessible Outside of Kubernetes to S3DF
=====================================================

Kubernetes IP addresses are not accessible from outside Kubernetes.  To make a service accessible from outside of Kubernetes configure the Kubernetes Service to use ``LoadBalancer`` and add an annotation for ``sdf-rubin-ingest``.  Below is an example of what to add to a service.

.. rst-class:: technote-wide-content

.. code-block:: yaml

    metadata:
        annotations:
        metallb.universe.tf/address-pool: sdf-rubin-ingest
    spec:
        allocateLoadBalancerNodePorts: true
        type: LoadBalancer

To reserve a specific IP address after provisioned add the below with the appropriate IP address.

.. rst-class:: technote-wide-content

.. code-block:: yaml

    spec:
      loadBalancerIP: <IP address>

Make Service Accessible from Outside S3DF
=========================================

Set Application Traffic to use LHN
==================================

Configuring Ingress
===================

Setting Proxy server
====================

For outbound access a proxy server needs to be set.  Add the below environment values to configure a proxy server.  Note the no proxy values should also be set so that internal traffic is not proxied.

.. rst-class:: technote-wide-content

.. code-block:: yaml

    - name: "HTTP_PROXY"
    value: "http://squid.slac.stanford.edu:3128"
    - name: "HTTPS_PROXY"
    value: "http://squid.slac.stanford.edu:3128"
    - name: "NO_PROXY"
    value: "127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,.cluster.local,argocd-repo-server,.stanford.edu,.slac.stanford.edu,.sdf.slac.stanford.edu"


Setting Kubernetes Resources and Requests
=========================================
