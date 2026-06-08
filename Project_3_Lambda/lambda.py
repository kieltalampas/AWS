import json
import boto3
from urllib.parse import unquote

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    print("Lambda triggered!")
    print(f"Event: {json.dumps(event)}")
    
    # Get the bucket and file name from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote(event['Records'][0]['s3']['object']['key'])  # DECODE URL
    
    print(f"Processing file: {key} from bucket: {bucket}")
    
    try:
        # Read the file from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        
        print(f"File size: {len(file_content)} bytes")
        
        # Simple processing: count rows
        lines = file_content.split('\n')
        row_count = len(lines) - 1  # Subtract header
        
        # Create output
        output_message = f"""
        File: {key}
        Total rows: {row_count}
        Processing completed successfully!
        """
        
        # Write result to output bucket
        output_key = f"processed/{key.split('/')[-1]}.log"
        s3_client.put_object(
            Bucket='kiel-output-bucket',
            Key=output_key,
            Body=output_message
        )
        
        print(f"Output written to: {output_key}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully processed {key}')
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }