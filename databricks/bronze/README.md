
# Bronze Layer

The Bronze layer stores raw data ingested from
SQL Server into Azure Data Lake Storage Gen2.

Azure Data Factory performs ingestion using
Lookup, ForEach, and Copy Data activities.

The Bronze files are used as input for the
Databricks Bronze-to-Silver transformation.
