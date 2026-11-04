
# Azure Data Factory

This folder contains the Azure Data Factory pipeline
definitions used in my end-to-end data engineering project.

## Main Pipeline: copyalltables

1. Lookup activity retrieves source SQL Server table names.
2. ForEach iterates through the source tables.
3. Copy Data ingests the tables into ADLS Gen2 Bronze.
4. Run_Medallion_Job triggers the Databricks workflow.

## Data Source

AdventureWorksLT2016 - SalesLT schema

## Destination

Azure Data Lake Storage Gen2 - Bronze layer

## Orchestration

ADF triggers the Databricks medallion_pipeline_job
after successful ingestion.
