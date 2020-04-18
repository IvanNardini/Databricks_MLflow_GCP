gcloud dataproc jobs submit pyspark pyspark_sa.py \
--cluster=${PROJECT_ID} \
-- gs://${PROJECT_ID}/pyspark_nlp/data/ gs://${PROJECT_ID}/pyspark_nlp/result gs://${PROJECT_ID}/pyspark_nlp/model