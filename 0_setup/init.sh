#!/bin/bash

# Install Dependencies
spark-shell --packages ml.combust.mleap:mleap-spark_2.11:0.15.0

#Download Model
wget https://github.com/IvanNardini/Databricks_MLflow_GCP/blob/master/2_notebooks/output/ModelProjects_Boston_ML_lrModel.zip -P /tmp



