# Project 1: S3 + Athena - Real Estate Data Analysis

## Dataset
- Name: House Price Prediction Dataset
- Source: Kaggle
- Rows: 2000
- Columns: [Id	Area	Bedrooms	Bathrooms	Floors	YearBuilt	Location	Condition	Garage	Price]

## Process
- Uploaded CSV to S3 bucket
- Created Athena table from S3 data
- Ran SQL queries to explore the data


## AWS Concepts
- S3 buckets store raw data
- Athena reads directly from S3 without moving data
- External tables point to S3 files
- CSV data needs ROW FORMAT DELIMITED parsing
- SQL queries on cloud data are fast + cheap



