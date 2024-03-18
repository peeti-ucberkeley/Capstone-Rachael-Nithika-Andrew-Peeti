import os
import io
import boto3
import base64
import json
import csv

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime = boto3.client('runtime.sagemaker')
s3 = boto3.client("s3")

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    key = event['s3_key']
    bucket = event['s3_bucket']
    
    ## Downloads the image sent in the event and stores it locally
    file_path = os.path.join('/tmp', 'image.jpg')
    with open(file_path, 'wb') as f:
        s3.download_fileobj(bucket, key, f)
    
    with open("/tmp/image.jpg", "rb") as f:
        image_data = f.read()
    
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='application/x-image',
                                       Body=image_data)
    print(response)
    
    result = json.loads(response['Body'].read().decode())
    print(result)
    
    return result

# Test JSON
"""
{
  "s3_bucket": "isicbucket",
  "s3_key": "preprocessed/224x224_center_crop/val/actinic keratoses/ISIC_0024654.jpg"
}
"""