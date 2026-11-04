# Databricks notebook source
silver_root = "/Volumes/demo_de_databricks01/default/silver_files/SalesLT/"
gold_root = "/Volumes/demo_de_databricks01/default/gold_files/SalesLT/"

df = spark.read.format("delta").load(
    silver_root + "SalesOrderHeader"
)

print(df.columns)
display(df)

# COMMAND ----------

import re

def to_snake_case(column_name):
    # Handle uppercase abbreviations followed by words
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', column_name)

    # Separate lowercase letters or digits from uppercase letters
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)

    return name.lower()

# Rename every column in the DataFrame
for column in df.columns:
    df = df.withColumnRenamed(column, to_snake_case(column))

print(df.columns)

display(df)

# COMMAND ----------

gold_path = gold_root + "SalesOrderHeader"

df.write.format("delta") \
    .mode("overwrite") \
    .save(gold_path)

print("SalesOrderHeader successfully written to Gold!")

# COMMAND ----------

gold_df = spark.read.format("delta").load(gold_path)

print("Gold row count:", gold_df.count())

display(gold_df)

# COMMAND ----------

import re

def to_snake_case(column_name):
    name = re.sub(
        r'([A-Z]+)([A-Z][a-z])',
        r'\1_\2',
        column_name
    )
    name = re.sub(
        r'([a-z0-9])([A-Z])',
        r'\1_\2',
        name
    )
    return name.lower()

table_names = [
    item.name.rstrip("/")
    for item in dbutils.fs.ls(silver_root)
    if item.isDir()
]

print("Total tables:", len(table_names))
print("Tables:", table_names)

# COMMAND ----------

for table in table_names:

    print(f"Processing: {table}")

    # 1. Read the Delta table from Silver
    input_path = silver_root + table

    df = spark.read.format("delta").load(input_path)

    # 2. Convert all column names to snake_case
    for column in df.columns:
        df = df.withColumnRenamed(
            column,
            to_snake_case(column)
        )

    # 3. Write the transformed data to Gold
    output_path = gold_root + table

    df.write.format("delta") \
        .mode("overwrite") \
        .save(output_path)

    print(f"Successfully written to Gold: {table}")

# COMMAND ----------

validation_results = []

for table in table_names:

    silver_df = spark.read.format("delta").load(
        silver_root + table
    )

    gold_df = spark.read.format("delta").load(
        gold_root + table
    )

    silver_count = silver_df.count()
    gold_count = gold_df.count()

    status = "PASS" if silver_count == gold_count else "FAIL"

    validation_results.append(
        (table, silver_count, gold_count, status)
    )

validation_df = spark.createDataFrame(
    validation_results,
    ["TableName", "SilverCount", "GoldCount", "Status"]
)

display(validation_df)