#! bin/bash

#Pass CLUSTER_NAME, REGION AND BUCKET parameters (or use default parameters)
CLUSTER_NAME=${1:-cluster-00000}
REGION=${2:-europe-west6}
BUCKET=${3:-cloud-demo-databrick-gcp}

#Run job
gcloud dataproc jobs submit pyspark \ 
--cluster ${CLUSTER_NAME} \
--region ${REGION} \  
gs://${BUCKET}/2_model/score.py --input "gs://cloud-demo-databrick-gcp/1_data/boston_house_prices_toscore.csv" --output "gs://cloud-demo-databrick-gcp/1_data/boston_house_prices_scored.csv"