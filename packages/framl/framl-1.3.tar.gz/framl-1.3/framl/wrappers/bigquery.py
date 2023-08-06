from google.cloud import bigquery


class BigQuery:
    FIELDS_MAPPING = {
        "integer":   "INTEGER",
        "float":     "FLOAT",
        "boolean":   "BOOLEAN",
        "string":    "STRING",
        "timestamp": "TIMESTAMP"
    }

    PROJECT_ID = "bbc-data-science"
    DATASET_NAME = "framl"

    @staticmethod
    def merge_schemas(current_schema: list, wanted_schema: dict) -> list:
        final_schema = current_schema[:]
        for field_name, params in wanted_schema.items():
            if "monitored" not in params or params.get("monitored") is not True:
                continue

            for c_filed in current_schema:
                if c_filed.name == field_name:
                    break
            else:
                final_schema.append(bigquery.SchemaField(field_name, BigQuery.FIELDS_MAPPING[params["data_type"]]))

        return final_schema

    @staticmethod
    def get_table_schema(table_name: str) -> list:
        client = bigquery.Client(project=BigQuery.PROJECT_ID)
        table_ref = client.dataset(BigQuery.DATASET_NAME).table(table_name)
        try:
            table = client.get_table(table_ref)
            return table.schema[:]
        except:
            return None

    @staticmethod
    def update_table(table_name, schema: list) -> None:
        client = bigquery.Client(project=BigQuery.PROJECT_ID)
        table_ref = client.dataset(BigQuery.DATASET_NAME).table(table_name)
        table = client.get_table(table_ref)
        table.schema = schema
        table = client.update_table(table, ["schema"])
        print(f"Updated table {table.project}.{table.dataset_id}.{table.table_id}")

    @staticmethod
    def create_table(table_name: str, schema: list) -> None:
        table_id = f"{BigQuery.PROJECT_ID}.{BigQuery.DATASET_NAME}.{table_name}"
        client = bigquery.Client(project=BigQuery.PROJECT_ID)
        table = bigquery.Table(table_id, schema=schema)
        table.time_partitioning = bigquery.table.TimePartitioning(field="prediction_time")
        table = client.create_table(table)
        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")
