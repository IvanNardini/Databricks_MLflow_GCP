#!/bin/bash

# init.sh
# Install spark dependencies. Install mleap pyspark. Download Model.zip

# Install Dependencies
spark-shell --packages ml.combust.mleap:mleap-spark_2.11:0.15.0

# Install python libraries
pip install mleap==0.15.0 pyspark==2.4.5

# Move in the right jars folder (to check)
mv /root/.ivy2/jars/*.jar /usr/lib/spark/jars

# Download Model
curl -X GET https://github.com/IvanNardini/Databricks_MLflow_GCP/raw/master/2_notebooks/output/ModelProjects_Boston_ML_lrModel.zip --output /tmp/model.zip



