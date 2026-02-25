# 🚀 Telegram Data Pipeline on AWS

End-to-end serverless data pipeline built on AWS to ingest, transform and analyze Telegram group messages using a layered Data Lake architecture.

---

## 🏗 Architecture Overview

**Flow:**

Telegram  
→ API Gateway  
→ Lambda (Ingestion)  
→ S3 RAW Layer (JSON, partitioned by date)  

EventBridge (Daily Schedule)  
→ Lambda (ETL Transformation)  
→ S3 ENRICHED Layer (Parquet, partitioned)  

Amazon Athena  
→ Analytical Queries (SQL)

---

## 🗂 Data Lake Layers

### 🔹 RAW Layer
- Stores original Telegram JSON payload
- Partitioned by `context_date`
- Immutable raw storage for traceability
- Optimized for durability, not performance

Example structure:

```
s3://raw-bucket/telegram/context_date=YYYY-MM-DD/
```

---

### 🔹 ENRICHED Layer
- Processed data in Parquet format
- Columnar storage for analytical performance
- Partitioned by `context_date`
- Queried using Amazon Athena

Example structure:

```
s3://enriched-bucket/telegram/context_date=YYYY-MM-DD/
```

---

## 🧠 Engineering Concepts Applied

- Serverless architecture
- Data Lake layered design (RAW / ENRICHED)
- Separation of ingestion and transformation responsibilities
- Partitioning strategy for performance optimization
- Columnar storage (Parquet)
- Scheduled ETL with EventBridge
- Analytical querying with Athena

---

## 📊 Analytical Capabilities

Available queries include:

- Messages per day
- Messages per user per day
- Average message length
- Temporal analysis (hour / weekday / week number)
- Word frequency ranking

SQL scripts available at:

```
sql/03_analytics_queries.sql
```

---

## ⚙️ Technologies Used

- AWS S3
- AWS Lambda
- AWS EventBridge
- AWS API Gateway
- Amazon Athena
- Python
- PyArrow
- SQL

---

## 🔐 Security & Best Practices

- No credentials stored in repository
- Environment variables used for configuration
- No sensitive production data included
- Modularized ETL logic

---

## 📈 Future Improvements

- Infrastructure as Code (Terraform)
- AWS Glue Catalog integration
- Dashboard layer (Power BI / Looker)
- Data quality validation layer
- Automated partition discovery

---

## 👩‍💻 Author

Developed as part of a professional transition into Data Engineering, applying real-world AWS architecture patterns and serverless design principles.
