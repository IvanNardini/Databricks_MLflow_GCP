#!/bin/bash

# setup_cluster.sh
# Create a plain vanilla cluster if doesn't exist with config.
# REGION  - Region name (default eu)
# BUCKET - Bucker name (default cloud-demo-databrick-gcp)


#Pass all parameters (or use default parameters)
CLUSTER_NAME=${1:-cluster-00000}
BUCKET=${2:-cloud-demo-databrick-gcp}
REGION=${3:-europe-west6}
ZONE=${4:-europe-west6-a}
PROJECT=${5:-sandbox}

# Setup cluster
gcloud beta dataproc clusters create ${CLUSTER_NAME} \
--enable-component-gateway \
--bucket ${BUCKET} \
--region ${REGION} \
--subnet default \
--zone ${ZONE} \
--master-machine-type n1-standard-4 \
--master-boot-disk-size 500 \
--num-workers 2 \
--worker-machine-type n1-standard-4 \
--worker-boot-disk-size 500 \
--image-version 1.3-deb9 \
--properties spark:spark.jars.packages=ml.combust.mleap:mleap-spark_2.11:0.15.0 \
--optional-components ANACONDA,JUPYTER \
--scopes 'https://www.googleapis.com/auth/cloud-platform' \
--project ${PROJECT} \
--initialization-actions 'gs://goog-dataproc-initialization-actions-europe-west6/conda/bootstrap-conda.sh','gs://goog-dataproc-initialization-actions-europe-west6/conda/install-conda-env.sh',"gs://${BUCKET}/0_setup/cluster_config/init.sh" \
--metadata 'MINICONDA_VARIANT=3','MINICONDA_VERSION=latest','PIP_PACKAGES=mleap==0.15.0 pyspark==2.4.5 gcsfs==0.6.1'