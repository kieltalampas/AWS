import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ===== STEP 1: Read from S3 =====
print("Reading CSV from S3...")
df = spark.read.csv("s3://kiel-realestate-data/House Price Prediction Dataset.csv", header=True, inferSchema=True)

print(f"Loaded {df.count()} rows")
print("Original schema:")
df.printSchema()

# ===== CONVERT ALL COLUMNS TO LOWERCASE =====
print("Converting column names to lowercase...")
df = df.select([col(c).alias(c.lower()) for c in df.columns])

# ===== STEP 2: Clean & Transform =====
print("Cleaning data...")

df = df.filter(col("price").isNotNull())
df = df.filter(col("price") > 0)
df = df.withColumn("yearbuilt", col("yearbuilt").cast("int"))
df = df.withColumn("price", col("price").cast("double"))
df = df.withColumn("pricesqft", col("price") / col("area"))

print(f"After cleaning: {df.count()} rows")
print("Transformed schema:")
df.printSchema()

# ===== STEP 3: Write to S3 (Parquet format) =====
# ===== STEP 3: Write to S3 (CSV format) =====
print("Writing transformed data to S3 as CSV...")
output_path = "s3://kiel-glue-output/house_data_transformed_csv/"
df.write.mode("overwrite").option("header", "true").csv(output_path)

print(f"Data successfully written to {output_path}")

job.commit()