# Project 4: EC2 + Python Script

## Summary

Run Python code on a virtual server (EC2) that processes data and connects to AWS services.

```
Launch EC2 → SSH Connect → Run Python Script → Process Data → Output to S3
```

---

## Step-by-Step Setup

### Step 1: Create SSH Key Pair

1. Go to **EC2** → **Key Pairs**
2. Click **"Create key pair"**
3. Name: `my-ec2-key`
4. Key file format: `.pem` (Mac/Linux) or `.ppk` (Windows)
5. Download and save safely

### Step 2: Create Security Group

1. Go to **EC2** → **Security Groups**
2. Click **"Create security group"**
3. Name: `ec2-python-sg`
4. Add inbound rules:
   - Type: SSH, Port: 22, Source: 0.0.0.0/0
   - Type: HTTPS, Port: 443, Source: 0.0.0.0/0
5. Create

### Step 3: Create IAM Role

1. Go to **IAM** → **Roles** → **Create role**
2. Service: EC2
3. Add permission: `AmazonS3FullAccess`
4. Name: `EC2S3Role`
5. Create

### Step 4: Launch EC2 Instance

1. Go to **EC2** → **Instances** → **Launch instances**
2. AMI: **Ubuntu Server 22.04 LTS** (plain, no SQL Server)
3. Instance type: **t2.micro**
4. IAM role: **EC2S3Role**
5. Security group: **ec2-python-sg**
6. Key pair: **my-ec2-key**
7. Click **"Launch instances"**
8. Wait 1-2 minutes for instance to start

### Step 5: Connect via SSH

**For Mac/Linux:**
```bash
ssh -i my-ec2-key.pem ubuntu@your-public-ip
```

**For Windows:**
- Download PuTTY from: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
- Open PuTTY
- Host: your public IP
- Port: 22
- SSH → Auth: Select your `.ppk` key
- Click Open
- Login as: `ubuntu`

### Step 6: Install Python & AWS SDK

Once connected, run:
```bash
sudo apt update
sudo apt install -y python3-pip
pip3 install boto3 pandas
```

### Step 7: Create Python Script

```bash
nano process_data.py
```

Copy and paste:

```python
import boto3

s3 = boto3.client('s3')

def process_csv():
    bucket = 'your-name-lambda-input'  # Change this
    key = 'HousePricePredictionDataset.csv'
    
    print(f"Reading {key} from {bucket}...")
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        
        lines = file_content.strip().split('\n')
        row_count = len(lines) - 1
        
        print(f"Total rows: {row_count}")
        
        # Extract prices and calculate average
        prices = []
        for row in lines[1:]:
            try:
                price = float(row.split(',')[-1])
                prices.append(price)
            except:
                pass
        
        if prices:
            avg_price = sum(prices) / len(prices)
            print(f"Average price: ${avg_price:,.2f}")
            print(f"Min: ${min(prices):,.2f}, Max: ${max(prices):,.2f}")
        
        # Write results
        results = f"File: {key}\nRows: {row_count}\nAvg Price: ${avg_price:,.2f}\n"
        
        s3.put_object(
            Bucket='your-name-output-bucket',
            Key='ec2-results/analysis.txt',
            Body=results
        )
        
        print("✅ Results uploaded to S3!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    process_csv()
```

Replace bucket names with your actual buckets.

Press Ctrl+X, then Y, then Enter to save.

### Step 8: Run Script

```bash
python3 process_data.py
```

You should see:
```
Reading HousePricePredictionDataset.csv from your-bucket...
Total rows: 2000
Average price: $500,000.00
Min: $100,000.00, Max: $1,000,000.00
✅ Results uploaded to S3!
```

### Step 9: Verify Results

1. Go to **S3** → your output bucket
2. Open **ec2-results/** folder
3. Check **analysis.txt** file




