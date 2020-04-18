#!/bin/bash

#Pass CLUSTER NAME and PROJECT


# Setup cluster

gcloud beta dataproc clusters create cluster-24d3 \
--bucket cloud-demo-databrick-gcp \
--region us-central1 \
--subnet default \
--no-address \
--zone us-central1-b \
--master-machine-type n1-standard-4 \
--master-boot-disk-size 500 \
--num-workers 2 \
--worker-machine-type n1-standard-4 \
--worker-boot-disk-size 500 \
--image-version 1.3-deb9 \
--project gel-sassandbox \
--initialization-actions 'gs://cloud-demo-databrick-gcp/0_init/init.sh','gs://cloud-demo-databrick-gcp/0_init/pip-install.sh' \
--metadata PIP_PACKAGES=mleap==0.15.0 pyspark==2.4.5
