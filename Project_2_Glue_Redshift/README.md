# Project 2: S3 → Glue → Redshift

## Data Flow
CSV (S3) → Glue Job (transform) → CSV (S3) → Redshift COPY → Warehouse
- Read real estate CSV from S3
- Cleaned: removed nulls, invalid prices
- Transformed: converted data types, added price_per_sqft column
- Wrote to S3 as CSV
- Created table in Redshift
- Loaded to Redshift with COPY command

## Results
- Rows loaded: 2000
- Key transformations: lowercase columns, type casting, new column

