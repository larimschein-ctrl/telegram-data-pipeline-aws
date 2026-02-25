import os
import json
import logging
from datetime import datetime, timedelta, timezone

import boto3


def lambda_handler(event: dict, context: dict) -> dict:
    """
    AWS Lambda function responsible for:
    - Receiving Telegram webhook events via API Gateway
    - Validating the chat_id
    - Storing raw JSON messages in S3 (RAW layer), partitioned by date
    """

    BUCKET = os.environ["AWS_S3_BUCKET"]
    TELEGRAM_CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

    tzinfo = timezone(offset=timedelta(hours=-3))
    current_date = datetime.now(tzinfo).strftime("%Y-%m-%d")
    timestamp = datetime.now(tzinfo).strftime("%Y%m%d%H%M%S%f")

    filename = f"{timestamp}.json"
    s3_client = boto3.client("s3")

    try:
        body = json.loads(event["body"])
        chat_id = body["message"]["chat"]["id"]

        # Validate chat ID
        if chat_id == TELEGRAM_CHAT_ID:

            # Save temporary file
            with open(f"/tmp/{filename}", mode="w", encoding="utf-8") as file:
                json.dump(body, file)

            # Upload to S3 (RAW layer)
            s3_client.upload_file(
                f"/tmp/{filename}",
                BUCKET,
                f"telegram/context_date={current_date}/{filename}",
            )

    except Exception as error:
        logging.error(f"Ingestion error: {error}")
        return {"statusCode": 500}

    return {"statusCode": 200}
