import os
import json
import logging
from datetime import datetime, timedelta, timezone

import boto3
import pyarrow as pa
import pyarrow.parquet as pq

from parse_data import parse_data


def lambda_handler(event: dict, context: dict) -> bool:
    """
    AWS Lambda function responsible for:
    - Reading raw Telegram JSON files from S3 (RAW layer)
    - Parsing relevant fields
    - Converting data to Parquet format
    - Storing optimized files in S3 (ENRICHED layer)
    """

    RAW_BUCKET = os.environ["AWS_S3_BUCKET"]
    ENRICHED_BUCKET = os.environ["AWS_S3_ENRICHED"]

    tzinfo = timezone(offset=timedelta(hours=-3))
    target_date = (datetime.now(tzinfo) - timedelta(days=1)).strftime("%Y-%m-%d")
    timestamp = datetime.now(tzinfo).strftime("%Y%m%d%H%M%S%f")

    s3_client = boto3.client("s3")
    table = None

    try:
        response = s3_client.list_objects_v2(
            Bucket=RAW_BUCKET,
            Prefix=f"telegram/context_date={target_date}"
        )

        for content in response.get("Contents", []):
            key = content["Key"]
            local_file = f"/tmp/{key.split('/')[-1]}"

            s3_client.download_file(RAW_BUCKET, key, local_file)

            with open(local_file, mode="r", encoding="utf-8") as file:
                data = json.load(file)["message"]

            parsed = parse_data(data)
            new_table = pa.Table.from_pydict(parsed)

            table = pa.concat_tables([table, new_table]) if table else new_table

        if table:
            output_file = f"/tmp/{timestamp}.parquet"

            pq.write_table(table, output_file)

            s3_client.upload_file(
                output_file,
                ENRICHED_BUCKET,
                f"telegram/context_date={target_date}/{timestamp}.parquet"
            )

        return True

    except Exception as error:
        logging.error(f"ETL error: {error}")
        return False
