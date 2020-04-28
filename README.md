# Databricks, Mlflow and GCP: How to deploy a Mleap flavor Model to GPC

Databricks, Mlflow and GCP: How to deploy a Mleap flavor Model to GPC is a simple exercise.
Its goal is to put together what I learned from Coursera's End-to-End Machine Learning with TensorFlow
on GCP course and Databricks' Academy MLFlow: Managing the Machine Learning Lifecycle course.

It is about:

1. **Train a model and track experiments with Managed MLflow in Databricks' platform**
2. **Export Mleap flavor format of Champion Model**
3. **Engineer the score code in a way that it can be deploy in a batch job on GCP Dataproc cluster**

Below the **high-level architecture of the project**: 

<img src="https://github.com/IvanNardini/Databricks_MLflow_GCP/raw/master/architecture.png">

And some **content of the demo**:

<img src="https://github.com/IvanNardini/Databricks_MLflow_GCP/raw/master/demo.gif">

## Setup

**Setup on Databricks' Community edition**

You have to create a cluster and install MLflow and MLeap on the cluster

1. *Create a cluster specifying*:

    - Databricks Runtime Version: Databricks Runtime 5.0 or above
    - Python Version: Python 3

2. *Install required libraries*: 

    - Create library with Source Maven Coordinate and the fully-qualified Maven artifact coordinate: ml.combust.mleap:mleap-spark_2.11:0.13.0
    - Install the libraries into the cluster.

3. *Install required Python library*

    - Create required library: Source PyPI and enter mlflow[extras].
    - Install the libraries into the cluster.

4. *Attach this notebook to the cluster*.

Notice: You can install mlflow and mleap libraries from notebook as well. 
Below the commands

- dbutils.library.installPyPI("mlflow", "1.7.0", extras="extras")
- dbutils.library.installPyPI("mleap", "0.15.0", extras="extras")
- dbutils.library.restartPython()

**Setup on GCP**

I've tried to make it as simple as possible.

Look at usage section below.

## Usage (Work in progress...)

On GCP Cloud Shell, clone the repo.

```
git clone https://github.com/IvanNardini/Databricks_MLflow_GCP.git
```
Then make .sh in 0_setup folder executable

```
chmod +x 1_setup_bucket.sh 2_setup_cluster.sh 3_submit_score_job.sh
```
Then run to create the bucket and the cluster run

```
./1_setup_bucket.sh 
./2_setup_cluster.sh
```
Finally you can run 

```
3_submit_score_job.sh
```
to submit the spark score job. Or you can use the GUI.

## Contributing

Test it. And please provide me feedback for improvements. Pull requests are welcome as well.

And feel free to reach me at [Ivan Nardini](ivan.nardini@sas.com )