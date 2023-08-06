from typing import Union, List
from framl.config_model import ConfigModel
from framl.wrappers.bigquery import BigQuery
from framl.wrappers.pubsub import Pubsub
from google.cloud import bigquery


class Monitoring:

    def __init__(self, app_path: str):
        model_conf_ob = ConfigModel(app_path)
        self._model_params = model_conf_ob.get_input_and_output_params()

        self._model_name = model_conf_ob.get_model_name()
        self._project_id = model_conf_ob.get_gcp_project_id()
        self._table_name = self._model_name.replace("-", "_")

    def prepare_table(self) -> None:

        table_name = self._table_name
        current_schema = BigQuery.get_table_schema(table_name)

        if current_schema is None:
            current_schema = [
                bigquery.SchemaField("prediction_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("prediction_time", "TIMESTAMP", mode="REQUIRED"),
            ]
            schema = BigQuery.merge_schemas(current_schema, self._model_params)
            BigQuery.create_table(table_name, schema)

        else:
            schema = BigQuery.merge_schemas(current_schema, self._model_params)
            if len(schema) <= len(current_schema):
                raise Exception(f"No schema modification for table {table_name}")
            BigQuery.update_table(table_name, schema)

    def list(self) -> dict:
        return {
            "topic": f"projects/{Pubsub.PROJECT_ID}/topics/{Pubsub.TOPIC_NAME}",
            "bucket" : "gs://framl-model-monitoring",
            "table": f"{BigQuery.PROJECT_ID}:{BigQuery.DATASET_NAME}.{self._table_name}"
        }
