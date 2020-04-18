#!/bin/bash

#Pass REGION and BUCKET name

#Create a BUCKET if not exist
if ! gsutil ls | grep -q gs://${BUCKET}/; then
  gsutil mb -l ${REGION} gs://${BUCKET}
  #upload cluster_init.sh, boston_house_prices_toscore.csv and Boston_lrModel_mleap.zip, score.py
  gsutil cp /home/ivan_nardini/Databricks_MLflow_GCP/0_setup/setup_cluster.sh gs://${BUCKET}/0_init/init.sh
  gsutil cp /home/ivan_nardini/Databricks_MLflow_GCP/1_data/boston_house_prices.csv gs://${BUCKET}/1_data/boston_house_prices_toscore.csv
  gsutil cp /home/ivan_nardini/Databricks_MLflow_GCP/2_notebooks/output/ModelProjects_Boston_ML_lrModel.zip gs://${BUCKET}/2_model/Boston_lrModel_mleap.zip
  gsutil cp /home/ivan_nardini/Databricks_MLflow_GCP/2_notebooks/output/score.py gs://${BUCKET}/2_model/score.py
fi

#Check BUCKET content
gsutil ls -r gs://${BUCKET}/**
