# End-to-End Pipeline Validation

## Objective

Validate that newly inserted SQL Server records can propagate through the Azure data platform and become available in Power BI.

## Test Environment

- **Source:** SQL Server — AdventureWorksLT2016
- **Ingestion:** Azure Data Factory — `copyalltables`
- **Storage:** ADLS Gen2 — Bronze, Silver, Gold
- **Transformation:** Azure Databricks — `medallion_pipeline_job`
- **Query Layer:** Azure Synapse Serverless SQL — `gold_db`
- **Reporting:** Power BI

## Test Scenario

Two test customer records were inserted into the `SalesLT.Customer` source table.

| Test Metric | Value |
|---|---|
| Initial customer count | 847 |
| New records inserted | 2 |
| Final source count | 849 |
| New records visible in Power BI | Yes |

## Validation Steps

1. Confirmed the original customer count in SQL Server.
2. Inserted two test customer records.
3. Verified that the source table contained 849 records.
4. Executed the ADF ingestion pipeline.
5. Corrected a Databricks notebook error and manually reran the Databricks workflow.
6. Queried the Gold reporting layer through Synapse.
7. Refreshed Power BI and verified the test records.

## Test Result

**Passed — Source-to-report data propagation verified.**

The inserted customer records became visible in Power BI.
