#!/usr/bin/python

import numpy as np
import pandas as pd
import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType
from pyspark.ml.feature import VectorAssembler
import mleap.pyspark
from mleap.pyspark.spark_support import SimpleSparkSerializer
from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import RegressionEvaluator


import os
import sys
import argparse
import tempfile
import warnings


def read_data_csv(spark, inputPath_CSV):
    
    '''
    Function to load data in the Spark Session 
    :param spark: spark session 
    :param inputPath: path to get the data 
    :return: df
    '''
    
    print('Trying to read the data...')
    
    try:
        schema = StructType([
          StructField('crim',DoubleType(),True),
          StructField('zn',DoubleType(),True),
          StructField('indus',DoubleType(),True),
          StructField('chas',IntegerType(),True),
          StructField('nox',DoubleType(),True),
          StructField('rm',DoubleType(),True),
          StructField('age',DoubleType(),True),
          StructField('dis',DoubleType(),True),
          StructField('rad',IntegerType(),True),
          StructField('tax',IntegerType(),True),
          StructField('ptratio',DoubleType(),True),
          StructField('b',DoubleType(),True),
          StructField('lstat',DoubleType(),True),
          StructField('medv',DoubleType(),True)]
        )
        
        df = (spark.read
          .option("HEADER", True)
          .schema(schema)
          .csv(inputPath_CSV))
    
    except ValueError:
        print('At least, one variable format is wrong! Please check the data')
      
    else:
        print('Data to score have been read successfully!')
        return df

def preprocessing(df):

    '''
    Function to preprocess data 
    :param df: A pyspark DataFrame 
    :return: abt_to_score
    '''
    
    print('Data preprocessing...')

    features = df.schema.names[:-1]
    assembler_features = VectorAssembler(inputCols=features, outputCol="features")
    abt_to_score = assembler_features.transform(df)
    
    print('Data have been processed successfully!')
    return abt_to_score

def score_data(abt_to_score, modelPath):
    
    '''
    Function to score data 
    :param abt_to_score: A pyspark DataFrame to score
    :param modelPath: The modelpath associated to .zip mleap flavor
    :return: scoredData
    '''
    print('Scoring process starts...')
    
    deserializedPipeline = PipelineModel.deserializeFromBundle("jar:file:{}".format(modelPath))
    scoredData = deserializedPipeline.transform(abt_to_score)
    return scoredData  
  
def write_output_csv(scoredData, outputPath_CSV):
    '''
    Function to write predictions
    :param scoredData: A pyspark DataFrame of predictions
    :param outputPath: The path to write the ouput table
    :return: scoredData
    '''
    print('Writing Prediction in {}'.format(outputPath_CSV))
    scoredData.toPandas().to_csv(outputPath_CSV, sep=',', index=False)
    return scoredData.toPandas().to_dict()

def evaluator(predictions):
    
    '''
    Function to produce some evaluation stats
    :param predictions: A pyspark DataFrame of predictions
    :return: rmse, mse, r2, mae
    '''
    evaluator = RegressionEvaluator(predictionCol="prediction", labelCol="medv")
    rmse = evaluator.evaluate(predictions)
    mse = evaluator.evaluate(predictions, {evaluator.metricName: "mse"})
    r2 = evaluator.evaluate(predictions, {evaluator.metricName: "r2"})
    mae = evaluator.evaluate(predictions, {evaluator.metricName: "mae"})
    
    return rmse, mse, r2, mae

def main():
    
    parser = argparse.ArgumentParser(description='Score')
    
    parser.add_argument('--input', dest="inputpath_CSV",
                        required=True, help='Provide the input path of data to score')
    
    #Mleap deserializeFromBundle method does not work with URL on GCP
    
    # parser.add_argument('--model', dest="modelPath",
    #                     required=True, help='Provide the model path to score')
    
    parser.add_argument('--output', dest="outputpath_CSV",
                        required=True, help='Provide the model path to score')

    args = parser.parse_args()
    input_path_CSV = args.inputpath_CSV
    # modelPath = args.modelPath
    modelPath = '/tmp/model.zip'
    output_path_CSV = args.outputpath_CSV
  
    try:
#         spark = SparkSession \
#         .builder \
#         .master(SPARK_MASTER) \
#         .config('spark.executor.memory', TOTAL_MEMORY) \
#         .config('spark.cores.max', TOTAL_CORES) \
#         .config('spark.jars.packages',
#                 'ml.combust.mleap:mleap-spark-base_2.11:0.15.0,ml.combust.mleap:mleap-spark_2.11:0.15.0') \
#         .appName("ClassifierTraining") \
#         .getOrCreate()
        spark = SparkSession.builder.appName('RegressionScoring').getOrCreate()
        spark.sparkContext.setLogLevel("OFF")
        print('Created a SparkSession')
    
    except ValueError:
        warnings.warn('Check')
  
    #Read data
    data_to_process = read_data_csv(spark, input_path_CSV)
    #Preprocessing
    abt = preprocessing(data_to_process)
    #Scoring
    abt_scored = score_data(abt, modelPath)
    #Write data
    write_output_csv(abt_scored, output_path_CSV)
    #Evaluate Model
    evalstats = evaluator(abt_scored)
    return evalstats
    
    
if __name__=="__main__":
    
    stats = main()
    print('-'*20)
    print('Process Log')
    print('-'*20)
    print('Scoring Job ends successfully!')
    print("RMSE for the model: {}".format(stats[0]))
    print("MSE for the model: {}".format(stats[1]))
    print("R2 for the model: {}".format(stats[2]))
    print("MAE for the model: {}".format(stats[3]))
    print('Look at the Storage Bucket to get predictions!')
    
