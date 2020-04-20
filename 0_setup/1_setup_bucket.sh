#!/bin/bash

# setup.sh
# Create a bucket if doesn't exist. And load deployment scripts (.sh, .py)
# REGION  - Region name (default eu)
# BUCKET - Bucker name (default cloud-demo-databrick-gcp)


#Pass REGION and BUCKET names (or use default parameters)
REGION=${1:-eu}
BUCKET=${2:-cloud-demo-databrick-gcp}

#Create a BUCKET name if not exist
if ! gsutil ls | grep -q gs://${BUCKET}/; then
  gsutil mb -l ${REGION} -b on gs://${BUCKET} 

  #Upload init.sh, boston_house_prices_toscore.csv and Boston_lrModel_mleap.zip, score.py
  gsutil cp /home/ivan_nardini/Databricks_MLflow_GCP/0_setup/cluster_config/init.sh gs://${BUCKET}/0_setup/cluster_config/init.sh
  gsutil cp /home/ivan_nardini/Databricks_MLflow_GCP/1_data/boston_house_prices.csv gs://${BUCKET}/1_data/boston_house_prices_toscore.csv 
  gsutil cp /home/ivan_nardini/Databricks_MLflow_GCP/2_notebooks/output/ModelProjects_Boston_ML_lrModel.zip gs://${BUCKET}/2_model/Boston_lrModel_mleap.zip
  gsutil cp /home/ivan_nardini/Databricks_MLflow_GCP/2_notebooks/output/score.py gs://${BUCKET}/2_model/score.py
fi

#Check BUCKET content
gsutil ls -r gs://${BUCKET}/**


