# Databricks notebook source
bronze_path = "/Volumes/demo_de_databricks01/default/bronze_files/SalesLT/Address/"

display(dbutils.fs.ls(bronze_path))

# COMMAND ----------

input_path = "/Volumes/demo_de_databricks01/default/bronze_files/SalesLT/Address/Address.parquet"

df = spark.read.format("parquet").load(input_path)

# COMMAND ----------

display(df)

# COMMAND ----------

from pyspark.sql.functions import to_date

df = df.withColumn(
    "ModifiedDate",
    to_date("ModifiedDate")
)

display(df)

# COMMAND ----------

silver_path = "/Volumes/demo_de_databricks01/default/silver_files/SalesLT/Address"

df.write.format("delta") \
    .mode("overwrite") \
    .save(silver_path)

print("Address data successfully written to Silver!")

# COMMAND ----------

silver_df = spark.read.format("delta").load(silver_path)
print("Bronze rows:", df.count())
print("Silver rows:", silver_df.count())

# COMMAND ----------

bronze_root = "/Volumes/demo_de_databricks01/default/bronze_files/SalesLT/"

table_names = [
    item.name.rstrip("/")
    for item in dbutils.fs.ls(bronze_root)
    if item.isDir()
]

print("Total tables:", len(table_names))
print("Tables:", table_names)

# COMMAND ----------

from pyspark.sql.functions import to_date
from pyspark.sql.types import TimestampType, DateType

silver_root = "/Volumes/demo_de_databricks01/default/silver_files/SalesLT/"

for table in table_names:

    print(f"Processing: {table}")

    # Read Bronze Parquet data
    input_path = f"{bronze_root}{table}/{table}.parquet"

    df = spark.read.parquet(input_path)

    # Convert date and timestamp columns to DateType
    for field in df.schema.fields:
        if isinstance(field.dataType, (TimestampType, DateType)):
            df = df.withColumn(
                field.name,
                to_date(field.name)
            )

    # Write transformed data to Silver as Delta
    output_path = f"{silver_root}{table}"

    df.write.format("delta") \
        .mode("overwrite") \
        .save(output_path)

    print(f"Successfully written: {table}")

# COMMAND ----------

validation_results = []

for table in table_names:

    bronze_path = f"{bronze_root}{table}/{table}.parquet"
    silver_path = f"{silver_root}{table}"

    bronze_count = spark.read.parquet(bronze_path).count()
    silver_count = spark.read.format("delta").load(silver_path).count()

    status = "PASS" if bronze_count == silver_count else "FAIL"

    validation_results.append(
        (table, bronze_count, silver_count, status)
    )

validation_df = spark.createDataFrame(
    validation_results,
    ["TableName", "BronzeCount", "SilverCount", "Status"]
)

display(validation_df)