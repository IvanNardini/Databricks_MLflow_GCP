# Track the Basic Multivariate Linear Regression using Mlleap flavor

with mlflow.start_run(run_name='Basic Multivariate Linear Regression') as run:
  
  #Define variables
  params = {'featuresCol' : 'features', 'labelCol' : 'medv', 'maxIter' : 10}

  # Create Model Instance
  lr = LinearRegression(**params)

  # Fit Model and Predict
  lrModel = lr.fit(abt_train)
  predictions = lrModel.transform(abt_test)

  # Log params and metrics using the MLflow APIs
  mlflow.log_params(params)
  mlflow.log_metric("rmse", rmse)
  mlflow.log_metric("mse", mse)
  mlflow.log_metric("r2", r2)
  mlflow.log_metric("mae", mae)
  
  #Log artefacts (Scored Test data & Coefficients Summary)
  
  ## Scored Test data
  temp1 = tempfile.NamedTemporaryFile(prefix='scored_df_', suffix='.csv')
  temp1_name = temp1.name
  try: 
    scored_df = predictions.drop('features').toPandas()
    scored_df.to_csv(temp1_name, index=False)
    mlflow.log_artifact(temp1_name)
  except SystemError:
    print('Check the log!')
  finally:
    temp1.close()
    
  ## Coefficients Summary
  temp2 = tempfile.NamedTemporaryFile(prefix='Coefficients_summary_', suffix='.csv')
  temp2_name = temp2.name
  try: 
    summary = pd.DataFrame(features, columns=['features'])
    summary['betacoeff'] = np.array(lrModel.coefficients)
    summary['pvalues'] = [round(pval, 4) for (col, pval) in zip(features, lrModel.summary.pValues[1:])]
    summary.sort_values(by='pvalues', inplace=True)
    summary.to_csv(temp2_name, index=False)
    mlflow.log_artifact(temp2_name)
  except SystemError:
    print('Check the log!')
  finally:
    temp2.close()
    
  # Log residuals using a temporary file
  temp3 = tempfile.NamedTemporaryFile(prefix="residuals-", suffix=".png")
  temp3_name = temp3.name
  
  try:
    ## Create Residual plots
    fig, ax = plt.subplots()
    sns.residplot('prediction', 'medv', data=scored_df)
    plt.xlabel("Predicted values for medv")
    plt.ylabel("Residual")
    plt.title("Residual Plot")
    fig.savefig(temp3_name)
    mlflow.log_artifact(temp3_name, "residuals.png")
    
  finally:
    temp3.close() # Delete the temp file

  # Log the model both in python and in spark and mleap flavors
  mlflow.spark.log_model(spark_model=lrModel, 
                         artifact_path="pyspark-multi-linear-model", 
                         sample_input=abt_test)
  
  runID = run.info.run_uuid
  experimentID = run.info.experiment_id
  
  print("Inside MLflow Run with run_id {} and experiment_id {}".format(runID, experimentID))