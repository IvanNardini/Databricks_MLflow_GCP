FROM python:3.7.0

LABEL mantainer="Ivan Nardini ivan.nardini@sas.com"

RUN git clone https://github.com/mlflow/mlflow

RUN pip install mlflow

EXPOSE 5000

CMD ["mlflow server --file-store", "mlflow --host 0.0.0.0"]
