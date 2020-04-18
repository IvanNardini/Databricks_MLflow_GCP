#!/bin/bash

# setup_cluster.sh
# Create a plain vanilla cluster if doesn't exist with config.
# REGION  - Region name (default eu)
# BUCKET - Bucker name (default cloud-demo-databrick-gcp)


#Pass REGION and BUCKET names (or use default parameters)
CLUSTER_NAME=${1:-cluster-0000}
BUCKET=${2:-cloud-demo-databrick-gcp}
REGION=${3:-europe-west6}
ZONE=${4:-europe-west6-a}

# Setup cluster
gcloud beta dataproc clusters create ${CLUSTER_NAME} \
--bucket ${BUCKET} \
--region ${REGION} \
--subnet default \
--no-address \
--zone ${ZONE} \
--master-machine-type n1-standard-4 \
--master-boot-disk-size 500 \
--num-workers 2 \
--worker-machine-type n1-standard-4 \
--worker-boot-disk-size 500 \
--image-version 1.3-deb9 \
--optional-components ANACONDA,JUPYTER \
--scopes 'https://www.googleapis.com/auth/cloud-platform' \
--project gel-sassandbox \
--initialization-actions 'gs://cloud-demo-databrick-gcp/0_init/init.sh'
