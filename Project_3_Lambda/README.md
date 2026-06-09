
# Project 3: Lambda + S3 (Event-Driven Processing)

## Summary

When a file is uploaded to S3, Lambda automatically processes it without manual intervention.

```
S3 Upload → Lambda Trigger → Process File → Output to S3
```

---

## Step-by-Step Setup

### Step 1: Create S3 Buckets

1. Go to **S3** → Create bucket
2. Name: `your-name-lambda-input`
3. Create bucket
4. Repeat for: `your-name-output-bucket`

### Step 2: Create IAM Role

1. Go to **IAM** → **Roles** → **Create role**
2. Service: Lambda
3. Add permissions:
   - `AmazonS3FullAccess`
   - `AWSLambdaBasicExecutionRole`
4. Name: `LambdaS3Role`
5. Create

### Step 3: Create Lambda Function

1. Go to **Lambda** → **Create function**
2. Name: `realestate-processor`
3. Runtime: Python 3.11
4. Execution role: `LambdaS3Role`
5. Click **Create**

### Step 4: Add Code

Delete default code and paste:

```python
import json
import boto3
from urllib.parse import unquote

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    print("Lambda triggered!")
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote(event['Records'][0]['s3']['object']['key'])
    
    print(f"Processing file: {key} from bucket: {bucket}")
    
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        
        lines = file_content.split('\n')
        row_count = len(lines) - 1
        
        output_message = f"File: {key}\nTotal rows: {row_count}\nProcessing completed!"
        
        output_key = f"processed/{key.split('/')[-1]}.log"
        s3_client.put_object(
            Bucket='your-name-output-bucket',
            Key=output_key,
            Body=output_message
        )
        
        print(f"Output written to: {output_key}")
        
        return {'statusCode': 200, 'body': 'Success'}
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': f'Error: {str(e)}'}
```

Replace `your-name-output-bucket` with your actual bucket name.

Click **Deploy**.

### Step 5: Add S3 Trigger

1. Click **"Add trigger"**
2. Source: S3
3. Bucket: `your-name-lambda-input`
4. Event: PUT
5. Click **Add**

### Step 6: Test

1. Click **"Test"** tab
2. Create test event with this JSON:

```json
{
  "Records": [
    {
      "s3": {
        "bucket": {"name": "your-name-lambda-input"},
        "object": {"key": "HousePricePredictionDataset.csv"}
      }
    }
  ]
}
```

3. Click **Test**

### Step 7: Verify Output

1. Go to **S3** → your output bucket
2. Open `processed/` folder
3. You should see a `.log` file



