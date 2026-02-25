CREATE EXTERNAL TABLE IF NOT EXISTS telegram (
  message_id BIGINT,
  user_id BIGINT,
  user_is_bot BOOLEAN,
  user_first_name STRING,
  chat_id BIGINT,
  chat_type STRING,
  text STRING,
  date BIGINT
)
PARTITIONED BY (context_date DATE)
STORED AS PARQUET
LOCATION 's3://<SEU_BUCKET_ENRICHED>/telegram/';
